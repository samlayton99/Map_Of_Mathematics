# Minimal Provisional Data Model

## 1. Principle

Store exact Lean data once. Compute candidate views. Do not turn every research hypothesis into a permanent entity.

## 2. Existing exact core

Retain:

- environment;
- expressions;
- declarations;
- exact theorem/definition bodies;
- local states where observed;
- source provenance.

## 3. Minimal derived records

### ReferenceOccurrence

```text
owner_artifact
referenced_declaration
expression_location
multiplicity_index
layer = type | body
classification[]
trust
```

### ApplicationOccurrence

```text
owner_artifact
head_declaration
root_expression
arguments[]
parent_occurrence?
expression_location
completeness
trust
```

### CandidateProofView

```text
owner_proof
view_kind
node_refs[]
edge_or_group_data
filter_spec?
completeness
provenance
```

### UseEvent

Use the minimal schema in Phase 2B.

### Annotation

```text
target_kind
target_id
annotation_type
payload
source
confidence
created_at
supersedes?
```

## 4. Deferred entities

Do not require these until evidence shows they are needed:

- formal statement families;
- permanent certificate-route objects;
- universal AND–OR route schema;
- proof-diversity metrics;
- concept ontology;
- map-region entities;
- curation/value objects;
- general operational snapshots;
- full alternative-proof registry.

They can be introduced later through ADRs.
