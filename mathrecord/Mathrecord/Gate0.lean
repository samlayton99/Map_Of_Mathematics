import Mathrecord.Frontend

/-! Gate 0 spike driver.

Probes each access point required by the audit:
  A. environment + imports
  B. declarations (kinds, universes, type/value Exprs)
  C. exact Expr + universe structure (no pretty-printing)
  D. dependencies (used constants, type vs value)
  E. source spans / provenance
  F. transparency / reducibility
  G. local proof states from InfoTrees (contexts, binders, lets, mvars, targets)
  H. transition access: observed tactic steps (before/after goal mvars) +
     programmatic execution of one successful and one failing action
  I. reconnecting a stored proof term to the Lean kernel (addDeclCore re-check)
-/

namespace Mathrecord.Gate0

open Lean Elab Meta

def biStr : BinderInfo → String
  | .default => "def" | .implicit => "imp" | .strictImplicit => "simp" | .instImplicit => "inst"

instance : ToString BinderInfo := ⟨biStr⟩

/-- Structural dump of an `Expr`: constructor-level s-expression, no pretty printer. -/
partial def dumpExpr (e : Expr) (depth : Nat := 6) : String :=
  if depth == 0 then "…" else
  let d := depth - 1
  match e with
  | .bvar i          => s!"(bvar {i})"
  | .fvar id         => s!"(fvar {id.name})"
  | .mvar id         => s!"(mvar {id.name})"
  | .sort u          => s!"(sort {dumpLevel u})"
  | .const n us      => s!"(const {n} [{", ".intercalate (us.map dumpLevel)}])"
  | .app f a         => s!"(app {dumpExpr f d} {dumpExpr a d})"
  | .lam n t b bi    => s!"(lam {n} {bi} {dumpExpr t d} {dumpExpr b d})"
  | .forallE n t b bi => s!"(forallE {n} {bi} {dumpExpr t d} {dumpExpr b d})"
  | .letE n t v b nd => s!"(letE {n} nondep={nd} {dumpExpr t d} {dumpExpr v d} {dumpExpr b d})"
  | .lit (.natVal v) => s!"(natLit {v})"
  | .lit (.strVal v) => s!"(strLit {v})"
  | .mdata _ b       => s!"(mdata {dumpExpr b d})"
  | .proj s i b      => s!"(proj {s} {i} {dumpExpr b d})"
where
  dumpLevel : Level → String
    | .zero       => "0"
    | .succ u     => s!"(succ {dumpLevel u})"
    | .max u v    => s!"(max {dumpLevel u} {dumpLevel v})"
    | .imax u v   => s!"(imax {dumpLevel u} {dumpLevel v})"
    | .param n    => s!"(par {n})"
    | .mvar id    => s!"(lmvar {id.name})"

def kindOf : ConstantInfo → String
  | .axiomInfo _  => "axiom"
  | .defnInfo _   => "def"
  | .thmInfo _    => "theorem"
  | .opaqueInfo _ => "opaque"
  | .quotInfo _   => "quot"
  | .inductInfo _ => "inductive"
  | .ctorInfo _   => "constructor"
  | .recInfo _    => "recursor"

/-- Probe B/C/D/E/F for one declaration. Runs in CoreM for env-dependent lookups. -/
def dumpDecl (name : Name) : CoreM Unit := do
  let env ← getEnv
  let some ci := env.find? name | IO.println s!"  !! {name} NOT FOUND"; return
  IO.println s!"\n== decl {name} kind={kindOf ci} levelParams={ci.levelParams}"
  IO.println s!"  module: {env.getModuleIdxFor? name |>.map (fun i => env.header.moduleNames[i.toNat]!) |>.getD env.mainModule}"
  IO.println s!"  type:  {dumpExpr ci.type}"
  IO.println s!"  typeDeps:  {ci.type.getUsedConstants}"
  match ci.value? (allowOpaque := true) with
  | some v =>
    IO.println s!"  value: {dumpExpr v 4}"
    IO.println s!"  valueDeps: {v.getUsedConstants}"
  | none => IO.println "  value: none"
  let red := getReducibilityStatusCore env name
  IO.println s!"  reducibility: {repr red}"
  match ← findDeclarationRanges? name with
  | some r => IO.println s!"  sourceRange: {r.range.pos}-{r.range.endPos}"
  | none => IO.println "  sourceRange: none"

