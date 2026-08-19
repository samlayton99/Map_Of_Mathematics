# limUnder_of_not_tendsto

*file:* `Mathlib/Topology/Basic.lean` · *style (derived):* automation · *proof-term size:* 5437 nodes

## Statement and source  [lean-exact]

```lean
theorem limUnder_of_not_tendsto [hX : Nonempty X] {f : Filter α} {g : α → X}
    (h : ¬ ∃ x, Tendsto g f (𝓝 x)) :
    limUnder f g = Classical.choice hX := by
  simp_rw [Tendsto] at h
  simp_rw [limUnder, lim, Classical.epsilon, Classical.strongIndefiniteDescription, dif_neg h]
```

Exact proof reference: record decl `d64` in `studies/Topology_Basic.study.json` (type `x4322`, value `x4651`).

## P2 — support set (body)  [deterministic-derived]

**Domain (25):** `TopologicalSpace`, `Nonempty`, `Filter`, `Not`, `Exists`, `Filter.Tendsto`, `nhds`, `Eq`, `Filter.limUnder`, `Classical.choice`, `Filter.lim`, `Filter.map`, `Classical.epsilon`, `Classical.strongIndefiniteDescription`, `of_eq_true`, `dite`, `Subtype`, `Classical.propDecidable`, `Subtype.mk`, `Classical.indefiniteDescription`, `True`, `congrFun'`, `Decidable`, `dif_neg`, `eq_self`

**Classified infrastructure (10):** `id` (eq-machinery), `LE.le` (structure-projection), `Preorder.toLE` (structure-projection,typeclass-instance), `PartialOrder.toPreorder` (structure-projection,typeclass-instance), `Filter.instPartialOrder` (typeclass-instance), `Subtype.val` (structure-projection), `Classical.strongIndefiniteDescription._proof_1` (internal-detail), `Classical.strongIndefiniteDescription._proof_2` (internal-detail), `Eq.trans` (eq-machinery), `congrArg` (eq-machinery)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `TopologicalSpace` (1 args) : <sort>
- `Nonempty` (1 args) : <sort>
- `Filter` (1 args) : <sort>
- `Not` (1 args) : <sort>
  - `Exists` (2 args) : <sort>
    - `Filter.Tendsto` (5 args) : <sort>
      - `nhds` (3 args) : Filter
- `id` (2 args) : Eq [Prop]
  - `Eq` (3 args) : <sort>
    - `Filter.limUnder` (6 args) : <local>
    - `Classical.choice` (2 args) : <local>
  - `id` (2 args) : Eq [Prop]
    - `Eq` (3 args) : <sort>
      - `Filter.lim` (4 args) : <local>
        - `Filter.map` (4 args) : Filter
      - `Classical.choice` (2 args) : <local>
    - `id` (2 args) : Eq [Prop]
      - `Eq` (3 args) : <sort>
        - `Classical.epsilon` (3 args) : <local>
          - `LE.le` (4 args) : <sort>
            - `Filter` (1 args) : <sort>
            - `Preorder.toLE` (2 args) : LE
              - `Filter` (1 args) : <sort>
              - `PartialOrder.toPreorder` (2 args) : Preorder
                - `Filter` (1 args) : <sort>
                - `Filter.instPartialOrder` (1 args) : PartialOrder
            - `Filter.map` (4 args) : Filter
            - `nhds` (3 args) : Filter
        - `Classical.choice` (2 args) : <local>
      - `id` (2 args) : Eq [Prop]
  ... (1162 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `of_eq_true` (2 args) : Eq (depth 4)
- `congrFun'` (6 args) : Eq (depth 6)
- `dif_neg` (6 args) : Eq (depth 9)
- `eq_self` (2 args) : Eq (depth 6)

## P5 — source-level use events  [observed]

- `simp` → `Filter.Tendsto`, `Filter.Tendsto` — `simp  only  [ Tendsto ] at h`
- `simp` → `Filter.limUnder`, `Filter.limUnder` — `simp  only  [ limUnder ]`
- `simp` → `Lean.Meta.Simp.Config.failIfUnchanged`, `Bool.false` — `simp  (  failIfUnchanged  :=  false  )  only at h`
- `simp` → `Filter.lim`, `Filter.lim` — `simp  only  [ lim ]`
- `simp` → `Classical.epsilon`, `Classical.epsilon` — `simp  only  [ Classical.epsilon ]`
- `simp` → `Classical.strongIndefiniteDescription`, `Classical.strongIndefiniteDescription` — `simp  only  [ Classical.strongIndefiniteDescription ]`
- `simp` → `dif_neg` — `simp  only  [ dif_neg h ]`
- `simp` → `Lean.Meta.Simp.Config.failIfUnchanged`, `Bool.false` — `simp  (  failIfUnchanged  :=  false  )  only`

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `TopologicalSpace` — inductive, module `Mathlib.Topology.Defs.Basic`
- `Nonempty` — inductive, module `Init.Prelude`
- `Filter` — inductive, module `Mathlib.Order.Filter.Defs`
- `Not` — def, module `Init.Prelude`
- `Exists` — inductive, module `Init.Core`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
