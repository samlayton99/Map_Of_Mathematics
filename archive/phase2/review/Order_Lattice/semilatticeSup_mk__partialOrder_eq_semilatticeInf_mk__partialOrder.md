# semilatticeSup_mk'_partialOrder_eq_semilatticeInf_mk'_partialOrder

*file:* `Mathlib/Order/Lattice.lean` · *style (derived):* rewrite · *proof-term size:* 1254 nodes

## Statement and source  [lean-exact]

```lean
/-- The partial orders from `SemilatticeSup_mk'` and `SemilatticeInf_mk'` agree
if `sup` and `inf` satisfy the lattice absorption laws `sup_inf_self` (`a ⊔ a ⊓ b = a`)
and `inf_sup_self` (`a ⊓ (a ⊔ b) = a`). -/
theorem semilatticeSup_mk'_partialOrder_eq_semilatticeInf_mk'_partialOrder
    {α : Type*} [Max α] [Min α]
    (sup_comm : ∀ a b : α, a ⊔ b = b ⊔ a) (sup_assoc : ∀ a b c : α, a ⊔ b ⊔ c = a ⊔ (b ⊔ c))
    (sup_idem : ∀ a : α, a ⊔ a = a) (inf_comm : ∀ a b : α, a ⊓ b = b ⊓ a)
    (inf_assoc : ∀ a b c : α, a ⊓ b ⊓ c = a ⊓ (b ⊓ c)) (inf_idem : ∀ a : α, a ⊓ a = a)
    (sup_inf_self : ∀ a b : α, a ⊔ a ⊓ b = a) (inf_sup_self : ∀ a b : α, a ⊓ (a ⊔ b) = a) :
    @SemilatticeSup.toPartialOrder _ (SemilatticeSup.mk' sup_comm sup_assoc sup_idem) =
      @SemilatticeInf.toPartialOrder _ (SemilatticeInf.mk' inf_comm inf_assoc inf_idem) :=
  PartialOrder.ext fun a b =>
    show a ⊔ b = b ↔ b ⊓ a = a from
      ⟨fun h => by rw [← h, inf_comm, inf_sup_self], fun h => by rw [← h, sup_comm, sup_inf_self]⟩
```

Exact proof reference: record decl `d467` in `studies/Order_Lattice.study.json` (type `x29879`, value `x30056`).

## P2 — support set (body)  [deterministic-derived]

**Domain (7):** `Max`, `Min`, `Eq`, `PartialOrder.ext`, `SemilatticeSup.mk'`, `SemilatticeInf.mk'`, `Iff`

**Classified infrastructure (10):** `Max.max` (structure-projection), `Min.min` (structure-projection), `SemilatticeSup.toPartialOrder` (structure-projection,typeclass-instance), `SemilatticeInf.toPartialOrder` (structure-projection,typeclass-instance), `Iff.intro` (logic-core,logic-core-ctor), `Eq.mpr` (eq-machinery), `id` (eq-machinery), `congrArg` (eq-machinery), `Eq.symm` (eq-machinery), `Eq.refl` (eq-machinery)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `Max` (1 args) : <sort>
- `Min` (1 args) : <sort>
- `Eq` (3 args) : <sort>
  - `Max.max` (4 args) : <local>
  - `Max.max` (4 args) : <local>
- `Eq` (3 args) : <sort>
  - `Max.max` (4 args) : <local>
    - `Max.max` (4 args) : <local>
  - `Max.max` (4 args) : <local>
    - `Max.max` (4 args) : <local>
- `Eq` (3 args) : <sort>
  - `Max.max` (4 args) : <local>
- `Eq` (3 args) : <sort>
  - `Min.min` (4 args) : <local>
  - `Min.min` (4 args) : <local>
- `Eq` (3 args) : <sort>
  - `Min.min` (4 args) : <local>
    - `Min.min` (4 args) : <local>
  - `Min.min` (4 args) : <local>
    - `Min.min` (4 args) : <local>
- `Eq` (3 args) : <sort>
  - `Min.min` (4 args) : <local>
- `Eq` (3 args) : <sort>
  - `Max.max` (4 args) : <local>
    - `Min.min` (4 args) : <local>
- `Eq` (3 args) : <sort>
  - `Min.min` (4 args) : <local>
    - `Max.max` (4 args) : <local>
- `PartialOrder.ext` (4 args) : Eq [Prop]
  - `SemilatticeSup.toPartialOrder` (2 args) : PartialOrder
  ... (161 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `PartialOrder.ext` (4 args) : Eq (depth 0)

## P5 — source-level use events  [observed]

- `rw` → (no named attribution) — `rw [← h, inf_comm, inf_sup_self]`
- `rw` → (no named attribution) — `rw [← h, sup_comm, sup_inf_self]`

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `Max` — inductive, module `Init.Prelude`
- `Min` — inductive, module `Init.Prelude`
- `Eq` — inductive, module `Init.Prelude`
- `PartialOrder.ext` — axiom, module `Mathlib.Order.Basic`
- `SemilatticeSup.mk'` — def, module `Lattice`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
