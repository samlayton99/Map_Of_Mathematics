# Landing port — add a ranking

Drop a `.py` file in this folder. It joins the suite everywhere: summary
tables, its own detail tab, the vibe check toggle, sweep curves, export
reports. Nothing else needs editing.

```python
# rankings_local/my_idea.py
from mathmap_eval import ranking

@ranking("R_my_idea", features=2)
def _mine(c, base):
    "One line describing it. This string is published in the dashboard."
    return (c.inc_in_stmt_world[base].astype("int8"),
            -c.inc_d_cite[base].astype(float))
```

Then:

```
~/venv/general_ml/bin/python src/ship.py
```

which verifies, exports, sweeps, packages and delivers to the laptop.

## The contract

Return **ascending lexicographic sort keys** — a tuple of arrays aligned to
`base`, lower = better rank. One array is fine.

A ranking **orders, never deletes**. Whatever it dislikes it ranks last. This
is checked: `src/ship.py` refuses to publish a ranking whose per-proof ranks
are not a permutation `0..n-1`, along with non-finite keys, wrong lengths and
non-numeric dtypes.

Keys must be a **pure function of the corpus** — no rater labels, no LLM
output, no held-out answers. Reading `review/labels/` from a ranking is
cheating and makes every semantic number meaningless.

## Signals available on `c`

| signal | meaning |
|---|---|
| `c.inc_d_cite[base]` | depth of the cited declaration |
| `c.inc_d_target[base]` | depth of the theorem being proved |
| `c.inc_in_stmt_world[base]` | cited thing already implied by the statement |
| `c.inc_roles[base]` | one-hot occurrence roles (8 columns) |
| `c.inc_glue[base]` | our structural plumbing flag |
| `c.inc_machinery[base]` | frozen V8 apparatus flag |
| `c.decl_is_claim[c.inc_decl[base]]` | the declaration is a proof, not data |
| `c.decl_logic_only[c.inc_decl[base]]` | purely logical ingredients |
| `c.decl_popularity[c.inc_decl[base]]` | library-wide citation count |
| `c.decl_idf[c.inc_decl[base]]` | `log(n_proofs / popularity)`, floored at 0 |
| `c.node_kind[c.inc_decl[base]]` | 0 theorem, 1 def, 2 inductive, … |

`base` is an array of incidence positions; index every global array with it.

## Inclusion policies

Same idea, different decorator — but note these are the *user's* knob, not
ours, and they may not change any ranking-quality number.

```python
from mathmap_eval import inclusion

@inclusion("my_policy", "per-proof", monotone_param="k")
def _mine(c, base, ranks, k=1):
    return ranks < k
```
