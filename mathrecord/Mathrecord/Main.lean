import Mathrecord.Extract
import Mathrecord.Validate
import Mathrecord.Study
import Mathrecord.DepDump
import Mathrecord.Provenance

/-! MathRecord CLI.

  mathrecord extract  <file.lean> <out.json> [--spike]
  mathrecord validate <file.lean> <record.json> (adversarial|failing|none)
  mathrecord alpha    <recordA.json> <recordB.json>
  mathrecord inspect  <record.json> <declName>

One source file per process invocation (see ADR-0001).
-/

namespace Mathrecord.Cli

open Lean Mathrecord Mathrecord.Validate

def printResults (rs : Array CheckResult) : IO UInt32 := do
  let mut failed := 0
  for r in rs do
    let tag := if r.passed then "PASS" else "FAIL"
    IO.println s!"[{tag}] {r.name}  {r.detail}"
    if !r.passed then failed := failed + 1
  return if failed == 0 then 0 else 1

/-- Structural rendering of a stored expression (display names shown, labeled). -/
partial def render (nodes : Std.HashMap String Json) (id : String) (depth : Nat) : String :=
  if depth == 0 then "…" else
  match nodes.get? id with
  | none => s!"<dangling {id}>"
  | some j =>
    let g (k : String) := (getStr j k).toOption.getD "?"
    let d := depth - 1
    match g "k" with
    | "bvar" => s!"(bvar {(j.getObjValAs? Nat "i").toOption.getD 0})"
    | "lvar" => s!"(lvar {(j.getObjValAs? Nat "i").toOption.getD 0})"
    | "mvar" => s!"(mvar {(j.getObjValAs? Nat "i").toOption.getD 0})"
    | "sort" => s!"(sort {(j.getObjVal? "u").toOption.map (·.compress) |>.getD "?"})"
    | "const" => s!"(const {g "n"})"
    | "app" => s!"(app {render nodes (g "f") d} {render nodes (g "a") d})"
    | "lam" => s!"(lam [{g "d"}] {g "bi"} {render nodes (g "t") d} {render nodes (g "b") d})"
    | "pi" => s!"(pi [{g "d"}] {g "bi"} {render nodes (g "t") d} {render nodes (g "b") d})"
    | "let" => s!"(let [{g "d"}] {render nodes (g "t") d} := {render nodes (g "v") d} in {render nodes (g "b") d})"
    | "lit" => s!"(lit {g "lt"} {g "v"})"
    | "proj" => s!"(proj {g "s"} {(j.getObjValAs? Nat "i").toOption.getD 0} {render nodes (g "b") d})"
    | k => s!"<bad kind {k}>"

