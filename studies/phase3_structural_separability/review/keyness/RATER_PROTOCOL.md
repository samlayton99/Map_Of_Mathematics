# Keyness Rating Protocol (blind)

You are an independent mathematical rater. You will read Lean proofs from
Mathlib and judge candidate "move views" — lists that claim to show the
mathematically meaningful moves of each proof. The views are anonymized
(labels A-E, shuffled per proof); you must not attempt to guess which
system produced which view.

For EACH proof brief, in this order:

1. Read the theorem statement and the proof source. BEFORE looking at any
   view, write `key_move`: the single lemma/idea you would tell another
   mathematician first if explaining how this proof works. Use the actual
   Lean name when one exists, otherwise a short phrase.
2. Then read views A-E and give each `tells_how_it_works`: an integer 1-5
   (1 = useless or misleading; 3 = partially helpful; 5 = reading this list
   alone, I understand how the proof works).
3. For each view, `top1_is_key`: does the FIRST item of the view match your
   `key_move` (or an equivalent statement of it)? one of "yes"/"partial"/"no".
   For the unordered view (bullets, no numbers), judge its most prominent
   plausible reading and set "no" unless the set makes the key move obvious.
4. `best_view`: the single letter you would keep if only one view existed.
5. `notes`: one sentence, only if something is noteworthy (e.g. "the proof
   is pure automation; no view can help").

Judge as a mathematician explaining proofs to a colleague, not as a string
matcher: a deep lemma doing the real work beats trivia even if the trivia
is technically present. Automation internals, equality plumbing, and
typeclass bureaucracy are never key moves.

Output: a single JSON object
  {"proof_<i>": {"key_move": str, "ratings": {"A": int, ..., "E": int},
                 "top1_is_key": {"A": "yes|partial|no", ...},
                 "best_view": "A".."E", "notes": str}, ...}
covering every brief, written with your Write tool to the path you are
given. No other output format.
