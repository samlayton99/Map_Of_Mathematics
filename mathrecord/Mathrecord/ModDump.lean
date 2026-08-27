import Mathrecord.Study

/-! Module accessibility dump.

For each module in the environment: its name, its direct imports, and its
constants in declaration order.  This is exactly what is needed to compute,
for any theorem, the legally accessible premise universe: constants of
(transitively) imported modules, plus constants declared earlier in the
theorem's own module.  Without this mask, retrieval benchmarks rank
declarations that do not exist yet at the theorem's source location.
-/

namespace Mathrecord.ModDump

open Lean Mathrecord Mathrecord.Study

def modDump (path : System.FilePath) (out : System.FilePath) : IO Unit := do
  let pf ← Mathrecord.processFile path mathlibOptions
  let env := pf.env
  let names := env.header.moduleNames
  let data := env.header.moduleData
  IO.println s!"env loaded: {names.size} modules"
  let h ← IO.FS.Handle.mk out .write
  for i in [0:names.size] do
    let md := data[i]!
    let imps : Array Json := md.imports.map (fun imp => Json.str (toString imp.module))
    let consts : Array Json := md.constNames.map (fun n => Json.str (toString n))
    let j := Json.mkObj [
      ("i", toJson i),
      ("name", Json.str (toString names[i]!)),
      ("imports", Json.arr imps),
      ("consts", Json.arr consts)]
    h.putStrLn j.compress
  IO.println s!"done: {names.size} modules"
  h.flush

end Mathrecord.ModDump
