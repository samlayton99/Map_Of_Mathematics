# Paste this into the coding agent

Read the attached MathMap / MathRecord handoff, beginning with `00_CODING_AGENT_PROMPT.md`.

Execute **only Gate 0 and Gate 1**.

First audit the current Lean ecosystem and determine what exact objects and maintained tools already exist. Avoid inventing a new intermediate representation where Lean or existing tooling already provides the required data.

Then build and validate the smallest coherent record

\[
\mathcal R=(E,X,D,S,T)
\]

of Lean environments, typed expressions, declarations, and local states, with only a transition-access spike for `T`. Lean remains the verifier and source of formal truth.

After Gate 1, stop. Produce the gate reports and one evidence-based recommendation: proceed to dynamic traces, revise the object, or abandon/wrap an existing representation.

Do not build a large Mathlib extraction, polished storefront, graph platform, model, conjecture generator, abstraction inventor, or curation system in this run.

Negative results are acceptable. The goal is to discover whether the smallest exact object is coherent and worth building on.
