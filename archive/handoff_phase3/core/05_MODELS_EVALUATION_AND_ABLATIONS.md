# 05 — Models, Evaluation, and Ablations

## 1. Descriptive analysis first

Before predictive modeling, show the feature distributions of each P3 class and the unclassified group.

Report whether apparent separation is driven by:

- extreme degree;
- a small number of universal nodes;
- one domain;
- one extraction-coverage stratum;
- or a stable combination of features.

## 2. Primary interpretable models

Use:

- prevalence/majority baseline;
- one-feature degree thresholds;
- regularized logistic regression;
- shallow decision tree with a predeclared maximum depth.

Standardize or log-transform heavy-tailed features where appropriate and document transformations.

A random forest or gradient-boosted model may be reported as an optional performance ceiling. It must not replace the interpretable analysis. Do not implement a GNN in this phase.

## 3. Evaluation splits

Report at least:

### Transductive descriptive split

A stratified random or repeated split that answers whether labels are separable within the observed graph.

Label this as transductive and do not interpret it as cross-domain generalization.

### Grouped module/file split

Hold out files or coherent modules to avoid near-duplicate local leakage.

### Leave-one-domain-out split

Train on five Phase 2 domains and test on the sixth. Repeat for all domains.

Where graph features require the full graph, state whether the result is transductive. For a stronger inductive sensitivity check, recompute features without held-out labels and, where feasible, without held-out internal edges.

## 4. Metrics for Question A

Because classes may be imbalanced, report:

- class prevalence;
- precision–recall AUC;
- ROC AUC;
- balanced accuracy;
- precision, recall, and F1 at a threshold selected on training data;
- calibration or reliability where probabilities are used;
- bootstrap confidence intervals grouped by file/domain rather than only by node.

For multi-label classes, report macro and per-class results.

Include a permutation test or shuffled-label sanity check within domains.

## 5. Degree-matched and boundary-matched controls

For each broad and class-specific result, include a comparison in which positive and negative examples are approximately matched on:

- degree;
- full versus shallow coverage;
- and domain/file where feasible.

The purpose is to determine whether richer topology adds information beyond “machinery is high-degree” or “imported nodes look different.”

## 6. Landmark ranking baselines

For each reviewed theorem, compare at least:

1. raw P2 support order or a documented neutral order;
2. occurrence frequency/multiplicity;
3. global PageRank or centrality alone;
4. existing P3 binary filtering/downweighting;
5. P4-route;
6. local structural salience alone;
7. combined soft machinery probability plus local salience;
8. P3/P4/P5 hybrid if available for that theorem.

Do not allow a method to benefit from source-proof information unavailable to its comparator without labeling that difference.

## 7. Metrics for Question B

On reviewed theorem-occurrence labels, report:

- precision at small `k`;
- recall of `key_landmark` at `k`;
- nDCG at `k` using landmark/support/scaffolding grades;
- scaffolding/noise fraction at `k`;
- pairwise reviewer preference among anonymized views;
- per-proof results and medians, not only pooled node metrics;
- grouped bootstrap intervals over proofs;
- reviewer agreement and reviewer-specific results.

A useful operational measure is:

> At a fixed recall of reviewed key landmarks, how much formal scaffolding can the structural score remove or downweight compared with P3 and P4-route?

## 8. Required ablations

- P2 simple graph versus P1 weighted occurrence graph;
- strict untyped topology versus typed formal relations;
- global features versus theorem-local features;
- degree-only versus all interpretable features;
- with versus without community features;
- coverage-controlled versus all-node population;
- hard P3 filtering versus soft probability downweighting;
- P4 result-inference success versus failure strata;
- term proofs versus tactic proofs;
- domain-by-domain results.

## 9. Interpretation rules

- High Question A performance does not imply human landmark discovery.
- High in-graph performance with poor domain holdout means the pattern is local, not universal.
- A model that reproduces P3 may simply reveal that P3 classes have distinct formal roles.
- Failure of one graph projection does not refute the unified exact structure.
- Negative results are valid outputs and must be preserved.