/-- G: collect all TacticInfo nodes with their contexts. -/
partial def collectTacticInfos (t : InfoTree) (ctx? : Option ContextInfo := none) :
    List (ContextInfo × TacticInfo) :=
  match t with
  | .context pctx t => collectTacticInfos t (pctx.mergeIntoOuter? ctx?)
  | .node i cs =>
    let rest := cs.toList.flatMap (collectTacticInfos · ctx?)
    match i, ctx? with
    | .ofTacticInfo ti, some ctx => (ctx, ti) :: rest
    | _, _ => rest
  | .hole _ => []

/-- G: dump one exact local state (context + target) from a metavariable, structurally. -/
def dumpState (mctx : MetavarContext) (g : MVarId) : IO Unit := do
  match mctx.findDecl? g with
  | none => IO.println s!"  goal {g.name}: NO DECL"
  | some md =>
    IO.println s!"  goal mvar={g.name} (userName={md.userName})"
    for ld in md.lctx do
      if !ld.isImplementationDetail then
        match ld with
        | .cdecl idx fv un t bi _ =>
          IO.println s!"    [{idx}] cdecl fv={fv.name} user={un} bi={bi} type={dumpExpr t 4}"
        | .ldecl idx fv un t v nonDep _ =>
          IO.println s!"    [{idx}] ldecl fv={fv.name} user={un} nonDep={nonDep} type={dumpExpr t 3} value={dumpExpr v 3}"
    IO.println s!"    ⊢ target: {dumpExpr md.type 5}"

/-- H2: programmatically run one tactic on a fresh goal; success and failure cases. -/
def transitionSpike : CoreM Unit := do
  IO.println "\n===== H2. programmatic transition spike (Elab.runTactic) ====="
  let env ← getEnv
  -- Build goal `1 + 1 = 2` (syntax-free construction via mkAppM)
  let run : MetaM Unit := do
    let one := mkNatLit 1
    let two := mkNatLit 2
    let lhs ← mkAppM ``HAdd.hAdd #[one, one]
    let goalType ← mkAppM ``Eq #[lhs, two]
    let g ← mkFreshExprMVar goalType .natural `spikeGoal
    let gid := g.mvarId!
    -- successful action
    match Parser.runParserCategory env `tactic "decide" "<spike>" with
    | .error e => IO.println s!"  parse error: {e}"
    | .ok stx =>
      let (goalsAfter, _) ← Elab.runTactic gid stx
      IO.println s!"  SUCCESS action=decide before={gid.name} after={goalsAfter.map (·.name)} (empty = closed)"
    -- failing action on a fresh copy of the same goal
    let g2 ← mkFreshExprMVar goalType .natural `spikeGoal2
    match Parser.runParserCategory env `tactic "exact Nat.zero" "<spike>" with
    | .error e => IO.println s!"  parse error: {e}"
    | .ok stx =>
      try
        let (goalsAfter, _) ← Elab.runTactic g2.mvarId! stx
        IO.println s!"  UNEXPECTED success: {goalsAfter.map (·.name)}"
      catch ex =>
        IO.println s!"  FAILURE captured (exception, state preserved): before={g2.mvarId!.name}"
        IO.println s!"    diagnostic (display-only): {← ex.toMessageData.toString}"
  run.run' -- MetaM → CoreM

/-- I: reconnect a stored proof term to the kernel: re-add it under a fresh name. -/
def kernelRecheck (name : Name) : CoreM Unit := do
  IO.println "\n===== I. kernel re-check of stored proof term ====="
  let env ← getEnv
  let some ci := env.find? name | IO.println "  decl not found"; return
  let some v := ci.value? (allowOpaque := true) | IO.println "  no value"; return
  let fresh := name.appendAfter "_recheck"
  let decl := Declaration.thmDecl { name := fresh, levelParams := ci.levelParams, type := ci.type, value := v }
  match env.addDeclCore 0 1024 decl none with
  | .ok _ => IO.println s!"  KERNEL OK: {name} value re-checked as {fresh}"
  | .error e =>
    IO.println s!"  KERNEL REJECTED: {← (e.toMessageData {}).toString}"
  -- negative control: swap in a wrong type; kernel must reject
  let bogusName := name.appendAfter "_bogus"
  let bogus := Declaration.thmDecl
    { name := bogusName, levelParams := ci.levelParams, type := mkConst ``False, value := v }
  match env.addDeclCore 0 1024 bogus none with
  | .ok _ => IO.println "  !! negative control FAILED: kernel accepted bogus decl"
  | .error _ => IO.println "  negative control OK: kernel rejected mistyped decl"

