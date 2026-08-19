# 04 — Features, Labels, and Leakage Controls

## 1. Feature families

Implement features in named groups so they can be ablated.

### F0 — Basic topology

- unique in-degree and out-degree;
- weighted in-degree and out-degree;
- total degree;
- in/out-degree ratio;
- neighbor-degree summary statistics;
- source/sink indicators;
- normalized depth or layer in the declaration DAG where well-defined.

### F1 — Global importance and structural role

- PageRank on dependency orientation;
- PageRank or equivalent on the reversed/use orientation;
- HITS hub and authority scores;
- k-core/coreness on a documented undirected projection;
- approximate betweenness or harmonic centrality;
- articulation/biconnected-component features where meaningful;
- approximate ancestor/dependent reach or sampled reachability.

For disconnected or directed graphs, use metrics whose interpretation is valid and document the projection.

### F2 — Community and bridge structure

Using a deterministic or fixed-seed community partition on a documented graph projection:

- community size;
- within-community degree z-score;
- participation coefficient;
- neighbor-community count;
- neighbor-community entropy;
- cross-community edge fraction;
- bridge or boundary score.

Do not use source file or namespace as a community feature. Files/domains are for evaluation splits only.

### F3 — Typed formal occurrence structure

Only in the typed-structure track:

- statement/type in/out degree;
- definition-body and proof-certificate in/out degree;
- statement-to-body occurrence ratio;
- occurrence multiplicity;
- relation-type entropy;
- application-head versus argument occurrence when available;
- occurrence-depth/path summaries.

### F4 — Theorem-local features

For candidate declaration `v` in theorem/proof `T`:

- local degree and centrality;
- distance from the proof root;
- minimum/mean application nesting depth;
- occurrence multiplicity;
- application-head fraction;
- proof-subgraph or branch coverage;
- local bridge score;
- local/global centrality ratio;
- whether the declaration occurs in the theorem statement or relevant local goal types;
- whether P5 records an explicit local use event;
- whether P4 result-type inference succeeded, recorded as missingness rather than silently dropping the item.

Use only features faithfully derivable from existing evidence. If a proposed feature is not well-defined on the current graph, omit it and explain why.

## 2. Label sets for Question A

### Existing broad label

`p3_any = 1` if any P3 classification is present; otherwise `0`.

Call the negative class `P3-unclassified` or `presumed-domain`, not “true mathematics.”

### Class-specific multi-label targets

Fit/report one-vs-rest results for every P3 class:

- typeclass-instance;
- recursor;
- structure-projection;
- generated;
- internal-detail;
- eq-machinery;
- logic-core;
- coercion.

Because classes overlap, preserve multi-label membership.

### Optional confidence tiers

If useful, group classes into clearly documented tiers such as implementation-generated scaffolding versus formal structural primitives, but never replace class-wise reporting with the tier.

## 3. Labels for Question B

Review labels are theorem-occurrence-relative, not permanent declaration labels:

- `key_landmark`;
- `useful_support`;
- `formal_scaffolding_or_noise`;
- `unclear_or_context_dependent`;
- `missing_local_or_conceptual_step` as a separate note, not a node class.

A declaration can receive different labels in different theorems.

## 4. Strict no-leakage policy

The primary topology-only and typed-structure models must not use:

- declaration names;
- namespace tokens;
- source text;
- docstrings;
- theorem statement tokens;
- comments;
- natural-language embeddings;
- semantic labels;
- P3 classifications or fields used to create them;
- source file/domain as predictive features;
- extraction coverage status as a predictive shortcut in the strict result.

The typed track may use exact formal relation types, but not target-defining metadata such as the environment instance flag when predicting `typeclass-instance`, projection flags when predicting `structure-projection`, or generated/internal flags when predicting those classes.

## 5. Leakage tests

Add automated checks that:

- replacing every declaration identifier with an opaque random ID leaves the strict feature matrix invariant;
- P3 class columns cannot be reached by the feature builder;
- source file/domain is used only for grouping and reporting;
- target-defining metadata is excluded from the corresponding model;
- no post-label filtering changes the input graph;
- train/test groups do not split obvious generated families when such families can be identified without reading the target label.
