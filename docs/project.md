### Your raw idea (full spec)

**Objective**
Build an open-source, **Lean-verifiable map of mathematics** that doubles as a **research companion**. It should prevent reinventing the wheel, orient researchers to adjacent tools/fields, and make new verified work immediately discoverable and connected to the rest of math.

**Core artifact**
A single, global **directed acyclic graph (DAG)** where:

* **Root nodes** are axioms/primitive definitions.
* **Definitions/structures** are nodes.
* **Theorems/lemmas** are nodes.
* **Edges** represent formal dependency (“this theorem/proof uses these definitions/lemmas/axioms”).
* Every node and edge is **Lean-checkable**, meaning any theorem is only admitted if its statement and proof typecheck in Lean.

**Ingestion / growth model**

* Anyone can contribute new math.
* If a contribution is **Lean-verified**, it is **automatically included** in the global graph.
* The system aims to handle:

  * different notations,
  * redundant definitions,
  * alternative proofs,
  * roundabout proof paths,
  * overlapping formalizations,
    while still letting them exist as verified artifacts.

**Agentic layer (the “research companion”)**
A natural-language interface where a researcher can describe:

* what they’re working on,
* the conjecture/goal,
* techniques they’re using,
* definitions/notation they prefer,

and an agent will:

1. **Locate the idea in the DAG** (find the closest existing nodes/subgraphs).
2. **Assess novelty / prior work** by checking whether equivalent or stronger results already exist in the graph.
3. **Suggest adjacent math**: what prerequisite tools, nearby fields, or lemmas are “close” in the dependency landscape.
4. **Recommend approaches**: candidate techniques, proof strategies, and relevant subgraphs to explore.
5. **Integrate new research**: help formalize and connect the work so it becomes a discoverable part of the global DAG once verified.

**Scalability / usability constraint (bloat control)**
Because a fully open graph will bloat quickly (multiple proofs, redundant routes, alternative formalizations), the default way the graph is shown and traversed should be a **“minimum energy DAG” view**:

* A compressive, canonical, easy-to-navigate projection of the full verified graph.
* It should prefer the simplest/most direct dependency routes and hide unnecessary detours by default.
* Users can still expand to see alternate proofs, longer chains, and deeper structure, but navigation starts from the minimum-energy view.

**Scope**

* Not a textbook, not just a proof library: a **global, continuously growing, machine-checked mathematical knowledge graph**.
* Covers “everything we know,” starting from a base corpus and expanding via community contributions and agent-assisted formalization.
* Intended to be both:

  * a **foundational map** (axioms → definitions → theorems),
  * and a **frontier tool** (cutting-edge research integration and discovery).

---

### Suggestions I’d add (after your raw idea)

* Treat “minimum energy DAG” as a **default view/projection** (canonical explanation subgraphs), while the underlying truth remains the full Lean dependency DAG.
* Explicitly represent and leverage **verified equivalences** (iso/iff/equiv) so “notation consolidation” is principled and reversible.
* Make the agent output **ranked candidates + confidence + proof/verification status** so novelty claims never feel hand-wavy.

**Confidence: 90%** (this is directly restating your described intent and constraints, with a small amount of structuring and labeling to make it a coherent spec).