unsafe def main (args : List String) : IO Unit := do
  initSearchPath (← findSysroot)
  enableInitializersExecution
  let dir : System.FilePath := args.head? |>.getD "spikes"
  let onlyFail := args.contains "--only-fail"
  if onlyFail then
    let pff ← Mathrecord.processFile (dir / "FailingProof.lean")
    IO.println "===== FailingProof processed FIRST in this process ====="
    for m in pff.messages.toList do
      let sev := match m.severity with
        | .error => "error" | .warning => "warning" | .information => "info"
      IO.println s!"  [{sev}] {m.pos}: {(← m.data.toString).take 120}"
    let tacFail := pff.trees.flatMap collectTacticInfos
    IO.println s!"  TacticInfo nodes: {tacFail.length}"
    for (_ctx, ti) in tacFail.take 8 do
      IO.println s!"  step kind={ti.stx.getKind} before={ti.goalsBefore.map (·.name)} after={ti.goalsAfter.map (·.name)}"
    return
  let pf ← Mathrecord.processFile (dir / "SampleProofs.lean")

  IO.println "===== A. environment ====="
  IO.println s!"lean version: {Lean.versionString} githash: {Lean.githash}"
  IO.println s!"mainModule: {pf.env.mainModule}"
  IO.println s!"direct imports: {pf.env.header.imports.map (·.module)}"
  IO.println s!"module count: {pf.env.header.moduleNames.size}"
  IO.println s!"errors in file: {(← pf.messages.toList.filterM (fun m => pure (m.severity == .error))).length}"

  let runCore {α} (act : CoreM α) : IO α := do
    let coreCtx : Core.Context := { fileName := pf.fileName, fileMap := default,
                                    options := {}, initHeartbeats := 0 }
    let (a, _) ← (act.toIO coreCtx { env := pf.env })
    return a

  IO.println "\n===== B–F. declarations ====="
  runCore do
    for n in [`Gate0Spike.double, `Gate0Spike.double_eq_two_mul,
              `Gate0Spike.exists_gt, `Gate0Spike.add_comm_spike] do
      dumpDecl n

  IO.println "\n===== G. local proof states (from InfoTrees, exact) ====="
  let tacInfos := pf.trees.flatMap collectTacticInfos
  IO.println s!"TacticInfo nodes found: {tacInfos.length}"
  -- Dump the first state of the `exists_gt` proof (has a local let + mvar target)
  for (_ctx, ti) in tacInfos do
    if ti.stx.getKind == `Lean.Parser.Tactic.refine then
      IO.println s!"\n  -- state BEFORE `refine ⟨m, ?_⟩` (inside exists_gt):"
      for g in ti.goalsBefore do
        dumpState ti.mctxBefore g
      IO.println s!"  -- goals after: {ti.goalsAfter.map (·.name)}"

  IO.println "\n===== H1. observed transitions (InfoTree tactic steps) ====="
  for (_ctx, ti) in tacInfos.take 12 do
    IO.println s!"  step kind={ti.stx.getKind} before={ti.goalsBefore.map (·.name)} after={ti.goalsAfter.map (·.name)}"

  runCore transitionSpike
  runCore (kernelRecheck `Gate0Spike.double_eq_two_mul)

  -- failing file: observe error capture + partial states
  IO.println "\n===== H3. failing action in a source file ====="
  let pff ← Mathrecord.processFile (dir / "FailingProof.lean")
  for m in pff.messages.toList do
    if m.severity == .error then
      IO.println s!"  error at {m.pos}: {(← m.data.toString).take 120}"
  let tacFail := pff.trees.flatMap collectTacticInfos
  IO.println s!"  TacticInfo nodes still recorded in failing file: {tacFail.length}"
  for (_ctx, ti) in tacFail.take 6 do
    IO.println s!"  step kind={ti.stx.getKind} before={ti.goalsBefore.map (·.name)} after={ti.goalsAfter.map (·.name)}"

  IO.println "\nGate 0 spike complete."

end Mathrecord.Gate0

unsafe def main := Mathrecord.Gate0.main
