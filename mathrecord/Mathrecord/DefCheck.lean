import Mathrecord.Frontend

/-! Positive kernel certification of "holds by definition": for each named
theorem, if its statement is an equality/iff whose two sides are
definitionally equal, the verdict is literally true by the kernel. -/

namespace Mathrecord.DefCheck

open Lean Meta

def defcheck (namesPath : System.FilePath) (envProbe : System.FilePath)
    (out : System.FilePath) : IO Unit := do
  let pf ← Mathrecord.processFile envProbe
  let env := pf.env
  let names := (← IO.FS.readFile namesPath).splitOn "\n" |>.filter (· ≠ "")
  let h ← IO.FS.Handle.mk out .write
  let coreCtx : Core.Context := { fileName := "<defcheck>", fileMap := default }
  let act : CoreM Unit := do
    for nm in names do
      let n := nm.toName
      let res ← try
        Core.withCurrHeartbeats <| (do
          let some ci := env.find? n | pure "absent"
          forallTelescope ci.type fun _ body => do
            let b ← whnfR body
            match b.getAppFnArgs with
            | (`Eq, #[_, lhs, rhs]) | (`Iff, #[lhs, rhs]) | (`HEq, #[_, lhs, _, rhs]) =>
              pure (if (← isDefEq lhs rhs) then "defeq" else "eq-shaped-not-defeq")
            | _ => pure "not-eq-shaped" : MetaM String).run'
      catch e => pure s!"check-failed"
      h.putStrLn s!"{nm}\t{res}"
    pure ()
  let (_, _) ← act.toIO coreCtx { env }
  h.flush
  IO.println s!"defcheck: {names.length} names -> {out}"

end Mathrecord.DefCheck
