import Mathrecord.DepDump

/-! Occurrence-level hierarchy dump — the Phase 6 Layer A substrate.

`hierdump <envProbe> <namesFile> <out.jsonl>` emits, for each named
declaration in `namesFile` that has a value, the typed occurrence forest of
its proof/definition term. Unlike `depdump` (which flattens to per-constant
role counts), this preserves WHERE each citation occurs:

One JSONL row per requested declaration:
  n      declaration name
  ok     value found and walked
  trunc  walk hit the node budget (occurrence list is a prefix)
  occ    array of occurrences, id = array index. Each occurrence is
         [const, parent, role, argIdx, nesting, nargs]:
           const    cited constant name
           parent   id of the nearest enclosing named-application occurrence
                    (-1 = root level of the value term)
           role     same 8-role scheme as depdump `vo`
           argIdx   which argument slot of the parent this occurrence sits in
                    (-1 = head position / not an argument of a named app)
           nesting  number of named-application ancestors
           nargs    number of arguments this occurrence is applied to

Dedup: a shared subterm (DAG sharing) is re-walked once per distinct
(pointer, role, parent-constant) context, so hierarchy under different
parents is preserved while identical contexts are counted once — the
hierarchical analogue of depdump's DAG multiplicity. A per-declaration node
budget guards against pathological blowup; overflows set `trunc` and are
reported loudly.
-/

namespace Mathrecord.HierDump

open Lean Meta Mathrecord Mathrecord.Study Mathrecord.DepDump

/-- One occurrence of a named constant inside a value term. -/
structure Occ where
  const   : Name
  parent  : Int
  role    : UInt8
  argIdx  : Int
  nesting : Nat
  nargs   : Nat

/-- Walk `value`, emitting the typed occurrence forest. Explicit stack;
dedup on (subterm pointer, role, parent constant). -/
def occurrenceForest (cache : IO.Ref (Std.HashMap Name (Array BinderInfo × Nat)))
    (value : Expr) (budget : Nat := 2000000) :
    MetaM (Array Occ × Bool) := do
  let mut occs : Array Occ := #[]
  let mut truncated := false
  let mut seen : Std.HashSet (USize × UInt8 × Name) := {}
  let mut pinned : Array Expr := #[]
  -- stack entry: (expr, role, parent occ id, parent const, argIdx, nesting)
  let mut stack : Array (Expr × UInt8 × Int × Name × Int × Nat) :=
    #[(value, 0, -1, .anonymous, -1, 0)]
  let mut pops := 0
  while h : stack.size > 0 do
    if pops ≥ budget then
      truncated := true
      break
    pops := pops + 1
    let (e, role, parent, pconst, argIdx, nesting) := stack[stack.size - 1]
    stack := stack.pop
    let key := (exprPtr e, role, pconst)
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
        let id : Int := occs.size
        occs := occs.push
          { const := c, parent := parent, role := role, argIdx := argIdx,
            nesting := nesting, nargs := args.size }
        let bis ← exactBinders cache c args.size
        for i in [0:args.size] do
          let argRole : UInt8 := match bis[i]? with
            | some .default => 2
            | some .implicit => 3
            | some .instImplicit => 4
            | some .strictImplicit => 5
            | none => 7
          stack := stack.push (args[i]!, argRole, id, c, i, nesting + 1)
      | _ =>
        stack := stack.push (fn, role, parent, pconst, argIdx, nesting)
        for a in args do
          stack := stack.push (a, role, parent, pconst, -1, nesting)
    | .lam _ t b _ =>
      stack := stack.push (t, 6, parent, pconst, -1, nesting)
      stack := stack.push (b, role, parent, pconst, -1, nesting)
    | .forallE _ t b _ =>
      stack := stack.push (t, 6, parent, pconst, -1, nesting)
      stack := stack.push (b, 6, parent, pconst, -1, nesting)
    | .letE _ t v b _ =>
      stack := stack.push (t, 6, parent, pconst, -1, nesting)
      stack := stack.push (v, 1, parent, pconst, -1, nesting)
      stack := stack.push (b, role, parent, pconst, -1, nesting)
    | .mdata _ b => stack := stack.push (b, role, parent, pconst, argIdx, nesting)
    | .proj _ _ b => stack := stack.push (b, role, parent, pconst, -1, nesting)
    | .const c _ =>
      occs := occs.push
        { const := c, parent := parent, role := role, argIdx := argIdx,
          nesting := nesting, nargs := 0 }
    | _ => pure ()
  return (occs, truncated)

def hierDump (envProbe : System.FilePath) (namesPath : System.FilePath)
    (out : System.FilePath) : IO Unit := do
  let pf ← Mathrecord.processFile envProbe mathlibOptions
  let env := pf.env
  IO.println s!"env loaded: {env.header.moduleNames.size} modules"
  let names := (← IO.FS.readFile namesPath).splitOn "\n" |>.filter (· ≠ "")
  let h ← IO.FS.Handle.mk out .write
  let coreCtx : Core.Context := { fileName := pf.fileName, fileMap := default }
  let exactCache ← IO.mkRef ({} : Std.HashMap Name (Array BinderInfo × Nat))
  let act : CoreM Unit := do
    let mut done := 0
    let mut truncCount := 0
    for nm in names do
      let n := nm.toName
      let row ← match env.find? n with
        | none => pure (Json.mkObj [("n", Json.str nm), ("ok", Json.bool false),
            ("err", Json.str "absent")])
        | some ci =>
          match ci.value? (allowOpaque := true) with
          | none => pure (Json.mkObj [("n", Json.str nm), ("ok", Json.bool false),
              ("err", Json.str "no value")])
          | some v => do
            let res ← try
              let r ← Core.withCurrHeartbeats <|
                ((occurrenceForest exactCache v).run' : CoreM _)
              pure (some r)
            catch _ => pure none
            match res with
            | none => pure (Json.mkObj [("n", Json.str nm),
                ("ok", Json.bool false), ("err", Json.str "walk failed")])
            | some (occs, trunc) => do
              if trunc then truncCount := truncCount + 1
              let occJson := occs.map fun o => Json.arr #[
                Json.str (toString o.const), Json.num o.parent,
                Json.num o.role.toNat, Json.num o.argIdx,
                Json.num o.nesting, Json.num o.nargs]
              pure (Json.mkObj [("n", Json.str nm), ("ok", Json.bool true),
                ("trunc", Json.bool trunc), ("occ", Json.arr occJson)])
      h.putStrLn row.compress
      done := done + 1
      if done % 10 == 0 then
        IO.println s!"  {done}/{names.length}"
    IO.println s!"done: {done} declarations; {truncCount} truncated"
  let (_, _) ← act.toIO coreCtx { env }
  h.flush

end Mathrecord.HierDump
