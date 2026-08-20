import Mathrecord.Study

/-! Full-environment dependency dump.

Loads an environment (e.g. `import Mathlib`) and writes one JSONL row per
constant: name, kind, classification flags, type-deps, value-deps. Used to
compute recursive unfolding depth over the complete library closure — the
global measure the Phase 3 corpus graph could not support (boundary artifact).
-/

namespace Mathrecord.DepDump

open Lean Meta Mathrecord Mathrecord.Extract Mathrecord.Study

def depDump (path : System.FilePath) (out : System.FilePath) : IO Unit := do
  let pf ← Mathrecord.processFile path mathlibOptions
  let env := pf.env
  IO.println s!"env loaded: {env.header.moduleNames.size} modules"
  let h ← IO.FS.Handle.mk out .write
  let coreCtx : Core.Context := { fileName := pf.fileName, fileMap := default }
  let act : CoreM Unit := do
    let mut count := 0
    for (n, ci) in env.constants.toList do
      let isInst ← Meta.isInstance n
      let cls := classify env n isInst
      let tdeps := ci.type.getUsedConstantsAsSet.toArray
      let vdeps := match ci.value? (allowOpaque := true) with
        | some v => v.getUsedConstantsAsSet.toArray
        | none => #[]
      let j := Json.mkObj [
        ("n", Json.str (toString n)),
        ("k", Json.str (kindString ci)),
        ("c", toJson (cls.map toString)),
        ("t", toJson (tdeps.map toString)),
        ("v", toJson (vdeps.map toString))]
      h.putStrLn j.compress
      count := count + 1
      if count % 50000 == 0 then
        IO.println s!"  {count} constants dumped"
    IO.println s!"done: {count} constants"
  let (_, _) ← act.toIO coreCtx { env }
  h.flush

end Mathrecord.DepDump
