# Future Natural-Language Tagging Harness

## 1. Role

A future agent harness may inspect natural-language mathematics and attach metadata to exact formal objects.

This is potentially important because Lean proof terms often do not preserve the conceptual explanation humans care about.

## 2. Possible annotations

- informal theorem statement;
- proof sketch;
- key named tools;
- proof-method labels;
- concepts and fields;
- prerequisites;
- application areas;
- difficulty;
- novelty/importance claims;
- analogy or bridge claims;
- correspondence between paper steps and Lean artifacts.

## 3. Trust boundary

Every annotation must carry:

- source document or agent;
- target exact ID;
- extraction method;
- confidence;
- timestamp/version;
- review status;
- supersession/retraction history.

Annotations never alter formal identity or kernel validity.

## 4. Research use

The tagging harness may eventually provide:

- human-scale route labels;
- supervision for semantic zoom;
- concept-conditioned retrieval;
- evaluation data for extracted candidate maps;
- bridge and analogy hypotheses.

It should be treated as a source of fallible semantic evidence, not a solution assumed in advance.
