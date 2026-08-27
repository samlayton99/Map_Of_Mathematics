import Mathrecord.HeadDump
import Mathrecord.Ho

/-! Semantic action compression: certificate grain vs search grain.

A reference proof term mixes two vocabularies: substantive applications
(support lemmas, hypotheses, constructors, eliminators) and MACHINE
CERTIFICATE structure - the congruence/transport skeleton that `rw` and
`simp` compile a single rewrite decision into (`congrArg`/`congr`/
`Eq.mpr`/`Eq.trans`/... chains).

This module:
  1. defines the certificate vocabulary (fixed, core-Lean, listed below);
  2. finds MAXIMAL certificate regions (a certificate-headed node whose
     subtree contains at least one core certificate constant) and extracts
     their BOUNDARY LEAVES - the proof-valued subterms with non-certificate
     heads: the rewrite facts (support lemmas, local hypotheses,
     sub-derivations) the certificate was compiled from;
  3. executes a certificate region as ONE semantic action - `simp only`
     with exactly the extracted leaf facts - through Lean's own simplifier
     (`Simp.mkContext`/`simpGoal`), never reproducing internal nodes;
  4. emits per-theorem SEMANTIC ACTION TRACES (family, parameters, nodes
     covered) for measurement: `mathrecord semtrace <import> <tasks> <out>`.
-/

namespace Mathrecord.Semantic

open Lean Meta Mathrecord

/-- Core certificate vocabulary: the congruence/transport constants that
`rw`/`simp` elaboration emits as proof STRUCTURE (never chosen by a search
policy as a mathematical step). Fixed list, core-Lean constants only. -/
def coreCert : List Name := [
  ``congrArg, ``congrFun, `congrFun', ``congr,
  ``Eq.trans, ``Eq.symm, ``Eq.mpr, ``Eq.mp,
  ``Eq.ndrec, ``Eq.rec, ``Eq.casesOn,
  ``of_eq_true, ``of_eq_false, ``eq_true, ``eq_false,
  ``eq_self, ``iff_self, ``ne_eq, ``not_false_eq_true,
  ``forall_congr, `forall_congr', ``implies_congr,
  ``funext, ``propext, ``Iff.of_eq, ``iff_of_eq,
  ``eq_of_heq, ``heq_of_eq, ``HEq.trans, ``HEq.symm]

/-- Wrapper vocabulary: constants that appear inside certificate chains as
glue but do not by themselves constitute a certificate. -/
def wrapCert : List Name := [``id, ``Eq.refl, ``rfl, ``HEq.refl, ``Iff.refl]

def isCoreCert (n : Name) : Bool := coreCert.contains n
def isCertVocab (n : Name) : Bool := coreCert.contains n || wrapCert.contains n

/-- Does the subtree contain at least one core certificate constant?
(A bare `id x` or `Eq.refl a` is not a certificate region.) -/
def containsCoreCert (e : Expr) : Bool :=
  Option.isSome <| e.find? fun sub =>
    match sub with
    | .const c _ => isCoreCert c
    | _ => false

/-- Is `e` the root of a (maximal, when reached top-down) certificate
region: certificate-headed application containing core certificate
structure? -/
def certRegionRoot (e : Expr) : Bool :=
  match e.consumeMData.getAppFn.consumeMData with
  | .const c _ => isCertVocab c && e.isApp && containsCoreCert e
  | _ => false

/-- A boundary leaf of a certificate region. -/
structure Leaf where
  term  : Expr          -- the fact subterm (possibly head-generalized)
  head  : String        -- const name / "FVAR" / other
  kind  : String        -- "const" | "fvar" | "compound" | "other"
  generalized : Bool    -- term referenced region-bound variables; head kept
  deriving Inhabited

/-- Is a proposition an equality-family statement (after stripping
foralls): `Eq`, `Iff`, `HEq`, or their `= True/False` closures?  These are
the REWRITE FACTS a certificate is compiled from; a certificate-node proof
argument of any other proposition is a CONTINUATION - the proof of the
rewritten goal, which stays a search goal. -/
def isEqFamilyProp (t : Expr) : Bool :=
  match t.getForallBody.consumeMData.getAppFn.consumeMData with
  | .const c _ => c == ``Eq || c == ``Iff || c == ``HEq
  | _ => false

