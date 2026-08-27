# isOpen_iff_of_cover

*file:* `Mathlib/Topology/Basic.lean` · *style (derived):* rewrite · *proof-term size:* 853 nodes

## Statement and source  [lean-exact]

```lean
lemma isOpen_iff_of_cover {f : α → Set X} (ho : ∀ i, IsOpen (f i)) (hU : (⋃ i, f i) = univ) :
    IsOpen s ↔ ∀ i, IsOpen (f i ∩ s) := by
  refine ⟨fun h i ↦ (ho i).inter h, fun h ↦ ?_⟩
  rw [← s.inter_univ, inter_comm, ← hU, iUnion_inter]
  exact isOpen_iUnion fun i ↦ h i
```

Exact proof reference: record decl `d61` in `studies/Topology_Basic.study.json` (type `x4063`, value `x4186`).

## P2 — support set (body)  [deterministic-derived]

**Domain (11):** `Set`, `TopologicalSpace`, `IsOpen`, `Eq`, `Set.iUnion`, `Set.univ`, `IsOpen.inter`, `Set.inter_univ`, `Set.inter_comm`, `Set.iUnion_inter`, `isOpen_iUnion`

**Classified infrastructure (7):** `Iff.intro` (logic-core,logic-core-ctor), `Inter.inter` (structure-projection), `Set.instInter` (typeclass-instance), `Eq.mpr` (eq-machinery), `id` (eq-machinery), `congrArg` (eq-machinery), `Eq.symm` (eq-machinery)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `Set` (1 args) : <sort>
- `TopologicalSpace` (1 args) : <sort>
- `Set` (1 args) : <sort>
- `IsOpen` (3 args) : <sort>
- `Eq` (3 args) : <sort>
  - `Set` (1 args) : <sort>
  - `Set.iUnion` (3 args) : Set
  - `Set.univ` (1 args) : Set
- `Iff.intro` (4 args) : Iff [Prop]
  - `IsOpen` (3 args) : <sort>
  - `IsOpen` (3 args) : <sort>
    - `Inter.inter` (4 args) : Set
      - `Set` (1 args) : <sort>
      - `Set.instInter` (1 args) : Inter
  - `IsOpen` (3 args) : <sort>
  - `IsOpen.inter` (6 args) : IsOpen [Prop]
  - `IsOpen` (3 args) : <sort>
    - `Inter.inter` (4 args) : Set
      - `Set` (1 args) : <sort>
      - `Set.instInter` (1 args) : Inter
  - `Eq.mpr` (4 args) : IsOpen [Prop]
    - `IsOpen` (3 args) : <sort>
    - `IsOpen` (3 args) : <sort>
      - `Inter.inter` (4 args) : Set
        - `Set` (1 args) : <sort>
        - `Set.instInter` (1 args) : Inter
        - `Set.univ` (1 args) : Set
    - `id` (2 args) : Eq [Prop]
      - `Eq` (3 args) : <sort>
        - `IsOpen` (3 args) : <sort>
  ... (163 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `IsOpen.inter` (6 args) : IsOpen (depth 1)
- `Set.inter_univ` (2 args) : Eq (depth 5)
- `Set.inter_comm` (3 args) : Eq (depth 5)
- `Set.iUnion_inter` (4 args) : Eq (depth 7)
- `isOpen_iUnion` (5 args) : IsOpen (depth 5)

## P5 — source-level use events  [observed]

- `exact` → `isOpen_iUnion` — `exact isOpen_iUnion fun i ↦ h i`
- `refine` → `Iff.intro` — `refine ⟨fun h i ↦ (ho i).inter h, fun h ↦ ?_⟩`
- `rewrite` → `Set.inter_univ`, `Set.inter_comm`, `Set.iUnion_inter` — `rewrite  [ ← s.inter_univ, inter_comm, ← hU, iUnion_inter ]`

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `Set` — def, module `Mathlib.Data.Set.Defs`
- `TopologicalSpace` — inductive, module `Mathlib.Topology.Defs.Basic`
- `IsOpen` — def, module `Mathlib.Topology.Defs.Basic`
- `Eq` — inductive, module `Init.Prelude`
- `Set.iUnion` — def, module `Mathlib.Order.SetNotation`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
