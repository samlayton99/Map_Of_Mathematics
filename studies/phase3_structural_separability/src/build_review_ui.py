#!/usr/bin/env python3
"""Generate the self-contained browser review page (review/ui/index.html).

Reads review/ui/review_data.json (built by build_review_data.py). English
statements and move glosses are authored here. Open the output directly:
  open studies/phase3_structural_separability/review/ui/index.html
"""
import json, os, html

HERE = os.path.dirname(os.path.abspath(__file__))
UI = os.path.normpath(os.path.join(HERE, "..", "review", "ui"))

STATEMENTS = {
    "Function.Bijective.existsUnique_iff":
        "Let f : A → B be a bijection and p a property of elements of B. Then there is "
        "exactly one y with p(y) if and only if there is exactly one x with p(f(x)).",
    "Function.Injective.isPartialInv":
        "If f is injective, then the canonical partial inverse of f (the function that "
        "returns the preimage of b when one exists, and nothing otherwise) really is a "
        "partial inverse: it maps f(a) back to a, and returns a only on input f(a).",
    "Function.LeftInverse.comp":
        "Left inverses compose: if f undoes g, and h undoes i, then h ∘ f undoes g ∘ i.",
    "IsClosed.and":
        "If the set of points satisfying P1 is closed, and the set satisfying P2 is "
        "closed, then the set of points satisfying both P1 and P2 is closed.",
    "Lattice.ext":
        "Two lattice structures on the same underlying set are equal as soon as they "
        "induce the same order relation (the same ≤).",
    "Nat.eq_one_of_dvd_coprimes":
        "If a and b are coprime natural numbers and k divides both, then k = 1.",
    "Nat.pow_sub_one_gcd_pow_sub_one":
        "For natural numbers: gcd(a^b − 1, a^c − 1) = a^gcd(b,c) − 1.",
    "Nat.pow_sub_one_mod_pow_sub_one":
        "For natural numbers: (a^c − 1) mod (a^b − 1) = a^(c mod b) − 1.",
    "Real.abs_log_mul_self_lt":
        "For real x with 0 < x ≤ 1: |x · log x| < 1.",
    "Real.le_exp_of_log_le":
        "For reals: if log x ≤ y, then x ≤ e^y.",
    "Real.one_sub_inv_le_log_of_pos":
        "For real x > 0: 1 − 1/x ≤ log x.",
    "Real.range_log":
        "The real logarithm attains every real value (its range is all of ℝ).",
    "TopologicalSpace.ext_iff":
        "Two topologies on the same set are equal exactly when they have the same open sets.",
    "add_one_zsmul":
        "In an additive group, (n + 1)·a = n·a + a for every integer n. (This lemma is "
        "auto-generated as the additive twin of a^(n+1) = a^n · a.)",
    "isClosed_sInter":
        "The intersection of an arbitrary family of closed sets is closed.",
    "limUnder_of_not_tendsto":
        "Mathlib's limit operator limUnder picks, using choice, a point that a function "
        "converges to — if one exists. This lemma: if the function converges to no point "
        "at all, the operator returns its default junk value (an arbitrary fixed point "
        "of the space).",
    "pow_iterate":
        "Applying “raise to the k-th power” n times in a row is the same as raising to "
        "the (k^n)-th power.",
    "sup_eq_and_inf_eq_iff":
        "In a lattice: a ⊔ b = c and a ⊓ b = c hold together exactly when a = c and "
        "b = c. (Auto-generated dual of the version with ⊔ and ⊓ swapped.)",
    "sup_left_idem":
        "In a join-semilattice: a ⊔ (a ⊔ b) = a ⊔ b.",
    "zpow_mul":
        "In a group, a^(m·n) = (a^m)^n for integer exponents m and n.",
}

