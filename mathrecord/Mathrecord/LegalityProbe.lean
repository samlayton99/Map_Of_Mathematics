import Mathrecord.Study

/-! Live legality probe: the smallest possible action generator.

Input: JSON {"goals": [{"n": <theorem name>, "cands": [<candidate name>...]}]}.
For each goal theorem, enter its binder context (so local instances are
registered), take its conclusion as the live goal, and for every candidate
attempt a backward application: metavariable-telescope the candidate's type
and ask the elaborator whether its conclusion unifies with the goal
(`isDefEq`, full typeclass/implicit machinery, capped heartbeats).

For each legal candidate, record how many explicit argument metavariables
remain unassigned after unification - the number of new subgoals the move
would open: the instantiated hyperedge  G -> {A_1 ... A_k}.

Output JSONL per goal: {"n":..., "legal":[{"c":..., "ng":..., "ni":...}],
"n_cands":..., "n_err":...}.
-/

namespace Mathrecord.LegalityProbe

open Lean Meta Mathrecord Mathrecord.Study

structure GoalSpec where
  name  : Name
  cands : Array Name

def parseInput (j : Json) : Except String (Array GoalSpec) := do
  let goals ← (← j.getObjVal? "goals").getArr?
  goals.mapM fun g => do
    let n ← (← g.getObjVal? "n").getStr?
    let cs ← (← g.getObjVal? "cands").getArr?
    let cands ← cs.mapM fun c => do pure (String.toName (← c.getStr?))
    pure { name := String.toName n, cands }

/-- Try candidate `c` backward against goal `g` (in the current local
context).  Returns `(numExplicitOpen, numInstOpen)` on success. -/
def tryCandidate (env : Environment) (c : Name) (g : Expr) :
    MetaM (Option (Nat × Nat)) := do
  let some ci := env.find? c | return none
  withoutModifyingState do
    try
      withOptions (fun o => o.set `maxHeartbeats (20000 : Nat)) do
        let (mvars, bis, conc) ← forallMetaTelescope ci.type
        if (← isDefEq conc g) then
          let mut ne := 0
          let mut ni := 0
          for i in [0:mvars.size] do
            let m := mvars[i]!
            if !(← m.mvarId!.isAssigned) then
              match bis[i]! with
              | .default => ne := ne + 1
              | .instImplicit => ni := ni + 1
              | _ => pure ()
          return some (ne, ni)
        else
          return none
    catch _ => return none

def probeGoal (env : Environment) (spec : GoalSpec) : MetaM Json := do
  let some ci := env.find? spec.name
    | return Json.mkObj [("n", Json.str (toString spec.name)),
                         ("error", Json.str "not found")]
  let mut legal : Array Json := #[]
  let mut nerr := 0
  let res ← forallTelescopeReducing ci.type fun _ g => do
    let mut acc : Array Json := #[]
    for c in spec.cands do
      match ← tryCandidate env c g with
      | some (ne, ni) =>
        acc := acc.push (Json.mkObj [("c", Json.str (toString c)),
                                     ("ng", toJson ne), ("ni", toJson ni)])
      | none => pure ()
    pure acc
  legal := res
  return Json.mkObj [
    ("n", Json.str (toString spec.name)),
    ("legal", Json.arr legal),
    ("n_cands", toJson spec.cands.size),
    ("n_err", toJson nerr)]

def probe (path : System.FilePath) (inp : System.FilePath)
    (out : System.FilePath) : IO Unit := do
  let pf ← Mathrecord.processFile path mathlibOptions
  let env := pf.env
  IO.println s!"env loaded: {env.header.moduleNames.size} modules"
  let raw ← IO.FS.readFile inp
  let j ← IO.ofExcept (Json.parse raw)
  let specs ← IO.ofExcept (parseInput j)
  IO.println s!"{specs.size} goals to probe"
  let h ← IO.FS.Handle.mk out .write
  let coreCtx : Core.Context := { fileName := pf.fileName, fileMap := default }
  let mut count := 0
  for spec in specs do
    let act : MetaM Json := probeGoal env spec
    let (row, _) ← (act.run' {} {}).toIO coreCtx { env }
    h.putStrLn row.compress
    count := count + 1
    if count % 50 == 0 then
      IO.println s!"  probed {count}/{specs.size}"
      h.flush
  IO.println s!"done: {count} goals"
  h.flush

end Mathrecord.LegalityProbe
