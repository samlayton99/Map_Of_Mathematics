import Mathrecord.Frontend

/-! Exact module lookup: name -> defining module, from the environment's
own records (no name-based file search). Used by audits to locate the true
source file of any declaration. -/

namespace Mathrecord.Modules

open Lean

def modules (namesPath : System.FilePath) (envProbe : System.FilePath)
    (out : System.FilePath) : IO Unit := do
  let pf ← Mathrecord.processFile envProbe
  let env := pf.env
  let names := (← IO.FS.readFile namesPath).splitOn "\n" |>.filter (· ≠ "")
  let h ← IO.FS.Handle.mk out .write
  for nm in names do
    let n := nm.toName
    let m := match env.getModuleIdxFor? n with
      | some i => toString env.header.moduleNames[i.toNat]!
      | none => if (env.find? n).isSome then "<current-or-unknown>" else "<absent>"
    h.putStrLn s!"{nm}\t{m}"
  h.flush
  IO.println s!"modules: {names.length} names resolved -> {out}"


/-- Dump per-name projection facts: is it a structure/class projection
function, and is the parent structure a class? Kernel/env facts. -/
def projflags (namesPath : System.FilePath) (envProbe : System.FilePath)
    (out : System.FilePath) : IO Unit := do
  let pf ← Mathrecord.processFile envProbe
  let env := pf.env
  let names := (← IO.FS.readFile namesPath).splitOn "\n" |>.filter (· ≠ "")
  let h ← IO.FS.Handle.mk out .write
  let mut cnt := 0
  for nm in names do
    let n := nm.toName
    match env.getProjectionFnInfo? n with
    | some info =>
      let cls := Lean.isClass env info.ctorName.getPrefix
      h.putStrLn s!"{nm}\t1\t{if cls then 1 else 0}"
      cnt := cnt + 1
    | none => pure ()
  h.flush
  IO.println s!"projflags: {cnt} projections among {names.length} names -> {out}"

end Mathrecord.Modules
