/- Gate 1: a file with a real failing tactic action.
   The first step succeeds (observable transition), the second fails. -/

namespace CorpusFail

theorem bad (n : Nat) : n + 0 = n := by
  rw [Nat.add_comm]
  exact Nat.succ_ne_zero n

end CorpusFail
