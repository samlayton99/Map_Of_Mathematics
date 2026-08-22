# MathRecord: what it extracts, what MathMap uses, what is missing

Accounting as of 2026-08-22, read off the source rather than memory.

## 1. The object

MathRecord is a Lean 4 binary run against a fully-imported Mathlib
environment (`lake env mathrecord <cmd> ... ImportAllProbe.lean`). It has
no Mathlib build dependency -- it reads the environment, never the
source text. It emits FOUR independent channels:

| channel | command | scope | output |
|---|---|---|---|
| **kernel dependency dump** | `depdump` | all 771,129 constants | `mathlib_deps7.jsonl` (1.2 GB) |
| **occurrence forests** | `hierdump` / `hierdumpt` / `hierdumpx` | a named subset only | `*_hier.jsonl` |
| **environment lookups** | `modules`, `projflags`, `envfacts` | any name list | TSV |
| **elaboration provenance** | `provenance` | 40 files only | `prov/*.json` |

The last is explicitly a SIDECAR ("not kernel content") -- source-level
identifiers and tactic kinds, never mixed into the canonical structure.

## 2. Channel 1: depdump (the substrate MathMap is built on)

Per constant:

| field | meaning |
|---|---|
| `n` `k` | name, kernel kind (theorem/def/inductive/ctor/opaque/quot/axiom/recursor) |
| `pr` (`prf`) | type is Prop-valued, by kernel `Meta.isProp` (fallback flag) |
| `ps` (`psf`) | type telescopes to `Sort 0`: propositional vs DATA vocabulary |
| `ar` | arity -- with `ps`, separates bare propositions from predicates |
| `t` / `v` | type dependencies / value dependencies |
| `vo` | per value-dep, an 8-vector of occurrence counts by ROLE: 0 applied, 1 let-value, 2 explicit arg, 3 implicit arg, 4 instance-implicit arg, 5 strict-implicit, 6 type annotation, 7 unresolved |
| `hb` | derived: refs with any occurrence in roles {0,1,2,7} |
| `bf` | argument positions whose binder role could not be resolved |
| `gen` | elaborator recorded NO source range => machine-generated |
| `ir` | inductive is recursive |
| `c` | classification flags |
| `rt` | root head chain (parked) |

## 3. The bridge: build_incidence.py -> three npz arrays

| array | columns |
|---|---|
| `nodes.npz` | kind, pr, ps, ar, gen, **depth**, **in_degree**, **stated** |
| `artifacts.npz` | certifies, is_generated, n_incidences |
| `incid.npz` | artifact, decl, roles[8], load_bearing, in_stmt_world, d_target, d_cite, delta_depth |

