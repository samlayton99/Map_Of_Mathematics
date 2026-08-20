import Mathrecord.Study

/-! Full-environment dependency dump — v3, the exact move substrate.

One JSONL row per constant:
  n/k/c/t/v/ir  as before (name, kind, classification flags, type deps,
                value deps, inductive-isRec)
  pr            the constant's type is genuinely proposition-valued
                (kernel check via `Meta.isProp`, NOT the kind proxy)
  prf           true when the Prop check fell back to the kind proxy
  vo            per value-dep (aligned with `v`) an 8-vector of occurrence
                counts by ROLE (counts are over distinct shared subterm
                occurrences — DAG multiplicity, not tree multiplicity):
                  0 applied/bare in proof body   1 let-bound value
                  2 explicit argument            3 implicit argument
                  4 instance-implicit argument   5 strict-implicit argument
                  6 type annotation              7 unresolved binder role
  bf            number of argument positions whose binder role could not be
                resolved even after definitional unfolding (instrumented
                fallback, judge condition; those args are counted in role 7)
  hb            derived compatibility set: refs with any occurrence in
                roles {0,1,2,7}
  rt            root head chain (kept for provenance experiments; the
                strategy channel built on it is parked)

Binder roles come from `forallBoundedTelescope` on the applied constant's
type (definitional unfolding included), cached per (constant, arity). No
names, no namespaces, no kind proxies in the substrate fields.
-/

namespace Mathrecord.DepDump

open Lean Meta Mathrecord Mathrecord.Extract Mathrecord.Study

/-- Binder-info prefix of a constant's type (syntactic Pis only) — used by
`rootChain` only, where approximation is acceptable. -/
def sigBinders (env : Environment) (cache : IO.Ref (Std.HashMap Name (Array BinderInfo)))
    (c : Name) : BaseIO (Array BinderInfo) := do
  if let some bis := (← cache.get).get? c then
    return bis
  let bis := match env.find? c with
    | some ci => collect ci.type #[]
    | none => #[]
  cache.modify (·.insert c bis)
  return bis
where
  collect : Expr → Array BinderInfo → Array BinderInfo
    | .forallE _ _ b bi, acc => collect b (acc.push bi)
    | _, acc => acc

/-- Exact binder-info prefix via telescope (definitional unfolding included).
Cache stores (infos, requestedBound): if a previous request with bound ≥ the
current need returned fewer infos, the type truly has no more Pis. -/
def exactBinders (cache : IO.Ref (Std.HashMap Name (Array BinderInfo × Nat)))
    (c : Name) (needed : Nat) : MetaM (Array BinderInfo) := do
  if let some (bis, bound) := (← cache.get).get? c then
    if bis.size ≥ needed || bis.size < bound then
      return bis
  let some ci := (← getEnv).find? c | return #[]
  let bis ← try
    forallBoundedTelescope ci.type (some needed) fun xs _ =>
      xs.mapM fun x => do pure (← x.fvarId!.getDecl).binderInfo
  catch _ => pure #[]
  cache.modify (·.insert c (bis, needed))
  return bis

/-- Role indices (see module docstring). -/
abbrev Roles := Array UInt32   -- length 8 per referenced constant

/-- Walk a value term collecting, per referenced constant, occurrence counts
by role. Explicit stack; memo on (subterm pointer, role). -/
def occurrenceRoles (cache : IO.Ref (Std.HashMap Name (Array BinderInfo × Nat)))
    (value : Expr) : MetaM (Std.HashMap Name Roles × Nat) := do
  let mut occ : Std.HashMap Name Roles := {}
  let mut fallbacks := 0
  let mut seen : Std.HashSet (USize × UInt8) := {}
  -- keep visited exprs alive so pointer keys stay valid
  let mut pinned : Array Expr := #[]
  let mut stack : Array (Expr × UInt8) := #[(value, 0)]
  let bump (m : Std.HashMap Name Roles) (c : Name) (r : UInt8) : Std.HashMap Name Roles :=
    let v := m.getD c (Array.replicate 8 0)
    m.insert c (v.set! r.toNat (v[r.toNat]! + 1))
  while h : stack.size > 0 do
    let (e, role) := stack[stack.size - 1]
    stack := stack.pop
    let key := (exprPtr e, role)
    if seen.contains key then
      continue
    seen := seen.insert key
    pinned := pinned.push e
    match e with
    | .app .. =>
      let fn := e.getAppFn
      let args := e.getAppArgs
      match fn with
      | .const c _ =>
        occ := bump occ c role
        let bis ← exactBinders cache c args.size
        for i in [0:args.size] do
          let argRole : UInt8 := match bis[i]? with
            | some .default => 2
            | some .implicit => 3
            | some .instImplicit => 4
            | some .strictImplicit => 5
            | none => 7
          if argRole == 7 then
            fallbacks := fallbacks + 1
          stack := stack.push (args[i]!, argRole)
      | _ =>
        stack := stack.push (fn, role)
        for a in args do
          stack := stack.push (a, role)
    | .lam _ t b _ =>
      stack := stack.push (t, 6)
      stack := stack.push (b, role)
    | .forallE _ t b _ =>
      stack := stack.push (t, 6)
      stack := stack.push (b, 6)
    | .letE _ t v b _ =>
      stack := stack.push (t, 6)
      stack := stack.push (v, 1)
      stack := stack.push (b, role)
    | .mdata _ b => stack := stack.push (b, role)
    | .proj _ _ b => stack := stack.push (b, role)
    | .const c _ => occ := bump occ c role
    | _ => pure ()
  return (occ, fallbacks)

