/- Gate 0 spike: a file whose proof contains a failing action.
   Used to test that failed tactic applications are observable. -/

namespace Gate0SpikeFail

theorem bad (n : Nat) : n + 0 = n := by
  rw [Nat.add_comm]   -- succeeds: goal becomes 0 + n = n
  exact Nat.succ_ne_zero n  -- FAILS: type mismatch

end Gate0SpikeFail
