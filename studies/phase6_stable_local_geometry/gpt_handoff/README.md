# MathMap — Stable Local Geometry and Multiscale Atlas

## Executive judgment

The latest review package found a real problem, but its proposed remedy stops one level too early.

It is right that:

- a local proof edge should not change because unrelated mathematics was added elsewhere;
- global quantities such as use, centrality, communities, and branch importance may evolve;
- global connectivity was the wrong map-quality target;
- universal low-level nodes can create false shortcuts;
- one rule need not serve both local proof explanation and global navigation.

However, the review still treats a proof primarily as a flat list of citations and then searches for a better ranking or filter over that list.

The original MathMap formulation already contained the likely missing object:

> A proof is a finite rooted, typed term-construction graph. Named citations occur at different positions and nesting levels inside it.

Flattening that hierarchy turns low-level support, implicit arguments, generated obligations, and nested applications into siblings and direct global edges. Global rarity then looks indispensable because it statistically pushes those flattened descendants back down. The same flattening also creates the universal hubs and artificial shortcuts now being diagnosed.

The next research push should therefore test this central hypothesis:

\[
\boxed{
\text{Restoring local proof hierarchy will reduce both ranking noise and global shortcuts more principledly than another scalar score.}
}
\]

The recommended architecture is:

\[
\text{stable exact local move objects}
\;\longrightarrow\;
\text{typed multiscale views}
\;\longrightarrow\;
\text{global atlas}
\;+\;
\text{versioned global fields}
\;\longrightarrow\;
\text{learned navigation}.
\]

## The governing distinction

For an unchanged proof artifact \(p\), adding unrelated declarations must preserve:

- its exact term;
- its occurrence graph;
- its typed local move relations;
- its intrinsic local edge attributes;
- its default intrinsic local ordering or layers.

The global atlas may legitimately update:

- citation counts;
- rarity;
- centrality;
- communities;
- branch importance;
- learned navigation policies.

Those dynamic quantities must be versioned sidecars. They may influence a current navigator without rewriting the canonical local structure.

## The most important theoretical conclusions

1. **No exact append-safe proxy for global universality exists.** Universality is an up-set/future-use property. Two declarations can have identical local/down-set structure and later receive radically different use. `delta_depth` therefore cannot be “universality”; it is an abstraction-span coordinate.

2. **The bad object is often the flat direct edge.** A low-level citation nested inside a named application should not automatically become a direct same-level neighbour of the theorem.

3. **Use a multifiltration, not one weighted sum.** Preserve at least:
   - local explanatory salience;
   - abstraction span;
   - relation/lane type.
   Let the user or navigation task select a view.

4. **Depth should become vertical geometry.** A large depth drop means “drill downward,” not automatically “bad edge.” A deep theorem citing `Eq` is a vertical support relation; a same-scale citation is a lateral mathematical neighbour.

5. **Definitions require typed lanes.** A definition in a type annotation is conceptual context; an unfolded definition or constructed object is a proof move. Both belong in MathMap, but not as indistinguishable items in one flat ranking.

6. **Rarity remains valuable—but as a dynamic global field or teacher, not a canonical local edge definition.**

7. **The strongest independent validation is metamorphic invariance.** Harmless proof refactorings should change the exact certificate while preserving the high-level navigational skeleton.

## Read order

1. `01_REVISED_PRINCIPLES.md`
2. `02_FORMAL_THEORY.md`
3. `03_ANSWERS_TO_REVIEW_QUESTIONS.md`
4. `04_HYPOTHESES.md`
5. `05_EXPERIMENT_PROGRAM.md`
6. `06_METAMORPHIC_VALIDATION.md`
7. `07_NEURAL_NAVIGATOR.md`
8. `PROMPT_TO_CODING_AGENT.md`
