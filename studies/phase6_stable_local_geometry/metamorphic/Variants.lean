import Mathlib

/-!
# Metamorphic variant corpus (Phase 6, P2)

Each `mm_g<k>_v<j>` group proves ONE statement several ways.  Groups g1..g11
are HARMLESS refactorings (the mathematics is the same route); groups
`mm_c<k>_v<j>` are CONTROLS: genuinely different mathematical routes to the
same statement, which must NOT come out invariant.

Transformation families covered:
  F1 simp/simpa vs explicit rewrite chain      g1, g8, g9, g11
  F2 inline term vs named `have` steps         g2, g3, g8, g9, g10
  F3 tactic proof vs term-mode proof           g1, g2, g3, g7, g9, g10
  F4 explicit instance/argument vs inferred    g4
  F5 wrapper insertion                         g5
  F6 fold vs unfold of a definition            g6
  F8 constructor/witness syntax variants       g7
-/

set_option linter.all false
set_option maxHeartbeats 1000000

/-! ## g1 — length of a self-append: simp vs rewrite chain vs term mode -/

theorem mm_g1_v1 (l : List ℕ) : (l ++ l).length = 2 * l.length := by
  simp [List.length_append, two_mul]

theorem mm_g1_v2 (l : List ℕ) : (l ++ l).length = 2 * l.length := by
  rw [List.length_append, two_mul]

theorem mm_g1_v3 (l : List ℕ) : (l ++ l).length = 2 * l.length :=
  Eq.trans (List.length_append ..) (two_mul l.length).symm

theorem mm_g1_v4 (l : List ℕ) : (l ++ l).length = 2 * l.length := by
  have h : (l ++ l).length = l.length + l.length := List.length_append ..
  have h2 : 2 * l.length = l.length + l.length := two_mul l.length
  exact h.trans h2.symm

/-! ## g2 — intersection inside union: term vs tactic vs named have -/

theorem mm_g2_v1 {α : Type*} (s t : Set α) : s ∩ t ⊆ s ∪ t :=
  fun _ hx => Or.inl hx.1

theorem mm_g2_v2 {α : Type*} (s t : Set α) : s ∩ t ⊆ s ∪ t := by
  intro x hx
  exact Or.inl hx.1

theorem mm_g2_v3 {α : Type*} (s t : Set α) : s ∩ t ⊆ s ∪ t := by
  intro x hx
  have hs : x ∈ s := hx.1
  exact Or.inl hs

/-- Control variant inside g2: a genuinely different route (compose two
library subset lemmas instead of arguing pointwise). -/
theorem mm_g2_v4 {α : Type*} (s t : Set α) : s ∩ t ⊆ s ∪ t :=
  Set.inter_subset_left.trans Set.subset_union_left

/-! ## g3 — associativity of min: term vs rewrite vs named have -/

theorem mm_g3_v1 {α : Type*} [LinearOrder α] (a b c : α) :
    min a (min b c) = min (min a b) c :=
  (min_assoc a b c).symm

theorem mm_g3_v2 {α : Type*} [LinearOrder α] (a b c : α) :
    min a (min b c) = min (min a b) c := by
  rw [min_assoc]

theorem mm_g3_v3 {α : Type*} [LinearOrder α] (a b c : α) :
    min a (min b c) = min (min a b) c := by
  have h : min (min a b) c = min a (min b c) := min_assoc a b c
  exact h.symm

theorem mm_g3_v4 {α : Type*} [LinearOrder α] (a b c : α) :
    min a (min b c) = min (min a b) c := by
  symm
  exact min_assoc a b c

/-! ## g4 — explicit instance/type argument vs inferred -/

theorem mm_g4_v1 (x y : ℝ) : x ≤ max x y :=
  le_max_left x y

theorem mm_g4_v2 (x y : ℝ) : x ≤ max x y :=
  @le_max_left ℝ inferInstance x y

theorem mm_g4_v3 (x y : ℝ) : x ≤ max x y :=
  le_max_left (α := ℝ) x y

theorem mm_g4_v4 (x y : ℝ) : x ≤ max x y := by
  exact le_max_left ..

/-! ## g5 — wrapper insertion

`mm_g5_helper` is a free-standing forwarding wrapper (owned by nobody);
`mm_g5_v3.aux` is a forwarding wrapper Lean names UNDER the variant, so the
generated-owner redirect should treat it as an internal step. -/

theorem mm_g5_helper (l : List ℕ) : l.reverse.reverse = l :=
  List.reverse_reverse ..

theorem mm_g5_v3.aux (l : List ℕ) : l.reverse.reverse = l :=
  List.reverse_reverse ..

theorem mm_g5_v1 (l : List ℕ) : l.reverse.reverse = l :=
  List.reverse_reverse ..

theorem mm_g5_v2 (l : List ℕ) : l.reverse.reverse = l :=
  mm_g5_helper l

theorem mm_g5_v3 (l : List ℕ) : l.reverse.reverse = l :=
  mm_g5_v3.aux l

/-! ## g6 — fold vs unfold of a definition -/

def mm_dbl (n : ℕ) : ℕ := 2 * n

theorem mm_g6_v1 (n : ℕ) : mm_dbl n = n + n := by
  rw [mm_dbl, two_mul]

theorem mm_g6_v2 (n : ℕ) : mm_dbl n = n + n := by
  unfold mm_dbl
  exact two_mul n

theorem mm_g6_v3 (n : ℕ) : mm_dbl n = n + n :=
  two_mul n

