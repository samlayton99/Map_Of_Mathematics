# Reviewer Worksheet — Phase 2A candidate representations

For each proof file in this bundle, answer (1=useless … 5=excellent). No human
review has been performed by the extraction pipeline itself; nothing in the
bundle is a usefulness claim.

1. Which single named declaration would be the most helpful hint for
   reconstructing this proof, and does the P2 domain list contain it?
2. Rate P2 (support set) as a short proof hint. How much is noise/infrastructure?
3. Rate P4 (application spine): does structure/nesting add information over P2?
4. Rate P5 (tactic events): does source-level order/role add information?
5. Which important conceptual tools are missing from every view?
6. Does order/grouping matter for this proof?
7. Does one-level expansion (P6) help or merely add verbosity?
8. Where would a natural-language tag be indispensable?
9. Best coarse summary for this proof: P2 / P3 / P4 / P5 / hybrid / none.

## Bundle contents
- Algebra_Group_Basic / automation / `pow_iterate`
- Algebra_Group_Basic / automation / `div_mul_comm`
- Algebra_Group_Basic / automation / `zpow_add_one`
- Algebra_Group_Basic / induction / `zpow_induction_right`
- Algebra_Group_Basic / induction / `zpow_induction_left`
- Algebra_Group_Basic / rewrite / `mul_right_comm`
- Algebra_Group_Basic / rewrite / `div_eq_div_iff_div_eq_div`
- Algebra_Group_Basic / rewrite / `zpow_mul`
- Algebra_Group_Basic / tactic-other / `pow_dite`
- Algebra_Group_Basic / tactic-other / `dite_pow`
- Algebra_Group_Basic / tactic-other / `eq_one_iff_eq_one_of_mul_eq_one`
- Algebra_Group_Basic / term / `additive_of_isTotal`
- Algebra_Group_Basic / term / `eq_neg_add_of_add_eq`
- Algebra_Group_Basic / term / `add_one_zsmul`
- Analysis_SpecialFunctions_Log_Basic / automation / `Real.log_div_self`
- Analysis_SpecialFunctions_Log_Basic / automation / `Real.log_finprod`
- Analysis_SpecialFunctions_Log_Basic / automation / `Real.log_le_self`
- Analysis_SpecialFunctions_Log_Basic / induction / `Real.log_zpow`
- Analysis_SpecialFunctions_Log_Basic / rewrite / `Real.log_lt_iff_lt_exp`
- Analysis_SpecialFunctions_Log_Basic / rewrite / `Real.le_exp_log`
- Analysis_SpecialFunctions_Log_Basic / rewrite / `Real.abs_log_mul_self_lt`
- Analysis_SpecialFunctions_Log_Basic / tactic-other / `Real.le_exp_of_log_le`
- Analysis_SpecialFunctions_Log_Basic / tactic-other / `Real.lt_exp_of_log_lt`
- Analysis_SpecialFunctions_Log_Basic / tactic-other / `Real.continuousAt_log_iff`
- Analysis_SpecialFunctions_Log_Basic / term / `Real.range_log`
- Analysis_SpecialFunctions_Log_Basic / term / `Real.surjOn_log`
- Analysis_SpecialFunctions_Log_Basic / term / `Real.one_sub_inv_le_log_of_pos`
- Data_Nat_GCD_Basic / automation / `Nat.pow_sub_one_gcd_pow_sub_one`
- Data_Nat_GCD_Basic / automation / `Nat.coprime_add_iff_left`
- Data_Nat_GCD_Basic / automation / `Nat.pow_sub_one_mod_pow_sub_one`
- Data_Nat_GCD_Basic / rewrite / `Nat.gcd_right_comm`
- Data_Nat_GCD_Basic / rewrite / `Nat.coprime_add_mul_right_left`
- Data_Nat_GCD_Basic / rewrite / `Nat.Coprime.mul_add_mul_ne_mul`
- Data_Nat_GCD_Basic / tactic-other / `Nat.gcd_mul_gcd_eq_iff_dvd_mul_of_coprime`
- Data_Nat_GCD_Basic / term / `Nat.Coprime.symmetric`
- Data_Nat_GCD_Basic / term / `Nat.dvd_lcm_of_dvd_right`
- Data_Nat_GCD_Basic / term / `Nat.eq_one_of_dvd_coprimes`
- Logic_Function_Basic / automation / `Function.extend_injective`
- Logic_Function_Basic / automation / `Function.Bijective.comp_right`
- Logic_Function_Basic / automation / `Function.surjective_comp_right_iff_injective`
- Logic_Function_Basic / induction / `cast_bijective`
- Logic_Function_Basic / induction / `eq_mp_bijective`
- Logic_Function_Basic / induction / `eq_mpr_bijective`
- Logic_Function_Basic / rewrite / `Function.LeftInverse.comp`
- Logic_Function_Basic / rewrite / `Function.Involutive.leftInverse_iff`
- Logic_Function_Basic / rewrite / `Function.Injective.isPartialInv`
- Logic_Function_Basic / tactic-other / `Function.hfunext`
- Logic_Function_Basic / tactic-other / `Function.LeftInverse.eq_rec_eq`
- Logic_Function_Basic / tactic-other / `Std.Symm.forall_existsUnique_iff'`
- Logic_Function_Basic / term / `Bool.involutive_not`
- Logic_Function_Basic / term / `Function.const_injective`
- Logic_Function_Basic / term / `Function.Bijective.existsUnique_iff`
- Order_Lattice / automation / `sup_left_idem`
- Order_Lattice / automation / `sup_assoc`
- Order_Lattice / automation / `AntitoneOn.map_sup`
- Order_Lattice / induction / `SemilatticeSup.ext`
- Order_Lattice / induction / `Lattice.ext`
- Order_Lattice / rewrite / `sup_left_right_swap`
- Order_Lattice / rewrite / `semilatticeSup_mk'_partialOrder_eq_semilatticeInf_mk'_partialOrder`
- Order_Lattice / rewrite / `le_of_inf_le_sup_le`
- Order_Lattice / tactic-other / `le_iff_exists_sup`
- Order_Lattice / tactic-other / `sup_eq_maxDefault`
- Order_Lattice / tactic-other / `inf_eq_and_sup_eq_iff`
- Order_Lattice / term / `DistribLattice.le_sup_inf`
- Order_Lattice / term / `ofDual_inf`
- Order_Lattice / term / `sup_eq_and_inf_eq_iff`
- Topology_Basic / automation / `isClosed_iUnion_of_finite`
- Topology_Basic / automation / `TopologicalSpace.ext_iff_isClosed`
- Topology_Basic / automation / `limUnder_of_not_tendsto`
- Topology_Basic / rewrite / `isOpen_empty`
- Topology_Basic / rewrite / `isOpen_iff_of_cover`
- Topology_Basic / rewrite / `IsOpen.union`
- Topology_Basic / tactic-other / `TopologicalSpace.ext_iff`
- Topology_Basic / term / `IsClosed.and`
- Topology_Basic / term / `IsOpen.sdiff`
- Topology_Basic / term / `isClosed_sInter`
