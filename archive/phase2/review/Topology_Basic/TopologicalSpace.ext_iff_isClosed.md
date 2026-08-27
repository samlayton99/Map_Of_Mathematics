# TopologicalSpace.ext_iff_isClosed

*file:* `Mathlib/Topology/Basic.lean` · *style (derived):* automation · *proof-term size:* 1513 nodes

## Statement and source  [lean-exact]

```lean
theorem TopologicalSpace.ext_iff_isClosed {X} {t₁ t₂ : TopologicalSpace X} :
    t₁ = t₂ ↔ ∀ s, IsClosed[t₁] s ↔ IsClosed[t₂] s := by
  rw [TopologicalSpace.ext_iff, compl_surjective.forall]
  simp only [@isOpen_compl_iff _ _ t₁, @isOpen_compl_iff _ _ t₂]
```

Exact proof reference: record decl `d26` in `studies/Topology_Basic.study.json` (type `x1830`, value `x2001`).

## P2 — support set (body)  [deterministic-derived]

**Domain (15):** `TopologicalSpace`, `Iff`, `Eq`, `Set`, `IsClosed`, `IsOpen`, `TopologicalSpace.ext_iff`, `Function.Surjective.forall`, `compl_surjective`, `of_eq_true`, `True`, `congrFun'`, `forall_congr`, `isOpen_compl_iff`, `iff_self`

**Classified infrastructure (10):** `Eq.mpr` (eq-machinery), `id` (eq-machinery), `congrArg` (eq-machinery), `propext` (eq-machinery), `Compl.compl` (structure-projection), `BooleanAlgebra.toCompl` (structure-projection,typeclass-instance), `Set.instBooleanAlgebra` (typeclass-instance), `Eq.trans` (eq-machinery), `congr` (eq-machinery), `Set.instCompl` (typeclass-instance)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `TopologicalSpace` (1 args) : <sort>
- `TopologicalSpace` (1 args) : <sort>
- `Eq.mpr` (4 args) : Iff [Prop]
  - `Iff` (2 args) : <sort>
    - `Eq` (3 args) : <sort>
      - `TopologicalSpace` (1 args) : <sort>
    - `Set` (1 args) : <sort>
    - `Iff` (2 args) : <sort>
      - `IsClosed` (3 args) : <sort>
      - `IsClosed` (3 args) : <sort>
  - `Iff` (2 args) : <sort>
    - `Set` (1 args) : <sort>
    - `Iff` (2 args) : <sort>
      - `IsOpen` (3 args) : <sort>
      - `IsOpen` (3 args) : <sort>
    - `Set` (1 args) : <sort>
    - `Iff` (2 args) : <sort>
      - `IsClosed` (3 args) : <sort>
      - `IsClosed` (3 args) : <sort>
  - `id` (2 args) : Eq [Prop]
    - `Eq` (3 args) : <sort>
      - `Iff` (2 args) : <sort>
        - `Eq` (3 args) : <sort>
          - `TopologicalSpace` (1 args) : <sort>
        - `Set` (1 args) : <sort>
        - `Iff` (2 args) : <sort>
          - `IsClosed` (3 args) : <sort>
          - `IsClosed` (3 args) : <sort>
      - `Iff` (2 args) : <sort>
        - `Set` (1 args) : <sort>
  ... (339 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `TopologicalSpace.ext_iff` (3 args) : Iff (depth 4)
- `Function.Surjective.forall` (5 args) : Iff (depth 5)
- `compl_surjective` (2 args) : Function.Surjective (depth 6)
- `of_eq_true` (2 args) : Iff (depth 2)
- `congrFun'` (6 args) : Eq (depth 4)
- `forall_congr` (4 args) : Eq (depth 6)
- `isOpen_compl_iff` (3 args) : Iff (depth 10)
- `isOpen_compl_iff` (3 args) : Iff (depth 9)
- `iff_self` (1 args) : Eq (depth 4)

## P5 — source-level use events  [observed]

- `rewrite` → `TopologicalSpace.ext_iff`, `Function.Surjective.forall` — `rewrite  [ TopologicalSpace.ext_iff, compl_surjective.forall ]`
- `simp` → `isOpen_compl_iff`, `isOpen_compl_iff` — `simp only [@isOpen_compl_iff _ _ t₁, @isOpen_compl_iff _ _ t₂]`

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `TopologicalSpace` — inductive, module `Mathlib.Topology.Defs.Basic`
- `Iff` — inductive, module `Init.Core`
- `Eq` — inductive, module `Init.Prelude`
- `Set` — def, module `Mathlib.Data.Set.Defs`
- `IsClosed` — inductive, module `Mathlib.Topology.Defs.Basic`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