GLOSS = {
    "AddGroup.toOrderedSub": "typeclass bridge: additive groups have well-behaved subtraction",
    "AddGroup.toSubtractionMonoid": "typeclass bridge: every additive group is a subtraction monoid",
    "And.casesOn": "logic glue: split a proof of “A and B” into its two parts",
    "And.intro": "logic glue: build “A and B” from proofs of A and B",
    "Classical.epsilon": "the choice operator: picks some element satisfying a property (axiom of choice)",
    "DivisionMonoid.toDivInvOneMonoid": "typeclass bridge between division-structure classes",
    "Eq": "the equality relation itself",
    "Eq.casesOn": "equality glue: use an equation by case analysis",
    "Eq.mp": "equality glue: transport a proof across an equality of propositions",
    "Eq.mpr": "equality glue: rewrite the goal along an equation",
    "Eq.ndrec": "equality glue: transport along an equation",
    "Eq.rec": "equality glue: transport along an equation (the primitive)",
    "Eq.refl": "equality glue: a = a",
    "Eq.symm": "equality glue: a = b implies b = a",
    "Eq.trans": "equality glue: chain two equations",
    "Filter.Tendsto": "the definition of “converges to” (via filters)",
    "Filter.lim": "the limit-picking operator (uses choice)",
    "Filter.limUnder": "the limit-of-a-function operator (uses choice)",
    "Function.Bijective.injective": "a bijection is injective",
    "Function.Bijective.surjective": "a bijection is surjective",
    "Function.LeftInverse": "the definition of “g is a left inverse of f”",
    "Function.Surjective.range_eq": "a surjective function has range equal to everything",
    "HPow.hPow": "the power operation a^b itself",
    "Iff.intro": "logic glue: build “A iff B” from the two directions",
    "Iff.rfl": "logic glue: A iff A",
    "Int.add_left_neg": "integers: (−a) + a = 0",
    "Int.negSucc_mul_negSucc": "integer multiplication, negative × negative case",
    "Int.negSucc_mul_ofNat": "integer multiplication, negative × nonnegative case",
    "Int.neg_add": "integers: −(a + b) = (−a) + (−b)",
    "Int.neg_add_cancel_right": "integers: (a + b) + (−b) = a",
    "Int.ofNat_mul_negSucc": "integer multiplication, nonnegative × negative case",
    "IsClosed.inter": "the intersection of two closed sets is closed",
    "IsOpen": "the definition of “open set”",
    "IsRelPrime": "the definition of “relatively prime” (common divisors are units)",
    "LE.le": "the ≤ relation itself",
    "Lattice.casesOn": "take a lattice structure apart into its components",
    "Lean.Omega.Constraint.addEquality_sat": "internal certificate lemma of the omega arithmetic tactic (automation plumbing)",
    "Lean.Omega.Constraint.not_sat'_of_isImpossible": "internal certificate lemma of the omega arithmetic tactic (automation plumbing)",
    "Lean.Omega.LinearCombo.coordinate_eval_1": "internal certificate lemma of the omega arithmetic tactic (automation plumbing)",
    "Lean.Omega.LinearCombo.coordinate_eval_2": "internal certificate lemma of the omega arithmetic tactic (automation plumbing)",
    "Lean.Omega.LinearCombo.coordinate_eval_6": "internal certificate lemma of the omega arithmetic tactic (automation plumbing)",
    "Lean.Omega.combo_sat'": "internal certificate lemma of the omega arithmetic tactic (automation plumbing)",
    "Lean.Omega.tidy_sat": "internal certificate lemma of the omega arithmetic tactic (automation plumbing)",
    "Mathlib.Tactic.Linarith.zero_lt_one": "internal lemma of the linarith tactic: 0 < 1",
    "Mathlib.Tactic.Ring.Common.inv_mul": "internal lemma of the ring tactic",
    "Monoid.toMulOneClass": "typeclass bridge: monoid → multiplication-with-one",
    "NPow.toPow": "typeclass bridge for the power operation",
    "Nat": "the type of natural numbers",
    "Nat.brecOn": "strong-induction engine for naturals (compiler-generated)",
    "Nat.coprime_iff_isRelPrime": "coprime (gcd = 1) is equivalent to the abstract “relatively prime”",
    "Nat.dvd_one": "k divides 1 iff k = 1",
    "Nat.instCommMonoid": "instance: the naturals form a commutative monoid",
    "Nat.instMonoid": "instance: the naturals form a monoid",
    "Nat.iterate": "the definition of iterating a function n times",
    "Nat.pow_sub_one_gcd_pow_sub_one._unary": "compiler-generated packed form of this very theorem (recursion plumbing)",
    "Nat.sub_lt_sub_iff_right": "naturals: b − a < c − a iff b < c (when a is small enough)",
    "Option.ctorIdx": "compiler plumbing for the Option type",
    "Option.some.noConfusion": "compiler plumbing: some x ≠ none, and some is injective",
    "PSigma.mk": "build a dependent pair",
    "PartialOrder.toPreorder": "typeclass bridge: partial order → preorder",
    "Real": "the type of real numbers (built from Cauchy sequences of rationals)",
    "Real.exp": "the real exponential function (defined by its power series)",
    "Real.exp_nonneg": "0 ≤ e^x for every real x",
    "Real.instField": "instance: ℝ is a field",
    "Real.instLE": "instance: the ≤ order on ℝ",
    "Real.instPreorder": "instance: ℝ is a preorder",
    "Real.instZero": "instance: ℝ has a zero",
    "Real.linearOrder": "instance: ℝ is linearly ordered",
    "Real.log": "the real logarithm (inverse of exp; 0 for nonpositive inputs)",
    "Real.log_div": "log(x/y) = log x − log y",
    "Real.log_inv": "log(1/x) = −log x",
    "Real.log_le_iff_le_exp": "log x ≤ y iff x ≤ e^y (for x > 0)",
    "Real.log_le_sub_one_of_pos": "log x ≤ x − 1 for x > 0",
    "Real.log_nonneg": "log x ≥ 0 when x ≥ 1",
    "Real.log_one": "log 1 = 0",
    "Real.log_surjective": "log attains every real value",
    "SemilatticeInf.ext": "two meet-semilattice structures with the same ≤ are equal",
    "SemilatticeInf.mk.noConfusion": "compiler plumbing: constructor injectivity for semilattice structures",
    "SemilatticeSup.ext": "two join-semilattice structures with the same ≤ are equal",
    "Set.compl_sInter": "complement of a family intersection = union of the complements",
    "Set.iUnion": "indexed union of sets (definition)",
    "Set.image": "image of a set under a function (definition)",
    "Set.ofPred": "the set of points satisfying a predicate (definition)",
    "Set.sUnion": "union of a family of sets (definition)",
    "Set.sUnion_image": "rewrite a union over an image as an indexed union",
    "TopologicalSpace": "the definition of a topology",
    "TopologicalSpace.ext": "two topologies with the same open sets are equal",
    "congrArg": "equality glue: a = b implies f(a) = f(b)",
    "congrFun'": "equality glue: equal functions give equal values",
    "congr_arg": "equality glue: a = b implies f(a) = f(b)",
    "dif_neg": "evaluate an if-then-else whose condition is known false",
    "dif_pos": "evaluate an if-then-else whose condition is known true",
    "eq_of_heq": "convert a heterogeneous equality to an ordinary one (plumbing)",
    "eq_self": "a = a is true (simp plumbing)",
    "forall_congr": "logic glue: pointwise-equivalent statements have equivalent ∀-forms",
    "funext": "two functions equal at every input are equal",
    "id": "the identity function",
    "inf_eq_sup": "a ⊓ b = a ⊔ b iff a = b",
    "inf_idem": "a ⊓ a = a",
    "inf_of_le_left": "if a ≤ b then a ⊓ b = a",
    "instHPow": "instance plumbing for the power operation",
    "instNatPowNat": "instance plumbing for natural-number powers",
    "instPowNat": "instance plumbing for natural-number powers",
    "inv_pow": "(a⁻¹)ⁿ = (aⁿ)⁻¹",
    "isOpen_biUnion": "a union of open sets (over a family) is open",
    "isUnit_iff_dvd_one": "k is a unit iff k divides 1",
    "le_inv_comm₀": "order/inverse swap: a ≤ 1/b iff b ≤ 1/a (positive elements)",
    "negSucc_zsmul": "integer scalar multiple, negative-integer case",
    "neg_le_sub_iff_le_add._simp_1": "compiler-generated simp helper (inequality rearrangement)",
    "neg_zsmul": "(−n)·a = −(n·a)",
    "nhds": "the neighborhood filter of a point (definition)",
    "noConfusion_of_Nat": "compiler plumbing: distinct constructors are unequal",
    "ofNat_zsmul": "integer scalar multiple agrees with the natural-number one on nonnegatives",
    "of_eq_true": "logic plumbing: from “P = True” conclude P",
    "pow_iterate._f": "compiler-generated recursion helper of this very theorem",
    "pow_mul": "a^(m·n) = (a^m)^n for natural-number exponents",
    "propext": "axiom: equivalent propositions are equal",
    "semigroupDvd": "instance: divisibility notation from multiplication",
    "succ_nsmul'": "(n+1)·a = a + n·a",
    "sup_idem": "a ⊔ a = a",
    "sup_of_le_left": "if b ≤ a then a ⊔ b = a",
    "sup_of_le_right": "if a ≤ b then a ⊔ b = b",
    "tsub_le_iff_right._simp_1": "compiler-generated simp helper (truncated-subtraction inequality)",
    "zpow_neg": "a^(−n) = (a^n)⁻¹ for integer exponents",
    "zpow_negSucc": "integer power, negative-exponent case: a^(−(n+1)) = (a^(n+1))⁻¹",
}