/-- Outermost head chain (kept for provenance experiments; approximate). -/
def rootChain (env : Environment) (cache : IO.Ref (Std.HashMap Name (Array BinderInfo)))
    (value : Expr) : BaseIO (Array Name) := do
  let mut chain : Array Name := #[]
  let mut e := value
  for _ in [0:5] do
    let mut peeled := true
    while peeled do
      match e with
      | .lam _ _ b _ => e := b
      | .letE _ _ _ b _ => e := b
      | .mdata _ b => e := b
      | _ => peeled := false
    match e.getAppFn with
    | .const c _ =>
      chain := chain.push c
      let args := e.getAppArgs
      if args.isEmpty then
        break
      let bis ← sigBinders env cache c
      let mut nxt : Option Expr := none
      for i in [0:args.size] do
        match bis[i]? with
        | some .default => nxt := some args[i]!
        | none => nxt := some args[i]!
        | some _ => pure ()
      match nxt with
      | some a => e := a
      | none => break
    | _ => break
  return chain

def depDump (path : System.FilePath) (out : System.FilePath) : IO Unit := do
  let pf ← Mathrecord.processFile path mathlibOptions
  let env := pf.env
  IO.println s!"env loaded: {env.header.moduleNames.size} modules"
  let h ← IO.FS.Handle.mk out .write
  let coreCtx : Core.Context := { fileName := pf.fileName, fileMap := default }
  let sigCache ← IO.mkRef ({} : Std.HashMap Name (Array BinderInfo))
  let exactCache ← IO.mkRef ({} : Std.HashMap Name (Array BinderInfo × Nat))
  let act : CoreM Unit := do
    let mut count := 0
    let mut propFallbacks := 0
    let mut kindPropDisagree := 0
    for (n, ci) in env.constants.toList do
      let isInst ← Meta.isInstance n
      let cls := classify env n isInst
      let tdeps := ci.type.getUsedConstantsAsSet.toArray
      -- exact Prop check (kernel), instrumented fallback to the kind proxy.
      -- Heartbeats reset per constant so one pathological type cannot
      -- exhaust the global budget (that failure mode killed run 1 at 50k).
      let kindIsThm := match ci with | .thmInfo _ => true | _ => false
      let (isPr, prFell) ← try
        let b ← Core.withCurrHeartbeats <| (Meta.isProp ci.type).run'
        pure (b, false)
      catch _ => pure (kindIsThm, true)
      if prFell then propFallbacks := propFallbacks + 1
      if isPr != kindIsThm && !prFell then kindPropDisagree := kindPropDisagree + 1
      let (vdeps, voJson, bf, hb, rt) ← match ci.value? (allowOpaque := true) with
        | some v => do
          let vdeps := v.getUsedConstantsAsSet.toArray
          -- per-constant heartbeat budget; on failure fall back loudly:
          -- every ref counted once in role 7 (unresolved), kept in hb
          let occRes ← try
            let r ← Core.withCurrHeartbeats <|
              ((occurrenceRoles exactCache v).run' : CoreM _)
            pure (some r)
          catch _ => pure none
          let (occ, fb) := match occRes with
            | some (o, f) => (o, f)
            | none =>
              (vdeps.foldl (fun m d =>
                m.insert d ((Array.replicate 8 (0 : UInt32)).set! 7 1)) {},
               vdeps.size)
          let vo := vdeps.map fun d =>
            let r := occ.getD d (Array.replicate 8 0)
            Json.arr (r.map (fun x => Json.num x.toNat))
          let hb := vdeps.filter fun d =>
            let r := occ.getD d (Array.replicate 8 0)
            r[0]! + r[1]! + r[2]! + r[7]! > 0
          let rt ← rootChain env sigCache v
          pure (vdeps, Json.arr vo, fb, hb, rt)
        | none => pure (#[], Json.arr #[], 0, #[], #[])
      let mut fields := [
        ("n", Json.str (toString n)),
        ("k", Json.str (kindString ci)),
        ("c", toJson (cls.map toString)),
        ("pr", Json.bool isPr),
        ("t", toJson (tdeps.map toString)),
        ("v", toJson (vdeps.map toString)),
        ("vo", voJson),
        ("hb", toJson (hb.map toString)),
        ("rt", toJson (rt.map toString))]
      if prFell then
        fields := fields ++ [("prf", Json.bool true)]
      -- machine-generated flag: no source declaration range (recorded env
      -- fact: the elaborator logs ranges for human-written declarations)
      if (← Lean.findDeclarationRanges? n).isNone then
        fields := fields ++ [("gen", Json.bool true)]
      if bf > 0 then
        fields := fields ++ [("bf", Json.num bf)]
      if let .inductInfo iv := ci then
        fields := fields ++ [("ir", Json.bool iv.isRec)]
      h.putStrLn (Json.mkObj fields).compress
      count := count + 1
      if count % 50000 == 0 then
        IO.println s!"  {count} constants dumped"
    IO.println s!"done: {count} constants; prop-check fallbacks {propFallbacks}; kind/prop disagreements {kindPropDisagree}"
  let (_, _) ← act.toIO coreCtx { env }
  h.flush

end Mathrecord.DepDump