Three fields are DERIVED here, not extracted: `depth` (exact SCC
condensation + longest path over the TYPE-only graph), `in_degree`, and
`in_stmt_world` (reverse-reachability from the theorem's statement
closure, following type deps everywhere plus non-theorem bodies, so it
never walks another theorem's proof).

## 4. What is extracted and then THROWN AWAY

| field | why |
|---|---|
| `c` (classification) | **correctly dropped**: it is built from NAME heuristics (`genSuffixes`, `logicCore`, `eqMachinery`, `coeRoots`, `isInternalDetail`) and violates the no-semantic-names principle |
| `hb` | redundant -- recomputed as `load_bearing` from roles |
| `rt` | deliberately parked |
| `bf`, `prf`, `psf` | fallback/quality counters, never joined |
| `ir` | isRec never reaches the npz |
| **`isInstance`** | **an accident**: `Meta.isInstance` IS computed in depdump, but only as an input to the name-contaminated `c`, so it was discarded along with it |

That last row is the one real loss. Note it is a genuinely different
fact from what the lane rule uses: our "infra" lane keys off role 5 /
instance-implicit ARGUMENT position -- a property of the CITATION SITE.
Whether the cited declaration IS an instance is a property of the
DECLARATION, and we never had it.

## 5. What was never collected at all

Ranked by (value x cheapness):

1. **Attributes.** Nothing anywhere reads any attribute. `@[simp]` is
   the big one: a lemma the library expects to fire automatically is a
   very different citation from a chosen mathematical step, and this is
   a pure environment fact with no names in it.
2. **Reducibility.** `reducibilityString` exists in `Extract.lean` and
   is used by the old per-file path, but is NOT emitted at map scale.
   `@[reducible]` marks a definition meant to be unfolded -- an
   abbreviation, i.e. plumbing.
3. **Declaration source position.** `findDeclarationRanges?` is called
   only to produce the BOOLEAN `gen`; the line number is thrown away.
   That is the within-file declaration ORDER, a finer chronological axis
   than the git file dates we resorted to for the chronological test.
4. **Occurrence POSITION at map scale.** `hierdump` records
   parent/argIdx/nesting/nargs, but only for named subsets (the 120 +
   48 graded targets, 52 metamorphic variants, a 20k sample). At map
   scale we have role COUNTS only. The frozen ranking's `first` key
   therefore has no corpus-wide equivalent -- harmless today (the
   gap-cut uses only depth, which is why `frozen_test` shows spec ==
   shipped) but blocking if we ever want ranked lists library-wide.
5. **Tactic kinds at map scale.** Exists in the provenance sidecar for
   40 files. Map-wide would need re-elaboration of all of Mathlib with
   InfoTrees on.
6. **Mathlib-specific attributes** (`@[ext]`, `@[norm_cast]`,
   `@[to_additive]`, `@[simps]`). These live in Mathlib's OWN
   environment extensions; reading them needs mathrecord to build
   against Mathlib, which today it deliberately does not.

## 6. Implemented today: `mathrecord envfacts`

New command, new module `Mathrecord/EnvFacts.lean`, wired into `Main`.
One TSV row per requested name; every column an environment fact:

    name  inst  red  simp  proj  cls  rec  unsafe  line  levels

- `inst` -- `Meta.isInstance` (gap 4 above, recovered)
- `red` -- reducibility 0/1/2/3 (gap 2)
- `simp` -- member of the default simp set, rewrite rules plus
  decls-to-unfold (gap 1, core-Lean part)
- `proj`/`cls` -- projection facts, folding in `projflags` so one file
  is authoritative
- `rec`, `unsafe`, `levels` -- cheap kernel facts that were being dropped
- `line` -- 1-based declaration line, -1 when absent (gap 3)

Deliberately NOT included: anything derived from a name, a docstring, or
a comment.

## 7. What the new facts are worth (measured, not assumed)

Run over all 771,129 declarations: 42,809 instances, 99,035 simp-set
members, 52,737 reducible, 463,580 with a source line. Validation:
`envfacts` reproduces `projflags` EXACTLY (4,619 class projections,
identical sets), and `frozen_test` still passes 4/4 unchanged.

Joined to 2,366 graded candidate slots across BOTH blind instruments
(120 + 48 targets, 3 raters each). "Useful" = consensus grade >= 3.

| fact | n | P(useful \| fact) | P(useful \| not) | ratio |
|---|---|---|---|---|
| registered instance | 704 | 0.041 | 0.187 | **0.22x** |
| recursive inductive (thm) | 24 | 0.000 | 0.115 | 0.00x |
| reducible (thm targets) | 65 | 0.000 | 0.119 | 0.00x |
| reducible (def targets) | 116 | 0.233 | 0.169 | 1.38x |
| **`@[simp]` member** | 28 | **0.679** | 0.137 | **4.96x** |

Three findings, two of them corrections to my own expectations:

1. **`isInstance` is a strong junk marker AND 95% redundant.**
   P(lane2 \| instance) = 0.950 and P(instance \| lane2) = 0.994.
   Outside lane 2 only 16-17 graded slots remain and the signal is
   noise. Among items the current policy would actually INCLUDE, one
   or two instance slots survive. So recovering the accidentally-lost
   fact changes nothing -- but it *validates* the existing rule: the
   role-5 argument-position proxy is a near-perfect stand-in for the
   declaration fact. That is worth knowing and was never checked.

2. **`reducible` is a real, non-redundant junk marker that our current
   policy SHIPS.** Among theorem-target items the frozen construction
   includes (dem 0, lane 0), reducible ones are **0 of 17 useful**
   against 0.517 for the rest. Tested as a lane-2 demotion for theorem
   targets on all three corpora:

   | | blind1 thm KM | blind1 thm F1 | old corpus KM (held out) | old F1 |
   |---|---|---|---|---|
   | frozen | 0.8939 | 0.7026 | 0.9127 | 0.6960 |
   | + reducible demotion | 0.8939 | 0.7046 | **0.9057** | 0.6975 |

   **NOT ADOPTED.** It buys +0.002 F1 and costs -0.007 key-move on the
   held-out corpus -- the exact signature that caught the
   class-projection over-reach on theorems. n=17 is too thin to spend
   held-out accuracy on.

3. **`@[simp]` is the OPPOSITE of the hypothesis it was collected to
   test.** I expected simp lemmas to be rewriting machinery. They are
   5x MORE likely to be graded useful, and the effect survives inside
   the move lane (0.750 vs 0.364 for non-simp lane-0 items). A
   plausible mechanism: simp lemmas that merely FIRE get absorbed into
   `Eq.mpr` scaffolding, so what survives as an explicit named citation
   in the kernel term is the substantive one. **n=28 -- a lead, not a
   result.** It wants a targeted sample before anything is built on it.

Net: no rule changes, `frozen.py` untouched, and the substrate is
richer by six facts with their predictive value measured rather than
assumed.

## 8. Left undone, with reasons

- **Mathlib attributes**: needs a build-architecture decision (add
  Mathlib as a mathrecord dependency). Recommend doing it -- `@[ext]`
  in particular names exactly the structural workhorses the map found
  and the LLM missed.
- **Map-scale hierdump**: a real run, not a lookup; estimate before
  committing.
- **Map-scale tactic channel**: full re-elaboration; the most expensive
  item on the list and the least clearly load-bearing.
