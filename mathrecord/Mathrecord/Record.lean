import Lean

/-! Canonical encoding of Lean expressions into the MathRecord expression store.

Canonicalization (documented, see SCHEMA.md):
- `mdata` nodes are stripped recursively before encoding (elaborator annotations,
  not kernel content; matches lean4export's default).
- Bound variables are Lean's native de Bruijn indices.
- Free variables (`FVarId`, unstable `_uniq.N` names) are replaced by `lvar i`,
  the ordinal position of the declaration in the state's ordered local context.
- Metavariables are replaced by `mvar i`, first-occurrence order within a state.
- Binder display names are stored (field `"d"`) but excluded from structural
  identity (`sid`).
- Universe parameters are kept by name in storage; `sid` replaces them by their
  index in the enclosing declaration's `levelParams` when that scope is known.

`sid` is the full canonical name-free encoding string (not a lossy hash), so
structural-identity claims are justified by exact string equality.
-/

namespace Mathrecord

open Lean

/-- Pointer address of an expression, for exact per-call memo keys.
NOTE: Lean's `Expr ==` (and `hash`) ignore binder display names, so
structural keys would collapse nodes that differ only in stored display
names. Pointer keys are exact; they are sound only while the root
expression is alive (per-call / per-scope caches, cleared at boundaries). -/
unsafe def exprPtrUnsafe (e : Expr) : USize := ptrAddrUnsafe e
@[implemented_by exprPtrUnsafe]
opaque exprPtr (e : Expr) : USize

/-- Recursively strip `mdata` (canonicalization step; documented loss of
elaborator annotations only). Sharing-aware: memoized (per call, by pointer)
and identity-preserving (returns the original object when nothing changed),
so DAG-shaped terms stay DAG-shaped instead of exploding into trees. -/
partial def stripMData (e : Expr) : Expr :=
  (go e).run' {}
where
  go (e : Expr) : StateM (Std.HashMap USize Expr) Expr := do
    if let some r := (← get).get? (exprPtr e) then
      return r
    let r ← match e with
      | .mdata _ b => go b
      | .app f a => do
        let f' ← go f; let a' ← go a
        pure (if f' == f && a'== a then e else .app f' a')
      | .lam n t b bi => do
        let t' ← go t; let b' ← go b
        pure (if t'== t && b'== b then e else .lam n t' b' bi)
      | .forallE n t b bi => do
        let t' ← go t; let b' ← go b
        pure (if t'== t && b'== b then e else .forallE n t' b' bi)
      | .letE n t v b nd => do
        let t' ← go t; let v' ← go v; let b' ← go b
        pure (if t'== t && v'== v && b'== b then e else .letE n t' v' b' nd)
      | .proj s i b => do
        let b' ← go b
        pure (if b'== b then e else .proj s i b')
      | _ => pure e
    modify (·.insert (exprPtr e) r)
    return r

def biToString : BinderInfo → String
  | .default => "default" | .implicit => "implicit"
  | .strictImplicit => "strictImplicit" | .instImplicit => "instImplicit"

/-- Errors raised when an expression contains data the record cannot represent
in the current scope (loud failure, never silent omission). -/
inductive EncodeError where
  | fvarInClosedExpr (id : FVarId)
  | mvarInClosedExpr (id : MVarId)
  | levelMVarNotAllowed
  | unknownFVar (id : FVarId)

instance : ToString EncodeError where
  toString
    | .fvarInClosedExpr id => s!"free variable {id.name} in closed expression"
    | .mvarInClosedExpr id => s!"metavariable {id.name} in closed expression"
    | .levelMVarNotAllowed => "level metavariable not allowed in this scope"
    | .unknownFVar id => s!"free variable {id.name} not in the state's local context"

/-- Encoding scope: how to resolve fvars/mvars/level params. -/
structure Scope where
  /-- fvarId → ordinal in the state's ordered local context. `none` = closed expr. -/
  fvarOrd : Option (Std.HashMap FVarId Nat) := none
  /-- allow mvars (states) or fail loudly (declarations). -/
  allowMVars : Bool := false
  /-- levelParams of the enclosing declaration, for sid index mapping. -/
  levelParams : List Name := []

structure EncState where
  keyToId : Std.HashMap String Nat := {}
  nodes   : Array Json := #[]
  /-- mvar → first-occurrence ordinal (reset per state group). -/
  mvarOrd : Std.HashMap MVarId Nat := {}
  lmvarOrd : Std.HashMap LMVarId Nat := {}
  /-- expr pointer → stored id. Shared subterms are encoded once instead of
  re-traversed per occurrence. Pointer-keyed (exact: display names preserved);
  MUST be cleared at scope boundaries (per declaration / per state) — see
  `resetEncScope`. The keyed Expr is stored too, keeping its address alive so
  pointer keys cannot be reused by freed objects. -/
  ememo : Std.HashMap USize (Expr × String) := {}

abbrev EncM := StateT EncState (Except EncodeError)

def exprIdStr (i : Nat) : String := s!"x{i}"

/-- Intern a node; returns its id string. Dedup key is the compressed JSON. -/
def intern (node : Json) : EncM String := do
  let key := node.compress
  let s ← get
  match s.keyToId.get? key with
  | some i => return exprIdStr i
  | none =>
    let i := s.nodes.size
    set { s with keyToId := s.keyToId.insert key i, nodes := s.nodes.push node }
    return exprIdStr i

def mvarOrdinal (id : MVarId) : EncM Nat := do
  let s ← get
  match s.mvarOrd.get? id with
  | some i => return i
  | none =>
    let i := s.mvarOrd.size
    modify fun st => { st with mvarOrd := st.mvarOrd.insert id i }
    return i

def lmvarOrdinal (id : LMVarId) : EncM Nat := do
  let s ← get
  match s.lmvarOrd.get? id with
  | some i => return i
  | none =>
    let i := s.lmvarOrd.size
    modify fun st => { st with lmvarOrd := st.lmvarOrd.insert id i }
    return i

partial def encodeLevel (sc : Scope) : Level → EncM Json
  | .zero => return Json.mkObj [("k", Json.str "zero")]
  | .succ u => do return Json.mkObj [("k", Json.str "succ"), ("u", ← encodeLevel sc u)]
  | .max u v => do
    return Json.mkObj [("k", Json.str "max"), ("u", ← encodeLevel sc u), ("v", ← encodeLevel sc v)]
  | .imax u v => do
    return Json.mkObj [("k", Json.str "imax"), ("u", ← encodeLevel sc u), ("v", ← encodeLevel sc v)]
  | .param n => return Json.mkObj [("k", Json.str "param"), ("n", Json.str (toString n))]
  | .mvar id => do
    if !sc.allowMVars then throw .levelMVarNotAllowed
    return Json.mkObj [("k", Json.str "lmvar"), ("i", toJson (← lmvarOrdinal id))]

/-- Clear per-scope encoder caches. Call at every scope boundary (new
declaration or new state): fvar/mvar ordinals change there, and pointer
keys must not outlive their expressions. -/
def resetEncScope : EncM Unit :=
  modify fun s => { s with mvarOrd := {}, lmvarOrd := {}, ememo := {} }

/-- Encode an expression (post `stripMData`) into the store; returns root id.
Pointer-memoized within the current scope, so DAG-shared subterms are
traversed once instead of once per occurrence. -/
partial def encodeExpr (sc : Scope) (e : Expr) : EncM String := do
  if let some (_, r) := (← get).ememo.get? (exprPtr e) then
    return r
  let r ← core e
  modify fun s => { s with ememo := s.ememo.insert (exprPtr e) (e, r) }
  return r
where core (e : Expr) : EncM String := do
  match e with
  | .bvar i => intern <| Json.mkObj [("k", Json.str "bvar"), ("i", toJson i)]
  | .fvar id =>
    match sc.fvarOrd with
    | none => throw (.fvarInClosedExpr id)
    | some m =>
      match m.get? id with
      | some i => intern <| Json.mkObj [("k", Json.str "lvar"), ("i", toJson i)]
      | none => throw (.unknownFVar id)
  | .mvar id =>
    if !sc.allowMVars then throw (.mvarInClosedExpr id)
    intern <| Json.mkObj [("k", Json.str "mvar"), ("i", toJson (← mvarOrdinal id))]
  | .sort u => do intern <| Json.mkObj [("k", Json.str "sort"), ("u", ← encodeLevel sc u)]
  | .const n us => do
    let usj ← us.mapM (encodeLevel sc)
    intern <| Json.mkObj [("k", Json.str "const"), ("n", Json.str (toString n)),
      ("us", Json.arr usj.toArray)]
  | .app f a => do
    intern <| Json.mkObj [("k", Json.str "app"),
      ("f", Json.str (← encodeExpr sc f)), ("a", Json.str (← encodeExpr sc a))]
  | .lam n t b bi => do
    intern <| Json.mkObj [("k", Json.str "lam"), ("d", Json.str (toString n)),
      ("bi", Json.str (biToString bi)),
      ("t", Json.str (← encodeExpr sc t)), ("b", Json.str (← encodeExpr sc b))]
  | .forallE n t b bi => do
    intern <| Json.mkObj [("k", Json.str "pi"), ("d", Json.str (toString n)),
      ("bi", Json.str (biToString bi)),
      ("t", Json.str (← encodeExpr sc t)), ("b", Json.str (← encodeExpr sc b))]
  | .letE n t v b nd => do
    intern <| Json.mkObj [("k", Json.str "let"), ("d", Json.str (toString n)),
      ("nd", Json.bool nd),
      ("t", Json.str (← encodeExpr sc t)), ("v", Json.str (← encodeExpr sc v)),
      ("b", Json.str (← encodeExpr sc b))]
  | .lit (.natVal v) =>
    intern <| Json.mkObj [("k", Json.str "lit"), ("lt", Json.str "nat"), ("v", Json.str (toString v))]
  | .lit (.strVal v) =>
    intern <| Json.mkObj [("k", Json.str "lit"), ("lt", Json.str "str"), ("v", Json.str v)]
  | .mdata _ b => encodeExpr sc b  -- pre-stripped; defensive transparency
  | .proj s i b => do
    intern <| Json.mkObj [("k", Json.str "proj"), ("s", Json.str (toString s)),
      ("i", toJson i), ("b", Json.str (← encodeExpr sc b))]

/-- Canonical name-free level identity string. -/
partial def sidLevel (sc : Scope) (lmvarOrd : Std.HashMap LMVarId Nat) :
    Level → Except EncodeError String
  | .zero => pure "0"
  | .succ u => do pure s!"S{← sidLevel sc lmvarOrd u}"
  | .max u v => do pure s!"M({← sidLevel sc lmvarOrd u},{← sidLevel sc lmvarOrd v})"
  | .imax u v => do pure s!"I({← sidLevel sc lmvarOrd u},{← sidLevel sc lmvarOrd v})"
  | .param n =>
    match sc.levelParams.idxOf? n with
    | some i => pure s!"p{i}"
    | none => pure s!"pn:{n}"   -- state scope: param names kept (documented)
  | .mvar id =>
    match lmvarOrd.get? id with
    | some i => pure s!"lm{i}"
    | none => throw .levelMVarNotAllowed

/-- Canonical name-free structural identity string. Exact, not a hash.
Memoized on subterms free of fvars/mvars/level-params (sid IS scope-dependent
for those), so DAG-shared subterms are rendered once per top-level call. -/
partial def sidOf (sc : Scope) (mvarOrd : Std.HashMap MVarId Nat)
    (lmvarOrd : Std.HashMap LMVarId Nat) (e : Expr) : Except EncodeError String :=
  (go e).run' {}
where
  go (e : Expr) : StateT (Std.HashMap Expr String) (Except EncodeError) String := do
    let cacheable := !e.hasFVar && !e.hasExprMVar && !e.hasLevelMVar && !e.hasLevelParam
    if cacheable then
      if let some r := (← get).get? e then
        return r
    let r : String ← match e with
      | .bvar i => pure s!"b{i}"
      | .fvar id =>
        match sc.fvarOrd with
        | none => throw (.fvarInClosedExpr id)
        | some m => match m.get? id with
          | some i => pure s!"l{i}"
          | none => throw (.unknownFVar id)
      | .mvar id =>
        match mvarOrd.get? id with
        | some i => pure s!"m{i}"
        | none => throw (.mvarInClosedExpr id)
      | .sort u => do pure s!"s({← sidLevel sc lmvarOrd u})"
      | .const n us => do
        let uss ← liftM (us.mapM (sidLevel sc lmvarOrd))
        pure s!"c({n};{",".intercalate uss})"
      | .app f a => do pure s!"a({← go f},{← go a})"
      | .lam _ t b bi => do
        pure s!"L({biToString bi},{← go t},{← go b})"
      | .forallE _ t b bi => do
        pure s!"P({biToString bi},{← go t},{← go b})"
      | .letE _ t v b nd => do
        pure s!"E({nd},{← go t},{← go v},{← go b})"
      | .lit (.natVal v) => pure s!"n{v}"
      | .lit (.strVal v) => pure s!"t{v.quote}"
      | .mdata _ b => go b
      | .proj s i b => do pure s!"j({s},{i},{← go b})"
    if cacheable then
      modify (·.insert e r)
    return r

end Mathrecord
