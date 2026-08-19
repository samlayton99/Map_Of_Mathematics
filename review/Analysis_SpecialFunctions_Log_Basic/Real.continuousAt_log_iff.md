# Real.continuousAt_log_iff

*file:* `Mathlib/Analysis/SpecialFunctions/Log/Basic.lean` · *style (derived):* tactic-other · *proof-term size:* 787 nodes

## Statement and source  [lean-exact]

```lean
@[simp]
theorem continuousAt_log_iff : ContinuousAt log x ↔ x ≠ 0 := by
  refine ⟨?_, continuousAt_log⟩
  rintro h rfl
  exact not_tendsto_nhds_of_tendsto_atBot tendsto_log_nhdsNE_zero _ <|
    h.tendsto.mono_left nhdsWithin_le_nhds
```

Exact proof reference: record decl `d22` in `studies/Analysis_SpecialFunctions_Log_Basic.study.json` (type `x5889`, value `x6021`).

## P2 — support set (body)  [deterministic-derived]

**Domain (15):** `Real`, `ContinuousAt`, `Real.log`, `Ne`, `Eq`, `False`, `not_tendsto_nhds_of_tendsto_atBot`, `nhdsWithin`, `Set`, `Real.tendsto_log_nhdsNE_zero`, `Filter.Tendsto.mono_left`, `nhds`, `ContinuousAt.tendsto`, `nhdsWithin_le_nhds`, `Real.continuousAt_log`

**Classified infrastructure (43):** `Iff.intro` (logic-core,logic-core-ctor), `UniformSpace.toTopologicalSpace` (structure-projection,typeclass-instance), `PseudoMetricSpace.toUniformSpace` (structure-projection,typeclass-instance), `Real.pseudoMetricSpace` (typeclass-instance), `OfNat.ofNat` (structure-projection), `Zero.toOfNat0` (typeclass-instance), `Real.instZero` (typeclass-instance), `Eq.ndrec` (eq-machinery,generated), `Real.instPreorder` (typeclass-instance), `instNoBotOrderOfNoMinOrder` (typeclass-instance), `instNoMinOrderOfNontrivial` (typeclass-instance), `Real.instRing` (typeclass-instance), `Real.partialOrder` (typeclass-instance), `Real.instIsOrderedRing` (typeclass-instance), `Real.instNontrivial` (typeclass-instance), `instClosedIicTopology` (typeclass-instance), `HasSolidNorm.orderClosedTopology` (typeclass-instance), `Real.normedAddCommGroup` (typeclass-instance), `Real.lattice` (typeclass-instance), `instHasSolidNormReal` (typeclass-instance), `Real.instIsOrderedAddMonoid` (typeclass-instance), `Compl.compl` (structure-projection), `Set.instCompl` (typeclass-instance), `Singleton.singleton` (structure-projection), `Set.instSingletonSet` (typeclass-instance), `Real.punctured_nhds_module_neBot` (typeclass-instance), `Real.instAddCommGroup` (typeclass-instance), `IsSemitopologicalSemiring.toContinuousAdd` (structure-projection,typeclass-instance), `NonUnitalNonAssocRing.toNonUnitalNonAssocSemiring` (typeclass-instance), `NonUnitalNonAssocCommRing.toNonUnitalNonAssocRing` (structure-projection,typeclass-instance), `NonUnitalCommRing.toNonUnitalNonAssocCommRing` (typeclass-instance), `CommRing.toNonUnitalCommRing` (typeclass-instance), `Real.commRing` (typeclass-instance), `IsSemitopologicalRing.toIsSemitopologicalSemiring` (structure-projection,typeclass-instance), `IsTopologicalRing.toIsSemitopologicalRing` (typeclass-instance), `instIsTopologicalRingReal` (typeclass-instance), `Semiring.toModule` (typeclass-instance), `Real.semiring` (typeclass-instance), `ContinuousMul.to_continuousSMul` (typeclass-instance), `Real.instMul` (typeclass-instance), `IsTopologicalSemiring.toContinuousMul` (structure-projection,typeclass-instance), `IsTopologicalRing.toIsTopologicalSemiring` (structure-projection,typeclass-instance), `Eq.symm` (eq-machinery)

## P4 — named application spine (top of tree)  [deterministic-derived]

- `Real` (0 args)
- `Iff.intro` (4 args) : Iff [Prop]
  - `ContinuousAt` (6 args) : <sort>
    - `Real` (0 args)
    - `Real` (0 args)
    - `UniformSpace.toTopologicalSpace` (2 args) : TopologicalSpace
      - `Real` (0 args)
      - `PseudoMetricSpace.toUniformSpace` (2 args) : UniformSpace
        - `Real` (0 args)
        - `Real.pseudoMetricSpace` (0 args)
    - `UniformSpace.toTopologicalSpace` (2 args) : TopologicalSpace
      - `Real` (0 args)
      - `PseudoMetricSpace.toUniformSpace` (2 args) : UniformSpace
        - `Real` (0 args)
        - `Real.pseudoMetricSpace` (0 args)
    - `Real.log` (0 args)
  - `Ne` (3 args) : <sort>
    - `Real` (0 args)
    - `OfNat.ofNat` (3 args) : Real
      - `Real` (0 args)
      - `Zero.toOfNat0` (2 args) : OfNat
        - `Real` (0 args)
        - `Real.instZero` (0 args)
  - `ContinuousAt` (6 args) : <sort>
    - `Real` (0 args)
    - `Real` (0 args)
    - `UniformSpace.toTopologicalSpace` (2 args) : TopologicalSpace
      - `Real` (0 args)
      - `PseudoMetricSpace.toUniformSpace` (2 args) : UniformSpace
        - `Real` (0 args)
  ... (367 occurrences total)

## P4-route — Prop-resulting spines with domain heads  [derived filter of P4]

- `not_tendsto_nhds_of_tendsto_atBot` (12 args) : False (depth 2)
- `Filter.Tendsto.mono_left` (8 args) : Filter.Tendsto (depth 3)
- `ContinuousAt.tendsto` (7 args) : Filter.Tendsto (depth 4)
- `nhdsWithin_le_nhds` (4 args) : LE.le (depth 4)
- `Real.continuousAt_log` (1 args) : <pi> (depth 1)

## P5 — source-level use events  [observed]

- `refine` → `Iff.intro` — `refine ⟨?_, continuousAt_log⟩`
- `exact` → `not_tendsto_nhds_of_tendsto_atBot` — `exact not_tendsto_nhds_of_tendsto_atBot tendsto_log_nhdsNE_zero _ <|
    h.tends`

## P6 — one-level expansion of top domain dependencies  [deterministic-derived]

- `Real` — inductive, module `Mathlib.Data.Real.Basic`
- `ContinuousAt` — def, module `Mathlib.Topology.Defs.Filter`
- `Real.log` — def, module `Basic`
- `Ne` — def, module `Init.Core`
- `Eq` — inductive, module `Init.Prelude`

## Reviewer questions (see WORKSHEET.md)

P2-hint useful? [1-5]   P2 noise? [1-5]   P4 adds over P2? [1-5]   P5 adds over P2/P4? [1-5]   missing key ideas? [free text]   best coarse view? [P2/P3/P4/P5/none]
