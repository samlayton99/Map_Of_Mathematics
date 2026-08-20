import Mathrecord.Study

/-! Full-environment dependency dump.

Loads an environment (e.g. `import Mathlib`) and writes one JSONL row per
constant: name, kind, classification flags, type-deps, value-deps, and — new —
the load-bearing head set `hb`: constants that occur in the value at the head
of an application (or bare) in a LOAD-BEARING position. Positions are
classified purely syntactically from the kernel term:

  load-bearing: proof root, let-bound values, bodies of lambdas/lets,
                arguments filling EXPLICIT binders of an applied constant
  background:   arguments filling instance-implicit / implicit / strict-
                implicit binders, and all type annotations (binder types,
                forallE parts)

Argument roles are read from the applied constant's own type signature
(syntactic Pi prefix). Unknown roles are treated as load-bearing
(conservative: keep rather than lose). No elaboration, no name heuristics.
-/

namespace Mathrecord.DepDump

open Lean Meta Mathrecord Mathrecord.Extract Mathrecord.Study

/-- Binder-info prefix of a constant's type (syntactic Pis only), cached. -/
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

/-- Collect the load-bearing head constants of a value term (explicit stack,
sharing-aware memoization on (subterm, position-class)). -/
def loadBearingHeads (env : Environment)
    (cache : IO.Ref (Std.HashMap Name (Array BinderInfo))) (value : Expr) :
    BaseIO NameSet := do
  let mut hb : NameSet := {}
  let mut seen : Std.HashSet (Expr × Bool) := {}
  let mut stack : Array (Expr × Bool) := #[(value, true)]
  while h : stack.size > 0 do
    let (e, load) := stack[stack.size - 1]
    stack := stack.pop
    if seen.contains (e, load) then
      continue
    seen := seen.insert (e, load)
    match e with
    | .app .. =>
      let fn := e.getAppFn
      let args := e.getAppArgs
      match fn with
      | .const c _ =>
        if load then hb := hb.insert c
        let bis ← sigBinders env cache c
        for i in [0:args.size] do
          let aload := match bis[i]? with
            | some .default => load
            | some _ => false        -- instImplicit / implicit / strictImplicit
            | none => load           -- beyond syntactic signature: conservative
          stack := stack.push (args[i]!, aload)
      | _ =>
        stack := stack.push (fn, load)
        for a in args do
          stack := stack.push (a, load)
    | .lam _ t b _ =>
      stack := stack.push (t, false)
      stack := stack.push (b, load)
    | .forallE _ t b _ =>
      stack := stack.push (t, false)
      stack := stack.push (b, false)
    | .letE _ t v b _ =>
      stack := stack.push (t, false)
      stack := stack.push (v, load)
      stack := stack.push (b, load)
    | .mdata _ b => stack := stack.push (b, load)
    | .proj _ _ b => stack := stack.push (b, load)
    | .const c _ => if load then hb := hb.insert c
    | _ => pure ()
  return hb

def depDump (path : System.FilePath) (out : System.FilePath) : IO Unit := do
  let pf ← Mathrecord.processFile path mathlibOptions
  let env := pf.env
  IO.println s!"env loaded: {env.header.moduleNames.size} modules"
  let h ← IO.FS.Handle.mk out .write
  let coreCtx : Core.Context := { fileName := pf.fileName, fileMap := default }
  let sigCache ← IO.mkRef ({} : Std.HashMap Name (Array BinderInfo))
  let act : CoreM Unit := do
    let mut count := 0
    for (n, ci) in env.constants.toList do
      let isInst ← Meta.isInstance n
      let cls := classify env n isInst
      let tdeps := ci.type.getUsedConstantsAsSet.toArray
      let (vdeps, hb) ← match ci.value? (allowOpaque := true) with
        | some v => do
          let hb ← loadBearingHeads env sigCache v
          pure (v.getUsedConstantsAsSet.toArray, hb.toArray)
        | none => pure (#[], #[])
      let j := Json.mkObj [
        ("n", Json.str (toString n)),
        ("k", Json.str (kindString ci)),
        ("c", toJson (cls.map toString)),
        ("t", toJson (tdeps.map toString)),
        ("v", toJson (vdeps.map toString)),
        ("hb", toJson (hb.map toString))]
      h.putStrLn j.compress
      count := count + 1
      if count % 50000 == 0 then
        IO.println s!"  {count} constants dumped"
    IO.println s!"done: {count} constants"
  let (_, _) ← act.toIO coreCtx { env }
  h.flush

end Mathrecord.DepDump
