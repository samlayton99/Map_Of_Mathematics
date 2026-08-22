import Mathrecord.Frontend

/-! Per-declaration ENVIRONMENT FACTS not captured by `depdump`.

`envfacts <namesFile> <envProbe> <out.tsv>` emits one row per requested
name. Every field is an environment/kernel fact recorded by the
elaborator -- no names are parsed, no namespaces inspected, no
docstrings or comments read. Columns (TSV):

  0  name
  1  inst    registered as a typeclass instance (`Meta.isInstance`).
             NOTE this is a property of the DECLARATION; the existing
             lane rule keys off instance-implicit ARGUMENT ROLE, which
             is a property of the citation SITE. Different facts.
  2  red     reducibility: 0 reducible, 1 semireducible, 2 irreducible,
             3 other. `@[reducible]` marks a definition the elaborator
             is expected to unfold -- an abbreviation, i.e. plumbing --
             while `@[irreducible]` marks one meant to be opaque.
  3  simp    member of the default simp set (either as a rewrite rule or
             as a decl-to-unfold). A lemma tagged `@[simp]` is one the
             library expects to fire automatically; a citation of it is
             far more likely to be rewriting machinery than a chosen
             mathematical step.
  4  proj    is a structure/class projection function
  5  cls     ... and its parent structure is a class
  6  rec     inductive type flagged recursive
  7  unsafe  declaration is unsafe/partial
  8  line    1-based source line of the declaration, or -1 when the
             elaborator recorded no range (the same fact `depdump`
             already reduces to the boolean `gen`). Gives within-file
             declaration ORDER, which file-level dates cannot.
  9  levels  number of universe parameters

Emitted for every requested name, including ones absent from the
environment (all fields default, line -1), so the file is positional
and joins cleanly.
-/

namespace Mathrecord.EnvFacts

open Lean Meta

/-- Names in the default simp set: rewrite rules plus decls-to-unfold. -/
def simpNameSet : MetaM (Std.HashSet Name) := do
  let s ← Meta.getSimpTheorems
  let mut out : Std.HashSet Name := {}
  for o in s.lemmaNames.toList do
    match o with
    | .decl d _ _ => out := out.insert d
    | _ => pure ()
  for d in s.toUnfold.toList do
    out := out.insert d
  return out

def redCode (env : Environment) (n : Name) : Nat :=
  match getReducibilityStatusCore env n with
  | .reducible => 0
  | .semireducible => 1
  | .irreducible => 2
  | _ => 3

def envfacts (namesPath : System.FilePath) (envProbe : System.FilePath)
    (out : System.FilePath) : IO Unit := do
  let pf ← Mathrecord.processFile envProbe
  let env := pf.env
  let names := (← IO.FS.readFile namesPath).splitOn "\n" |>.filter (· ≠ "")
  let h ← IO.FS.Handle.mk out .write
  let coreCtx : Core.Context := {
    fileName := "<envfacts>", fileMap := default,
    maxHeartbeats := 400000000, maxRecDepth := 2000 }
  let act : CoreM Unit := do
    let simps ← (simpNameSet).run'
    IO.println s!"default simp set: {simps.size} declarations"
    let mut nInst := 0
    let mut nSimp := 0
    let mut nRed := 0
    let mut nLine := 0
    for nm in names do
      let n := nm.toName
      let some ci := env.find? n
        | h.putStrLn s!"{nm}\t0\t3\t0\t0\t0\t0\t0\t-1\t0"
          continue
      let isInst ← try
          Core.withCurrHeartbeats <| Meta.isInstance n
        catch _ => pure false
      let red := redCode env n
      let isSimp := simps.contains n
      let (isProj, isCls) := match env.getProjectionFnInfo? n with
        | some info => (true, Lean.isClass env info.ctorName.getPrefix)
        | none => (false, false)
      let isRec := match ci with
        | .inductInfo iv => iv.isRec
        | _ => false
      let line ← match ← findDeclarationRanges? n with
        | some r => pure (r.range.pos.line)
        | none => pure 0
      let lineStr := if line == 0 then "-1" else toString line
      if isInst then nInst := nInst + 1
      if isSimp then nSimp := nSimp + 1
      if red == 0 then nRed := nRed + 1
      if line != 0 then nLine := nLine + 1
      h.putStrLn <| String.intercalate "\t" [
        nm,
        if isInst then "1" else "0",
        toString red,
        if isSimp then "1" else "0",
        if isProj then "1" else "0",
        if isCls then "1" else "0",
        if isRec then "1" else "0",
        if ci.isUnsafe then "1" else "0",
        lineStr,
        toString ci.levelParams.length]
    IO.println s!"envfacts: {names.length} names; instances {nInst}; simp {nSimp}; reducible {nRed}; with source line {nLine}"
  let (_, _) ← act.toIO coreCtx { env }
  h.flush
  IO.println s!"envfacts -> {out}"

end Mathrecord.EnvFacts