/-- Collect constant references from a stored expression (derived data). -/
partial def storedDeps (nodes : Std.HashMap String Json) (id : String)
    (acc : Array String := #[]) : Array String :=
  match nodes.get? id with
  | none => acc
  | some j =>
    let g (k : String) := (getStr j k).toOption.getD ""
    match g "k" with
    | "const" =>
      let n := g "n"
      if acc.contains n then acc else acc.push n
    | "app" => storedDeps nodes (g "a") (storedDeps nodes (g "f") acc)
    | "lam" | "pi" => storedDeps nodes (g "b") (storedDeps nodes (g "t") acc)
    | "let" => storedDeps nodes (g "b") (storedDeps nodes (g "v") (storedDeps nodes (g "t") acc))
    | "proj" => storedDeps nodes (g "b") acc
    | _ => acc

def inspect (recordPath : System.FilePath) (declName : String) : IO UInt32 := do
  let rec ← loadRecord recordPath
  let some d := rec.decls.find? (fun d => (getStr d "name").toOption == some declName)
    | IO.eprintln s!"declaration {declName} not found in record"; return 1
  let g (k : String) := (getStr d k).toOption.getD "?"
  IO.println s!"declaration : {g "name"}"
  IO.println s!"kind        : {g "kind"}  levelParams: {(d.getObjValAs? (List String) "levelParams").toOption.getD []}"
  IO.println s!"module      : {g "module"}  reducibility: {g "reducibility"}"
  IO.println s!"span        : {(d.getObjVal? "span").toOption.map (·.compress) |>.getD "?"}"
  IO.println s!"trust       : {g "trust"}"
  IO.println ""
  IO.println s!"exact statement (structural; [names] are display-only):"
  IO.println s!"  {render rec.nodes (g "type") 8}"
  IO.println ""
  match getStr d "value" with
  | .ok vid =>
    IO.println s!"body/proof term (structural, depth-limited):"
    IO.println s!"  {render rec.nodes vid 5}"
    IO.println ""
    IO.println s!"direct references (value): {storedDeps rec.nodes vid}"
  | .error _ => IO.println "body/proof term: none"
  IO.println s!"direct references (type):  {storedDeps rec.nodes (g "type")}"
  IO.println ""
  let assoc := rec.states.filter (fun st => (getStr st "decl").toOption == some declName)
  match assoc[0]? with
  | none => IO.println "local states: none recorded for this declaration"
  | some st =>
    IO.println s!"one local state ({(getStr st "id").toOption.getD "?"} of {assoc.size} recorded):"
    for entry in (getArr st "ctx").toOption.getD #[] do
      let eg (k : String) := (getStr entry k).toOption.getD "?"
      let v := match getStr entry "v" with
        | .ok vid => s!" := {render rec.nodes vid 4}"
        | .error _ => ""
      IO.println s!"  [{(entry.getObjValAs? Nat "i").toOption.getD 0}] [{eg "d"}] {eg "bi"} : {render rec.nodes (eg "t") 5}{v}"
    IO.println s!"  ⊢ {render rec.nodes ((getStr st "target").toOption.getD "?") 6}"
  return 0

def alpha (pathA pathB : System.FilePath) : IO UInt32 := do
  let ra ← loadRecord pathA
  let rb ← loadRecord pathB
  let mut results : Array CheckResult := #[]
  -- declarations paired by name
  let mut declOk := 0
  let mut declFail : List String := []
  let mut paired := 0
  for da in ra.decls do
    let name := (getStr da "name").toOption.getD "?"
    match rb.decls.find? (fun db => (getStr db "name").toOption == some name) with
    | none => declFail := s!"{name}(unpaired)" :: declFail
    | some db =>
      paired := paired + 1
      let ta := (getStr da "typeSid").toOption
      let tb := (getStr db "typeSid").toOption
      let va := (getStr da "valueSid").toOption
      let vb := (getStr db "valueSid").toOption
      if ta == tb && va == vb then declOk := declOk + 1
      else
        let what := (if ta != tb then "type " else "") ++ (if va != vb then "value" else "")
        declFail := s!"{name}({what})" :: declFail
  results := results.push <| check "alpha:decl-sids-invariant-under-renaming"
    declFail.isEmpty s!"paired={paired} ok={declOk} fail={declFail}"
  -- states paired by extraction order
  let mut stOk := 0
  let mut stFail : List String := []
  if ra.states.size == rb.states.size then
    for i in [0:ra.states.size] do
      let sa := (getStr ra.states[i]! "sid").toOption
      let sb := (getStr rb.states[i]! "sid").toOption
      if sa == sb then stOk := stOk + 1
      else stFail := s!"state#{i}" :: stFail
    results := results.push <| check "alpha:state-sids-invariant-under-renaming"
      stFail.isEmpty s!"paired={ra.states.size} ok={stOk} fail={stFail}"
  else
    results := results.push <| check "alpha:state-sids-invariant-under-renaming"
      false s!"state count differs: {ra.states.size} vs {rb.states.size}"
  printResults results

unsafe def main (args : List String) : IO UInt32 := do
  Lean.initSearchPath (← Lean.findSysroot)
  Lean.enableInitializersExecution
  match args with
  | ["extract", file, out] | ["extract", file, out, "--spike"] => do
    let spike := args.contains "--spike"
    let json ← Extract.extractFile file spike
    IO.FS.writeFile out (json.pretty ++ "\n")
    IO.println s!"extracted {file} -> {out}"
    return 0
  | ["validate", file, recordPath, mode] => do
    let pf ← Mathrecord.processFile file
    let rec ← loadRecord recordPath
    let mut results ← validateDecls pf.env rec
    results := results ++ (← validateStates pf.env rec)
    if mode == "adversarial" then
      results := results ++ (← validateCorpusAssertions rec)
    if mode == "failing" then
      results := results ++ (← validateFailingAssertions rec)
    printResults results
  | ["study", file, out] | ["study", file, out, "--mathlib"] => do
    let opts := if args.contains "--mathlib" then Study.mathlibOptions else {}
    let json ← Study.studyFile file opts
    IO.FS.writeFile out (json.pretty ++ "\n")
    IO.println s!"studied {file} -> {out}"
    return 0
  | ["depdump", file, out] => do
    Mathrecord.DepDump.depDump file out
    return 0
  | ["provenance", file, out] => do
    Mathrecord.Provenance.provenance file out
    return 0
  | ["alpha", a, b] => alpha a b
  | ["inspect", recordPath, declName] => inspect recordPath declName
  | _ => do
    IO.eprintln "usage: mathrecord (extract <file> <out.json> [--spike] | validate <file> <record.json> <adversarial|failing|none> | alpha <a.json> <b.json> | inspect <record.json> <decl>)"
    return 2

end Mathrecord.Cli

unsafe def main := Mathrecord.Cli.main