def esc(s):
    return html.escape(s, quote=True)


def move_li(m, rank=None):
    gloss = GLOSS.get(m["name"], "")
    badge = '<span class="badge new">new</span>' if m["new"] else '<span class="badge old">in stmt</span>'
    num = f'<span class="rank">{rank}</span>' if rank else ""
    g = f'<span class="gloss">{esc(gloss)}</span>' if gloss else '<span class="gloss dim">(no gloss)</span>'
    return (f'<li>{num}{g} <code>{esc(m["name"])}</code> '
            f'<span class="badge depth">d={m["depth"]}</span> {badge}</li>')


def card(decl, v):
    stmt = STATEMENTS[decl]
    moves = "\n".join(move_li(m, i + 1) for i, m in enumerate(v["moves"]))
    allc = "\n".join(move_li(m) for m in v["all_cands"])
    route = "\n".join(
        f'<li><span class="gloss">{esc(GLOSS.get(r, ""))}</span> <code>{esc(r)}</code></li>'
        for r in v["route"]) or "<li>(none identified)</li>"
    return f"""
<section class="card" id="{esc(decl)}">
  <h2><code>{esc(decl)}</code></h2>
  <p class="meta">Mathlib file: {esc(v["file"])} &middot; theorem depth {v["depth"]} &middot;
     statement depth {v["stmt_depth"]} &middot; {v["n_cands"]} ingredients in the proof term</p>
  <p class="stmt">{esc(stmt)}</p>
  <h3>Predicted moves (top {len(v["moves"])}, ranked: new-to-statement first, then depth)</h3>
  <ol class="moves">{moves}</ol>
  <details><summary>Show the actual Lean proof</summary>
    <pre>{esc(v["source"])}</pre>
    <h4>Comparison: lemmas the proof term actually applies (route view)</h4>
    <ul class="moves">{route}</ul>
  </details>
  <details><summary>Show all {v["n_cands"]} ingredients (same ranking)</summary>
    <ul class="moves">{allc}</ul>
  </details>
  <div class="judge">
    <span>How helpful was the predicted-moves list for understanding this proof?</span>
    <span class="stars" data-decl="{esc(decl)}">
      {"".join(f'<button data-v="{k}">{k}</button>' for k in range(1, 6))}
    </span>
    <textarea data-decl="{esc(decl)}" placeholder="notes (optional)"></textarea>
  </div>
</section>"""