theorem mm_g6_v4 (n : ℕ) : mm_dbl n = n + n := by
  show 2 * n = n + n
  exact two_mul n

/-! ## g7 — constructor / witness syntax variants -/

theorem mm_g7_v1 : ∃ n : ℕ, 3 < n ∧ n < 5 :=
  ⟨4, by norm_num, by norm_num⟩

theorem mm_g7_v2 : ∃ n : ℕ, 3 < n ∧ n < 5 :=
  Exists.intro 4 (And.intro (by norm_num) (by norm_num))

theorem mm_g7_v3 : ∃ n : ℕ, 3 < n ∧ n < 5 := by
  refine ⟨4, ?_, ?_⟩ <;> norm_num

theorem mm_g7_v4 : ∃ n : ℕ, 3 < n ∧ n < 5 := by
  have h : (3 : ℕ) < 4 ∧ (4 : ℕ) < 5 := ⟨by norm_num, by norm_num⟩
  exact ⟨4, h⟩

/-! ## g8 — continuity: automation vs explicit composition vs named haves -/

theorem mm_g8_v1 : Continuous fun x : ℝ => x ^ 2 + 3 * x := by
  fun_prop

theorem mm_g8_v2 : Continuous fun x : ℝ => x ^ 2 + 3 * x :=
  (continuous_pow 2).add (continuous_const.mul continuous_id)

theorem mm_g8_v3 : Continuous fun x : ℝ => x ^ 2 + 3 * x := by
  apply Continuous.add
  · exact continuous_pow 2
  · exact continuous_const.mul continuous_id

theorem mm_g8_v4 : Continuous fun x : ℝ => x ^ 2 + 3 * x := by
  have h1 : Continuous fun x : ℝ => x ^ 2 := continuous_pow 2
  have h2 : Continuous fun x : ℝ => 3 * x := continuous_const.mul continuous_id
  exact h1.add h2

/-! ## g9 — cardinality of a range: simp vs named lemma vs rewrite vs have -/

theorem mm_g9_v1 (n : ℕ) : (Finset.range n).card = n := by
  simp

theorem mm_g9_v2 (n : ℕ) : (Finset.range n).card = n :=
  Finset.card_range n

theorem mm_g9_v3 (n : ℕ) : (Finset.range n).card = n := by
  rw [Finset.card_range]

theorem mm_g9_v4 (n : ℕ) : (Finset.range n).card = n := by
  have h : (Finset.range n).card = n := Finset.card_range n
  exact h

/-! ## g10 — transitivity of subset: term vs pointwise vs have -/

theorem mm_g10_v1 {α : Type*} (s t u : Set α) (h1 : s ⊆ t) (h2 : t ⊆ u) : s ⊆ u :=
  h1.trans h2

theorem mm_g10_v2 {α : Type*} (s t u : Set α) (h1 : s ⊆ t) (h2 : t ⊆ u) : s ⊆ u := by
  exact subset_trans h1 h2

theorem mm_g10_v3 {α : Type*} (s t u : Set α) (h1 : s ⊆ t) (h2 : t ⊆ u) : s ⊆ u := by
  intro x hx
  have hxt : x ∈ t := h1 hx
  exact h2 hxt

theorem mm_g10_v4 {α : Type*} (s t u : Set α) (h1 : s ⊆ t) (h2 : t ⊆ u) : s ⊆ u :=
  fun _ hx => h2 (h1 hx)

/-! ## g11 — binomial square: named lemma vs rewrite vs have -/

theorem mm_g11_v1 (a b : ℝ) : (a + b) ^ 2 = a ^ 2 + 2 * a * b + b ^ 2 :=
  add_sq a b

theorem mm_g11_v2 (a b : ℝ) : (a + b) ^ 2 = a ^ 2 + 2 * a * b + b ^ 2 := by
  rw [add_sq]

theorem mm_g11_v3 (a b : ℝ) : (a + b) ^ 2 = a ^ 2 + 2 * a * b + b ^ 2 := by
  have h : (a + b) ^ 2 = a ^ 2 + 2 * a * b + b ^ 2 := add_sq a b
  exact h

/-- Control variant inside g11: `ring` builds a normalisation certificate
instead of citing the algebraic identity. -/
theorem mm_g11_v4 (a b : ℝ) : (a + b) ^ 2 = a ^ 2 + 2 * a * b + b ^ 2 := by
  ring

/-! ## c1 — CONTROL: library lemma vs induction -/

theorem mm_c1_v1 (n : ℕ) : 0 ≤ n :=
  Nat.zero_le n

theorem mm_c1_v2 (n : ℕ) : 0 ≤ n := by
  induction n with
  | zero => exact Nat.le_refl 0
  | succ k ih => exact Nat.le_succ_of_le ih

/-! ## c2 — CONTROL: closed form (simp/card) vs induction on the range -/

theorem mm_c2_v1 (n : ℕ) : ∑ _i ∈ Finset.range n, (1 : ℕ) = n := by
  simp

theorem mm_c2_v2 (n : ℕ) : ∑ _i ∈ Finset.range n, (1 : ℕ) = n := by
  induction n with
  | zero => simp
  | succ k ih => rw [Finset.sum_range_succ, ih]

/-! ## c3 — CONTROL: library commutativity vs induction -/

theorem mm_c3_v1 (a b : ℕ) : a * b = b * a :=
  Nat.mul_comm a b

theorem mm_c3_v2 (a b : ℕ) : a * b = b * a := by
  induction b with
  | zero => simp
  | succ k ih => rw [Nat.mul_succ, ih, Nat.succ_mul]
