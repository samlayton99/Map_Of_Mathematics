/- Gate 0 spike corpus: three small proofs plus supporting declarations. -/

namespace Gate0Spike

/-- A transparent definition with a body. -/
def double (n : Nat) : Nat := n + n

/-- Proof 1: tactic proof with intro/induction-free rewriting. -/
theorem double_eq_two_mul (n : Nat) : double n = 2 * n := by
  unfold double
  rw [Nat.two_mul]

/-- Proof 2: a dependent statement with a local `let` and an existential witness,
proved by a multi-step tactic script (gives branching tactic states). -/
theorem exists_gt (n : Nat) : ∃ m, n < m := by
  let m := n + 1
  refine ⟨m, ?_⟩
  exact Nat.lt_succ_self n

/-- Proof 3: a term-mode proof (no tactics at all). -/
theorem add_comm_spike (a b : Nat) : a + b = b + a :=
  Nat.add_comm a b

end Gate0Spike