def main():
    data = json.load(open(os.path.join(UI, "review_data.json")))
    missing = [d for d in data if d not in STATEMENTS]
    assert not missing, f"no English statement for: {missing}"
    order = sorted(data, key=lambda d: data[d]["depth"])
    cards = "\n".join(card(d, data[d]) for d in order)
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>MathMap Move Review</title>
<style>
:root {{ --bg:#f7f7f5; --card:#ffffff; --ink:#1a1a1a; --dim:#6b6b6b; --line:#e2e2dd;
        --acc:#2456a4; --new:#0a7a4b; --old:#8a6d1a; }}
@media (prefers-color-scheme: dark) {{
  :root {{ --bg:#141414; --card:#1e1e1e; --ink:#e8e8e4; --dim:#9a9a94; --line:#333;
          --acc:#7aa7e8; --new:#5fd3a0; --old:#d8bb6a; }} }}
* {{ box-sizing:border-box }}
body {{ margin:0; background:var(--bg); color:var(--ink);
       font:16px/1.55 -apple-system, "Segoe UI", sans-serif; }}
main {{ max-width:880px; margin:0 auto; padding:24px 16px 80px; }}
h1 {{ font-size:1.5rem }}
.intro {{ color:var(--dim); font-size:.95rem }}
.card {{ background:var(--card); border:1px solid var(--line); border-radius:10px;
        padding:18px 20px; margin:22px 0; }}
.card h2 {{ margin:0 0 2px; font-size:1.05rem }}
.meta {{ color:var(--dim); font-size:.85rem; margin:2px 0 10px }}
.stmt {{ font-size:1.05rem; border-left:3px solid var(--acc); padding-left:12px }}
h3 {{ font-size:.95rem; margin:16px 0 6px }}
ol.moves, ul.moves {{ margin:4px 0; padding-left:22px }}
.moves li {{ margin:5px 0; }}
.rank {{ display:none }}
.gloss {{ }}
.gloss.dim {{ color:var(--dim) }}
code {{ font:.82em ui-monospace, "SF Mono", Menlo, monospace; color:var(--dim);
        word-break:break-all }}
.card h2 code {{ color:var(--ink); font-size:1em }}
.badge {{ font-size:.72rem; padding:1px 7px; border-radius:9px; white-space:nowrap }}
.badge.depth {{ background:color-mix(in srgb, var(--acc) 14%, transparent); color:var(--acc) }}
.badge.new {{ background:color-mix(in srgb, var(--new) 14%, transparent); color:var(--new) }}
.badge.old {{ background:color-mix(in srgb, var(--old) 14%, transparent); color:var(--old) }}
details {{ margin:10px 0; }}
summary {{ cursor:pointer; color:var(--acc); font-size:.92rem }}
pre {{ background:var(--bg); border:1px solid var(--line); border-radius:8px;
      padding:12px; overflow-x:auto; font-size:.8rem; line-height:1.45 }}
.judge {{ border-top:1px solid var(--line); margin-top:14px; padding-top:12px;
         font-size:.9rem; color:var(--dim) }}
.stars {{ margin-left:10px }}
.stars button {{ width:30px; height:26px; margin:0 2px; border:1px solid var(--line);
  background:var(--card); color:var(--ink); border-radius:6px; cursor:pointer }}
.stars button.on {{ background:var(--acc); color:#fff; border-color:var(--acc) }}
.judge textarea {{ display:block; width:100%; margin-top:8px; min-height:34px;
  background:var(--bg); color:var(--ink); border:1px solid var(--line);
  border-radius:6px; padding:6px 8px; font:inherit; font-size:.88rem }}
#exportbar {{ position:sticky; top:0; background:var(--bg); padding:10px 0;
  border-bottom:1px solid var(--line); z-index:2 }}
#exportbar button {{ padding:6px 14px; border:1px solid var(--acc); color:var(--acc);
  background:var(--card); border-radius:8px; cursor:pointer; font:inherit; font-size:.9rem }}
#exportout {{ width:100%; min-height:60px; margin-top:8px; display:none;
  font:.78rem ui-monospace, Menlo, monospace }}
</style></head><body><main>
<h1>MathMap Move Review</h1>
<p class="intro">20 Mathlib proofs. For each: the statement in English, then the
<b>predicted moves</b> — the proof's ingredients ranked by a name-free graph score
(ingredients <b>new</b> to the statement first, deepest first). <b>d</b> = depth: how many
unfolding levels sit beneath a fact in all of Mathlib. <b>new</b> = not already needed
just to state the theorem; <b>in stmt</b> = already part of stating it. Form your judgment
from the list alone, then unhide the actual proof and rate how well the list anticipated
what the proof really does. Ratings and notes save locally; press Export when done and
send me the JSON.</p>
<div id="exportbar"><button id="exportbtn">Export review JSON</button>
<textarea id="exportout" readonly></textarea></div>
{cards}
</main>
<script>
const KEY = "mathmap-move-review-v1";
const state = JSON.parse(localStorage.getItem(KEY) || "{{}}");
function save() {{ localStorage.setItem(KEY, JSON.stringify(state)); }}
document.querySelectorAll(".stars").forEach(el => {{
  const d = el.dataset.decl;
  const paint = () => el.querySelectorAll("button").forEach(b =>
    b.classList.toggle("on", (state[d]||{{}}).score >= +b.dataset.v));
  el.querySelectorAll("button").forEach(b => b.addEventListener("click", () => {{
    state[d] = state[d] || {{}}; state[d].score = +b.dataset.v; save(); paint();
  }}));
  paint();
}});
document.querySelectorAll(".judge textarea").forEach(t => {{
  const d = t.dataset.decl;
  t.value = (state[d]||{{}}).notes || "";
  t.addEventListener("input", () => {{
    state[d] = state[d] || {{}}; state[d].notes = t.value; save();
  }});
}});
document.getElementById("exportbtn").addEventListener("click", () => {{
  const out = document.getElementById("exportout");
  out.style.display = "block";
  out.value = JSON.stringify(state, null, 1);
  out.select();
  try {{ navigator.clipboard.writeText(out.value); }} catch (e) {{}}
}});
</script></body></html>"""
    with open(os.path.join(UI, "index.html"), "w") as f:
        f.write(page)
    print(f"wrote {os.path.join(UI, 'index.html')} ({len(page)//1024} KB), {len(order)} proofs")


if __name__ == "__main__":
    main()