/-- Walk a certificate region: recurse through certificate-headed
applications and lambdas (funext/forall_congr children).  Collects
  - FACT leaves: equality-family proof subterms with non-certificate heads
    (the rewrite lemmas/hypotheses the certificate was compiled from); a
    leaf mentioning a region-bound variable is generalized to its head -
    the shape `simp only [h]` uses;
  - CONTINUATIONS: non-equality proof arguments (`Eq.mpr cert body` - the
    proof of the rewritten goal, which remains a search goal);
  - the count of internal structure nodes.
Data arguments (motives, endpoints) are never collected. -/
partial def regionParts (e : Expr) :
    MetaM (Array Leaf × Array Expr × Nat) := do
  let leaves ← IO.mkRef (#[] : Array Leaf)
  let conts ← IO.mkRef (#[] : Array Expr)
  let nStruct ← IO.mkRef 0
  let rec pushLeaf (a : Expr) (bound : Array FVarId) : MetaM Unit := do
    let fn := a.getAppFn.consumeMData
    let usesBound := bound.any fun f => a.containsFVar f
    let (term, generalized) :=
      if usesBound then (fn, true) else (a, false)
    let (head, kind) := match fn with
      | .const c _ => (toString c, "const")
      | .fvar _ => ("FVAR", "fvar")
      | _ => ("OTHER", "other")
    leaves.modify (·.push { term, head, kind, generalized })
  let rec go (e : Expr) (bound : Array FVarId) : MetaM Unit := do
    let e := e.consumeMData
    match e with
    | .lam .. =>
      lambdaTelescope e fun xs b =>
        go b (bound ++ xs.map (·.fvarId!))
    | .letE nm ty val body _ => do
      let vP ← try Meta.isProp (← inferType val) catch _ => pure false
      if vP then go val bound
      withLetDecl nm ty val fun x => go (body.instantiate1 x) (bound.push x.fvarId!)
    | _ =>
      let fn := e.getAppFn.consumeMData
      let inVocab := match fn with
        | .const c _ => isCertVocab c
        | _ => false
      if inVocab && e.isApp then
        nStruct.modify (· + 1)
        for a in e.getAppArgs do
          let aP ← try Meta.isProp (← inferType a) catch _ => pure false
          if aP then
            let a' := a.consumeMData
            let aFn := a'.getAppFn.consumeMData
            let aCert := match aFn with
              | .const c _ => isCertVocab c
              | _ => false
            if a'.isLambda || (aCert && a'.isApp) then go a' bound
            else
              let aT ← try instantiateMVars (← inferType a') catch _ => pure default
              if isEqFamilyProp aT then pushLeaf a' bound
              else if bound.any (fun f => a'.containsFVar f) then
                -- continuation under region binders: not liftable to a goal
                pushLeaf a' bound
              else conts.modify (·.push a')
      else
        pushLeaf e bound
  go e #[]
  pure (← leaves.get, ← conts.get, ← nStruct.get)

/-- Execute a certificate region as ONE semantic rewrite action: `simp
only` with exactly the FACT leaves (const-headed facts by NAME - the
simplifier re-instantiates them - fvar and instantiated facts as proof
terms).  A goal the simplifier leaves open must match a region
CONTINUATION (the proof of the rewritten goal): it is registered in the
guide and returned as the next guided goal.  The certificate's internal
nodes are never reconstructed. -/
def semSimpAct (guide : IO.Ref (Std.HashMap Name Expr))
    (g : MVarId) (e : Expr)
    (simprocs : Simp.Simprocs) : MetaM (List MVarId) := g.withContext do
  let (leaves, conts, _) ← regionParts e
  if leaves.isEmpty && conts.isEmpty then throwError "sem: empty region"
  let mut thms : SimpTheorems := {}
  let mut i := 0
  for l in leaves do
    let added ← try
      match l.term.consumeMData with
      | .const c _ => do thms ← thms.addConst c; pure true
      | t => do
        if l.generalized then
          match t.getAppFn.consumeMData with
          | .const c _ => do thms ← thms.addConst c; pure true
          | .fvar f => do thms ← thms.add (.fvar f) #[] (mkFVar f); pure true
          | _ => pure false
        else do
          thms ← thms.add (.other (Name.mkSimple s!"semfact{i}")) #[] t
          pure true
    catch _ => pure false
    let _ := added
    i := i + 1
  let ctx ← Simp.mkContext (simpTheorems := #[thms])
              (congrTheorems := ← Meta.getSimpCongrTheorems)
  let (res, _) ← simpGoal g ctx (simprocs := #[simprocs])
  match res with
  | none => pure []
  | some (_, g') => do
    -- the open goal should be a rewritten form owned by a continuation
    let g'T ← instantiateMVars (← g'.getType)
    for c in conts do
      let cT ← try instantiateMVars (← inferType c) catch _ => pure default
      let okC ← try isDefEq g'T cT catch _ => pure false
      if okC then
        guide.modify (·.insert g'.name c)
        return [g']
    try g'.refl; pure []
    catch _ =>
      if ← g'.assumptionCore then pure []
      else throwError "sem simp residual goal ({conts.size} conts unmatched)"

/-- Head-name based family classification for non-certificate nodes. -/
def elimFamily (c : Name) : Bool :=
  let s := c.toString
  s.endsWith ".casesOn" || s.endsWith ".rec" || s.endsWith ".recOn" ||
  s.endsWith ".ndrec" || s.endsWith ".elim" || s.endsWith ".ndrecOn"

/-! ## Semantic trace emission (measurement) -/

structure STCtx where
  env  : Environment
  rows : IO.Ref (Array Json)
  fuel : IO.Ref Nat

/-- Emit the semantic action trace of a reference proof: one row per
search-grain action.  Certificate regions become single `rewrite` rows
carrying their leaf facts and covered-node counts; leaves that are
themselves compound derivations (a proof-typed argument somewhere inside)
are recursed as separate sub-traces (`have` grain). -/
partial def semWalk (ctx : STCtx) (e : Expr) (depth : Nat := 0) : MetaM Unit := do
  if (← ctx.fuel.get) == 0 then return ()
  ctx.fuel.set ((← ctx.fuel.get) - 1)
  let e := e.consumeMData
  let t ← try instantiateMVars (← inferType e) catch _ => return ()
  let isP ← try Meta.isProp t catch _ => pure false
  if !isP then return ()
  let push (fields : List (String × Json)) : MetaM Unit :=
    ctx.rows.modify (·.push (Json.mkObj (("d", toJson depth) :: fields)))
  match e with
  | .lam .. =>
    lambdaTelescope e fun xs body => do
      push [("f", Json.str "intro"), ("n", toJson xs.size)]
      semWalk ctx body (depth + 1)
  | .letE nm ty val body _ => do
    push [("f", Json.str "have")]
    semWalk ctx val (depth + 1)
    withLetDecl nm ty val fun x => semWalk ctx (body.instantiate1 x) (depth + 1)
  | .app .. =>
    let fn := e.getAppFn.consumeMData
    if fn.isLambda then
      semWalk ctx fn (depth + 1)
      for a in e.getAppArgs do semWalk ctx a (depth + 1)
      return ()
    if certRegionRoot e then
      let (leaves, conts, nStruct) ←
        try regionParts e catch _ => pure (#[], #[], 0)
      push [("f", Json.str "rewrite"),
            ("nleaves", toJson leaves.size),
            ("nconts", toJson conts.size),
            ("nstruct", toJson nStruct),
            ("leaves", Json.arr (leaves.map fun l => Json.mkObj [
              ("h", Json.str l.head), ("k", Json.str l.kind),
              ("g", toJson l.generalized)]))]
      -- fact leaves that are themselves derivations: separate sub-traces
      for l in leaves do
        if !l.generalized && l.term.isApp then
          let hasProofArg ← l.term.getAppArgs.anyM fun a =>
            try Meta.isProp (← inferType a) catch _ => pure false
          if hasProofArg then
            semWalk ctx l.term (depth + 1)
      -- continuations are the NEXT semantic goals
      for c in conts do
        semWalk ctx c (depth + 1)
      return ()
    let (family, headStr) := match fn with
      | .const c _ =>
        (if elimFamily c then "cases"
         else match ctx.env.find? c with
           | some (.ctorInfo _) => "constructor"
           | _ => "apply", toString c)
      | .fvar _ => ("apply_hyp", "FVAR")
      | _ => ("apply_other", "OTHER")
    push [("f", Json.str family), ("h", Json.str headStr)]
    for a in e.getAppArgs do semWalk ctx a (depth + 1)
  | .proj _ _ s =>
    push [("f", Json.str "exact_proj")]
    semWalk ctx s (depth + 1)
  | .fvar _ => push [("f", Json.str "exact_hyp")]
  | .const c _ => push [("f", Json.str "exact_const"), ("h", Json.str (toString c))]
  | _ => push [("f", Json.str "exact_other")]

/-- Certificate-grain action count of the SAME term under the SAME
emission conventions as `semWalk`, but descending into certificate
regions node by node - the denominator of the compression ratio. -/
partial def rawCount (e : Expr) : MetaM Nat := do
  let e := e.consumeMData
  let t ← try instantiateMVars (← inferType e) catch _ => return 0
  let isP ← try Meta.isProp t catch _ => pure false
  if !isP then return 0
  match e with
  | .lam .. =>
    lambdaTelescope e fun _ body => do pure (1 + (← rawCount body))
  | .letE nm ty val body _ => do
    let nv ← rawCount val
    let nb ← withLetDecl nm ty val fun x => rawCount (body.instantiate1 x)
    pure (1 + nv + nb)
  | .app .. => do
    let fn := e.getAppFn.consumeMData
    let mut n ← if fn.isLambda then rawCount fn else pure 1
    for a in e.getAppArgs do
      n := n + (← rawCount a)
    pure n
  | .proj _ _ s => do pure (1 + (← rawCount s))
  | _ => pure 1

/-- Target-attached auxiliary unfolding (same criterion as the prover's
`deAux`; duplicated locally to keep module dependencies acyclic). -/
partial def unfoldAux (env : Environment) (selfStr : String) (e : Expr)
    (fuel : Nat := 8) : Expr :=
  if fuel == 0 then e else
  let isAuxName (s : String) : Bool :=
    s.startsWith (selfStr ++ ".") ||
    (s.startsWith "_private." && (s.splitOn ("." ++ selfStr ++ ".")).length > 1)
  let e' := e.replace fun sub =>
    match sub with
    | .const c lvls =>
      if isAuxName c.toString then
        match env.find? c with
        | some ci =>
          match ci.value? (allowOpaque := true) with
          | some v => some (v.instantiateLevelParams ci.levelParams lvls)
          | none => none
        | none => none
      else none
    | _ => none
  if e' == e then e else unfoldAux env selfStr e' (fuel - 1)

/-- CLI driver: semantic action traces for every task theorem. -/
def semtrace (path : System.FilePath) (inp : System.FilePath)
    (out : System.FilePath) : IO Unit := do
  let pf ← Mathrecord.processFile path Mathrecord.Study.mathlibOptions
  let env := pf.env
  IO.println s!"env loaded: {env.header.moduleNames.size} modules"
  let raw ← IO.FS.readFile inp
  let j ← IO.ofExcept (Json.parse raw)
  let ts ← IO.ofExcept ((← IO.ofExcept (j.getObjVal? "goals" <|> j.getObjVal? "tasks")).getArr?)
  IO.println s!"{ts.size} theorems"
  let h ← IO.FS.Handle.mk out .write
  let coreCtx : Core.Context := { fileName := pf.fileName, fileMap := default }
  let mut count := 0
  for tj in ts do
    let nm := ((do (← tj.getObjVal? "n").getStr? :
      Except String String)).toOption.getD ""
    if nm == "" then continue
    let n := String.toName nm
    let act : MetaM Json := do
      let some ci := env.find? n
        | return Json.mkObj [("n", Json.str nm), ("error", Json.str "not found")]
      let some val := ci.value? (allowOpaque := true)
        | return Json.mkObj [("n", Json.str nm), ("error", Json.str "no value")]
      Meta.forallTelescope ci.type fun xs _ => do
        let rows ← IO.mkRef (#[] : Array Json)
        let fuel ← IO.mkRef 2000
        let term := unfoldAux env nm (val.beta xs)
        semWalk { env, rows, fuel } term
        let raw ← try rawCount term catch _ => pure 0
        let rs ← rows.get
        return Json.mkObj [
          ("n", Json.str nm),
          ("n_actions", toJson rs.size),
          ("n_raw", toJson raw),
          ("actions", Json.arr rs)]
    let row ← try
      let (r, _) ← (act.run' {} {}).toIO coreCtx { env }
      pure r
    catch _ => pure (Json.mkObj [("n", Json.str nm), ("error", Json.str "exception")])
    h.putStrLn row.compress
    count := count + 1
    if count % 25 == 0 then
      IO.println s!"  {count}/{ts.size}"
      h.flush
  IO.println s!"done: {count} traces"
  h.flush

end Mathrecord.Semantic
