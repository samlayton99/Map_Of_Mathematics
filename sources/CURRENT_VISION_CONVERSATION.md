The most mature formulation I would now endorse is:

> **Relative to a fixed Lean environment, mathematics can be represented as a context-indexed, certified, recursively expandable typed hypergraph.**
>
> The primitive nodes are well-typed mathematical constructions. The primitive hyperedges are valid term-construction or inference steps. Named definitions and theorems act as reversible abstraction boundaries: each can be treated as one node or expanded into the certified subgraph that implements it. Different proofs are different routes to the same theorem. Category theory organizes contexts, substitution, and transport. Lean certifies the exact formal core.

That is not merely a metaphor. It is a plausible technical specification.

It also resolves the tension we kept encountering:

-  A bare theorem-citation graph is too crude. 
-  A typed, contextual, hierarchical hypergraph is not too crude. 
-  Category theory does not replace the hypergraph; it supplies its organizing laws. 
-  There can be one unified underlying object even though there are many proof routes and many useful views. 

## 1. The foundational primitive is a typed judgment

For a fixed Lean environment Σ, the fundamental object is:

Σ;Γ⊢t\:A.​ 

This says:

- Σ: these global declarations, definitions, theorems, inductive types, and axioms are available; 
- Γ: these local variables and assumptions are available; 
- t: this is the mathematical construction; 
- A: this is its type. 

Examples include:

Γ⊢3\:N, Γ⊢f\:R→R, 

and, under Curry–Howard,

Γ⊢p\:P, 

where P is a proposition and p is its proof.

Types themselves are also terms at a higher universe level:

Γ⊢A\:Typeu​. 

So objects, functions, propositions, structures, and proofs all inhabit the same typed formal world.

This is the actual unification—not that all mathematics is “just theorem nodes,” but that all formal mathematical artifacts can be expressed as typed terms.

## 2. Primitive hyperedges are term-construction steps

A typed term is built from smaller typed terms.

For example, function application is:

Γ⊢f(a)\:B(a)Γ⊢f:Πx\:A​B(x)Γ⊢a\:A​. 

As a directed hyperedge:

{Γ⊢f:Πx\:A​B(x),Γ⊢a\:A}⟶Γ⊢f(a)\:B(a).​ 

This is a genuine hyperedge because the output requires both inputs jointly.

Lambda abstraction is another construction:

Γ⊢λx.b:Πx\:A​B(x)Γ,x\:A⊢b\:B(x)​. 

Conjunction construction looks like:

Γ⊢⟨p,q⟩\:P∧QΓ⊢p\:PΓ⊢q\:Q​. 

Induction, rewriting, existential construction, structure construction, projection, recursion, and theorem application can all be represented through typed construction steps of this general form.

So the primitive formal object is not merely:

A→B. 

It is a labeled, typed, contextual hyperedge:

{J1​,…,Jk​}constructor or inference​J.​ 

Here every Ji​ and J is a well-typed judgment.

A bare hypergraph would be too weak. A **typed and context-indexed** hypergraph is substantially richer.

The earlier outside review reached essentially the same correction: a proof is not simply a set of ordinary dependency edges, but a derivationally closed set of labeled hyperedges that preserve joint premises. 

## 3. A proof is a rooted certified subhypergraph

Suppose T is a theorem and Lean accepts:

Σ⊢p\:T. 

The term p is constructed from smaller terms. Those terms are constructed from still smaller terms.

The resulting structure is:

H(p), 

a finite rooted term or proof hypergraph whose root is:

p\:T. 

Every internal hyperedge represents a legal construction. Every premise is either:

-  produced by another hyperedge; 
-  a local assumption; 
-  a referenced declaration; 
-  an inductive constructor or recursor; 
-  an explicit axiom; 
-  a kernel-level primitive. 

Thus:

a proof is a finite rooted, derivationally closed, certified hypergraph.​ 

“Certified” means that the graph is not trusted because it looks reasonable. It is generated from—or can be reconstructed into—a proof term that Lean checks.

This gives a precise interpretation of your original “proof as a set of edges” intuition. You were missing three details:

1.  The edges generally have multiple inputs, so they are hyperedges. 
2.  The nodes and edges are typed and live in contexts. 
3.  The graph must be derivationally closed and carry a checkable certificate. 

But the broad structural intuition was correct.

## 4. Every declaration has an interface and an implementation

A Lean declaration has approximately the form:

d\:A:=t. 

Here:

- d is the name; 
- A is the interface or type; 
- t is the body, implementation, or proof. 

For a definition:

Even\:N→Prop 

might have the body:

Even(n):=∃k, n=2k. 

For a theorem:

even\_add\_even\:Even(a)→Even(b)→Even(a+b) 

has a proof term inhabiting that type.

Therefore every declaration has two expandable structures.

### The statement/type graph

Htype​(d)=H(A). 

This tells us what is required to express the declaration.

It includes the constants and constructions appearing in the statement.

### The body/proof graph

Hbody​(d)=H(t). 

This tells us how the declaration is implemented or proved.

These give two importantly different dependency relations:

TypeDeps(d) 

and

BodyDeps(d). 

A theorem may be stated entirely in the language of topology while its selected proof uses measure theory. The statement dependencies and proof dependencies should therefore never be conflated.

This distinction is already present in MathRecord’s declaration and expression layers.

## 5. A named declaration is a reversible abstraction boundary

Suppose a proof uses theorem L.

At coarse resolution, we see:

L​. 

That is useful because L may stand for hundreds or thousands of lower-level construction steps.

At finer resolution:

L​expand/fold​Hbody​(L). 

A definition behaves similarly:

D​expand/fold​Hbody​(D). 

This is the exact formal content behind the claim that definitions and lemmas are compression.

They are not merely labels added to a graph. They introduce reusable interfaces that allow a large subgraph to be treated as one mathematical unit.

That means the mathematical library is simultaneously:

-  a collection of proved artifacts; 
-  a vocabulary; 
-  a system of reusable interfaces; 
-  a hierarchy of compression boundaries. 

This is why mathematical discovery is not merely graph search. Mathematicians can alter the effective graph by introducing a useful abstraction. The earlier review identified this as the deepest departure from chess: definitions compress recurring subgraphs and thereby modify the action space. 

## 6. Exact zoom is a family of opacity choices

There is a particularly clean way to formalize zooming.

Let D be the declarations available in the environment.

Choose some set:

O⊆D 

of declarations that should be treated as **opaque** at the current zoom level.

When constructing the view of proof p:

-  declarations in O remain collapsed nodes; 
-  declarations not in O are expanded into their bodies when available. 

Call the resulting view:

HO​(p). 

If:

O1​⊆O2​, 

then O1​ treats fewer declarations as opaque and therefore produces a finer view:

HO1​​(p)⟶HO2​​(p). 

This is the rigorous version of zoom.

At one extreme, almost everything is opaque:

Theorem T uses Lemmas A,B,C.​ 

At another level:

A,B,C 

are expanded into their own proof graphs.

At the finest useful formal level, all available declaration bodies have been expanded until we reach:

-  kernel expression constructors; 
-  primitive recursors; 
-  explicit axioms; 
-  opaque declarations with unavailable bodies; 
-  recursive back-references. 

The exact zoom structure is therefore not necessarily one linear hierarchy:

H0​→H1​→H2​. 

It is more naturally a **partially ordered family of views**. We can independently expand one branch while leaving another collapsed.

That matches actual mathematical reading. A user might understand topology well and keep all topology collapsed while expanding the unfamiliar algebraic portion.

So the Google Maps analogy becomes:

> A zoom level is a choice about which named mathematical interfaces are treated as atomic.

## 7. The hierarchy is not literally a tree

Locally, the syntax of one term can be displayed as a tree.

But globally:

-  the same theorem may be cited by thousands of proofs; 
-  the same definition may occur in many statements; 
-  different abstractions may overlap; 
-  several proof routes may share large regions; 
-  recursive and mutual definitions may create finite cycles or strongly connected blocks. 

So the more accurate progression is:

syntax tree→shared term DAG→typed proof hypergraph→hierarchical mathematical hypergraph. 

For a fixed Lean environment, named declaration dependencies are usually acyclic because a declaration generally references earlier declarations. Mutual declarations and recursive constructions should be represented as grouped strongly connected components or as finite back-references—not unfolded indefinitely.

This is important. “Fully unfolding mathematics” does not mean infinitely normalizing every recursive function.

It means exposing the finite formal construction while preserving recursion and induction explicitly.

## 8. Alternative proofs form a proof family

For theorem T, define:

PΣ​(T)={p∣Σ⊢p\:T}. 

Each proof gives a hypergraph:

p↦H(p). 

So:

HΣ​(T)={H(p)\:p∈PΣ​(T)}.​ 

This is the **proof family** of T.

I would avoid calling it an equivalence class until we choose an actual equivalence relation. Proofs can be considered equivalent in many different senses:

-  definitionally equal; 
-  propositionally equal; 
-  extensionally equivalent; 
-  identical after erasing implementation details; 
-  merely proofs of the same proposition. 

Lean may treat proofs in `Prop` as proof-irrelevant for many formal purposes, but MathMap should preserve distinct proof artifacts because their dependency structure, explanatory value, and generalizability may differ.

Your representative-proof idea is then:

HT,q∗​∈argH∈HΣ​(T)min​Cq​(H), 

where q identifies the user's objective.

For example:

Ccitations​(H)=#{distinct named dependencies}, Csteps​(H)=#{primitive inference steps}, Cdepth​(H)=depth(H), 

or:

Ccombined​(H)=αCcitations​+βCsteps​+γCdepth​. 

Eventually we might estimate:

Chuman​(H) 

or:

Cfuture​(H), 

representing conceptual difficulty or expected future utility.

There is probably no universal optimal proof. The correct output is often a Pareto frontier:

-  shortest proof; 
-  fewest dependencies; 
-  weakest assumptions; 
-  most elementary prerequisites; 
-  most computational; 
-  most explanatory; 
-  most reusable. 

Again, Google Maps does not choose one metaphysically correct route.

## 9. Category theory supplies the contextual structure

The hypergraph captures the construction and dependency geometry.

Category theory answers:

> How do mathematical constructions move coherently between contexts?

Let:

Γ=(x\:R) 

and suppose we have:

Γ⊢p\:P(x). 

Now introduce another context:

Δ=(y\:R) 

with substitution:

σ\:x↦y+1. 

Write:

σ:Δ→Γ. 

Applying the substitution transports the judgment:

Γ⊢p\:P(x) 

to:

Δ⊢σ∗p\:P(y+1). 

The contexts and substitutions form a category:

CtxΣ​. 

Every context has types and terms living over it. Every valid substitution transports those types and terms.

At a schematic level, one can describe the proof hypergraph as context-indexed:

HΣ​\:CtxΣop​⟶TypedHyp. 

This means:

-  every context Γ has a typed proof hypergraph HΣ​(Γ); 
-  every substitution σ:Δ→Γ induces a structure-preserving map: 

σ∗\:HΣ​(Γ)⟶HΣ​(Δ). 

This is the mathematically precise version of:

> The local machinery is the same everywhere.

Substitution, application, abstraction, induction, and composition do not depend on whether the local subject is algebra, topology, or probability.

The categorical structure guarantees that these operations interact coherently with contexts.

So the two pictures divide the work:

category/type theoryhypergraph​: context, typing, substitution, transport,: construction, dependency, proof routes, hierarchy.​​ 

Category theory is the grammar.

The hypergraph is the map.

## 10. The unified exact object

A concise formal specification is therefore:

MΣ​=(CtxΣ​,JΣ​,EΣ​,DΣ​,body,cert).​ 

Here:

### CtxΣ​

The category of contexts and valid substitutions.

### JΣ​

The typed judgments:

Γ⊢t\:A. 

### EΣ​

The directed hyperedges corresponding to valid term constructors and inference instances.

### DΣ​

The named declarations in the environment.

### body

The map taking a declaration to its stored implementation or proof term when available:

d↦td​. 

### cert

The connection from nodes and hyperedges back to Lean-checkable terms.

The object actually stored in a finite repository is not all theoretically possible Lean mathematics. That would be infinite.

Instead, we distinguish:

UΣ​=all well-typed constructions possible in Σ 

from:

Kt​⊆UΣt​​, 

the finite, growing body of mathematics that has actually been named, proved, recorded, or explored by time t.

So the total mathematical record is more accurately:

Mt​=(Σt​,Kt​,fold/unfold structure,provenance).​ 

The type theory defines the possible territory.

The mathematical library records the explored and curated territory.

## 11. Soundness has a precise but limited meaning

“Provably sound” must be scoped carefully.

The exact formal claim is:

> Every certified theorem node and proof hyperedge corresponds to a term accepted by the Lean kernel in the recorded environment.

For:

{P1​,…,Pn​}→Q, 

the certificate can be a term:

e\:P1​→⋯→Pn​→Q. 

For a theorem:

T, 

the certificate is:

p\:T. 

For a definition:

d\:A:=t, 

the certificate is that Lean accepts:

t\:A. 

Exact fold/unfold must preserve the underlying term up to the appropriate formal equality—typically alpha-equivalence or definitional equality.

But this soundness is relative to:

(Lean foundation,environment,version,axioms). 

The map must therefore preserve:

-  environment fingerprint; 
-  explicit axiom dependencies; 
-  whether `sorryAx` or unsafe assumptions occur; 
-  library version; 
-  chosen proof. 

The Lean kernel does not establish:

-  that Lean itself is consistent; 
-  that the formal statement captures an author's informal intent; 
-  that the theorem is novel; 
-  that it is important; 
-  that a conceptual summary is accurate. 

So the system needs a strict boundary.

### Certified core

Lean-checkable declarations, proof terms, definitions, exact dependencies, and exact expansion maps.

### Semantic overlay

Human or model-generated labels such as:

-  “compactness argument”; 
-  “analogous to Fourier duality”; 
-  “important bridge theorem”; 
-  “appropriate for an undergraduate”; 
-  “used in economics.” 

The semantic overlay can be invaluable, but it must remain distinguishable from kernel-certified truth.

This is how the system stays honest.

## 12. The zoom hierarchy has exact and interpretive levels

The exact formal levels are approximately:

named theorem or definition⇕named declaration dependencies⇕proof/body term graph⇕primitive term constructors⇕kernel-checkable expression​​ 

These can be connected by exact expansion and collapse.

Above them we can eventually add:

human proof methodsmathematical conceptstheories and fieldsapplications and models​​ 

Those higher views may not be exactly derivable from syntax.

The missing “grocery store” is largely the mapping from the exact graph to the task-appropriate semantic view. The independent review identified this learned coarse-graining as one of the central unbuilt layers. 

## 13. How modern mathematics sits on top of the primitives

The construction tower is approximately:

kernel term constructors​ 

then:

inductive types, recursors, basic logic, equality​ 

then:

data structures and mathematical structures​ 

such as naturals, integers, groups, rings, fields, ordered sets, metric spaces, and topological spaces;

then:

concepts and interfaces​ 

such as continuity, compactness, measurability, differentiability, spectra, manifolds, and homology;

then:

lemmas and theories​ 

then:

major theorems​. 

A theorem about compact continuous functions can be displayed as one node.

Expanding its statement exposes:

-  the function type; 
-  the topology; 
-  compactness; 
-  continuity; 
-  order structure. 

Expanding its proof exposes the lemmas and constructions used.

Expanding those exposes lower-level definitions and proof terms.

Eventually we reach Lean's core term language and explicit assumptions.

The relationship is similar to:

high-level program⟷libraries⟷intermediate representation⟷machine instructions. 

But the intermediate levels are mathematically meaningful and should not be discarded.

## 14. What MathRecord has actually built

MathRecord currently records approximately:

(E,X,D,S,T). 

For the structural object you care about, the most important pieces are:

E+X+D​. 

### E: environment

The exact Lean and Mathlib context in which a declaration has meaning.

### X: expression structure

The typed expression trees/DAGs of theorem statements, definitions, and proof terms.

### D: declarations

Named constants linked to their types and bodies.

These three components are enough to begin deriving:

-  statement/type graphs; 
-  definition-body graphs; 
-  proof-term graphs; 
-  direct type dependencies; 
-  direct proof dependencies; 
-  recursively expanded declaration graphs; 
-  exact declaration-level fold/unfold views. 

The proof-state and transition layers S,T are valuable for studying proof search, agents, failed attempts, and mathematical process.

But they are not logically necessary for the first structural MathMap.

So I would revise the immediate priority.

## 15. The correct next object to build

The next prototype should be:

> **A certified static hierarchical hypergraph projection of a bounded Lean corpus.**

For each selected declaration d, it should produce:

Htype​(d), 

the statement/type graph, and:

Hbody​(d), 

the definition or proof graph.

It should then support:

1.  Named declaration nodes. 
2.  Separate type and body dependencies. 
3.  Primitive typed construction hyperedges. 
4.  Exact fold/unfold at declaration boundaries. 
5.  Multiple opacity sets O, producing different exact zoom views. 
6.  Distinct proof routes where alternative proof terms are available. 
7.  Explicit leaves for axioms, primitives, opaque bodies, and recursion. 
8.  Reconstruction or kernel validation proving that the view corresponds to the original Lean object. 
9.  A thin interface that allows a user to expand one branch without expanding all others. 
10.  A clear separation between exact formal views and later semantic annotations. 

The first proof-of-concept should use perhaps 50–200 declarations, chosen to include:

-  ordinary definitions; 
-  structures; 
-  inductive types; 
-  recursive definitions; 
-  simple and complex theorems; 
-  shared dependencies; 
-  alternative proofs; 
-  typeclass-heavy mathematics; 
-  opaque and transparent declarations. 

The central acceptance test would be:

> Every displayed exact node and hyperedge must be traceable back to the original Lean expression, and every fold/unfold operation must preserve the underlying certified artifact.

That would be the first real construction of the object you originally imagined.

## Final formulation

The compact formulation is:

Mathematics relative to Lean is an evolvingcontext-indexed, certified, hierarchical typed hypergraph.​​ 

Its nodes are typed constructions:

Γ⊢t\:A. 

Its primitive hyperedges are valid term constructors and inference instances.

Its named definitions and theorems are reversible compression boundaries.

Its theorem statements and proof bodies form separate but connected expression graphs.

Its proofs are rooted certified subhypergraphs.

Its alternative proofs are different routes to the same theorem type.

Its zoom levels are generated by choosing which declarations remain opaque.

Its contextual self-similarity is governed by substitution and abstraction, which category/type theory organizes.

Its exact formal validity comes from the Lean kernel.

Its human concepts, analogies, importance, and applications live in a provenance-aware semantic overlay.

MathRecord has not built this complete object. It has built and validated much of the exact raw material—particularly the environment, expression, and declaration layers—from which the first real hierarchical hypergraph can now be derived.

So I would no longer describe the project as:

> “Build a graph of theorem citations.”

I would describe it as:

> **Build the certified, recursively expandable mathematical structure implicit in Lean, then learn how to navigate and coarse-grain it.**

That is coherent, technically grounded, and sufficiently specific to construct and test.

**Confidence: 97%** that this is internally coherent as a representation program; **94%** that it accurately synthesizes the strongest ideas from the conversation; **90%** that MathRecord's E+X+D layers are the correct starting point for the first static hierarchical-hypergraph prototype; **72%** that this explicit structure will ultimately prove to be a substantially better learning substrate than strong hybrid token-based representations.

okay, just read through your previous response:  yes, it is a tree of heirarchies, primitives if you will, but isn't that what lean is already doing here? like nothing new (or am I missing something, i assume that I am)   the thing that isn't new is that we are throwing a stake in the ground with each theorem we declare. we don't need to double click on the at theorem all the way down to the primitives, because it has already been declared. Here is the intuition. if we keep using a theorem over and over again as a technique to prove other theorems, that theorem is probably important. yes it is a tree search, but figuring out the right 100k primitives is hopelessly unachievable. but if we have a theorem that sits as a key stepping stone, and we take it as black box, then we can use that. and if it is used by a lot of other proofs in the neighborhood of its goal or context, its likely that this might also be useful.   same story with definitions. we see definitions being very useful objects that have lots of inheret patterns.   in my mind I really see these hypergraphs. the first is that proofs themselves go all the way down to the primitives. definitions also are just collections of statements, repackaged. that also presents a hypergraph. finally, thereoms have a dependency structure, not just all the way down to the primitives, but one where we only let it go one level deep. i.e. this is a registered theorem. etc. and so we break it down to that theorem. and see how many theorems it cites.   so I guess all of mathematics at a certain level, could cite what building blocks it is founded on. so like we can choose the level we are looking at too... idk. I am getting a little lost and bogged down here. I just feel like my original insight as an undergrad was really good. what mathematicians are doing, is we have a repository of theorems in our belt, and we have an instinct of when to use them as tools or techniques. so in my mind if I was given a theorem, and I wanted to tell another mathematician in the least amount of words, how do you quickly prove this, I would give a list of theorems that I cite. If I have to figure it out on my own, what do I do? I think about the definitions, I think, okay what moves here have I done on other problems that put these hypothesis in a new interesting way? what do I know about proving convex functions? I could prove this or that instead, and thats sufficient... I basically look at my previous experience working with these objects, and I massage from both ends. if someone were to give me a hint, (use this theorem in the proof) that would be probably the most helpful bit of information. if I am workin from forwards and backwards, then that is most helpful. the objects we should be working with are these theorems, definitions, etc. and the way we have used them in the past are the key to proving new results. so a way to directly analyze which theorems are used when and where, that was the original insight. stripping away math at all levels down to just this concept was my idea, and I thought it was a great way to form a taxonomy of math as well. in a proof, what theorems were cited.   I realize that this is incomplete and insufficient to describe all of math. but maybe this is the right lens that can be materialized at different zoom levels of granularity. when you are getting stuck, zoom in more, when making lots of progress, zoom out. but maybe thats getting ahead of ourselves. the point is, in my head I had an intuition about which theorems, lemmas, and definitions to unfold when working through a problem. and that came from experience of "traversing the graph" before. so why not strip math down to this bare skeleton. and use lean as a reckoning.   this is what I felt good about: when you said this.   I now think the cleanest division is:  substrate local machinery navigation verification 	​  =typed, contextual, recursively expandable hypergraph, =type-theoretic inference + substitution + rewriting + composition, =search + retrieval + transport + abstraction, =Lean kernel. 	​  	​   so I want you to think one more time. think about everything. then explain it from the beginning. you have been saying a lot of things, and I think some of it is good. but I think we are not on the same page. so first truly understand what I am trying to say, then I want you to reflect on what you've been saying and tell me if there is a unifying middle ground.   then I need you to explain it all back to me, because I am truly lost from what you are trying to say or where you are coming from. I am going to disregard everything else you have said in the past, and I will let you justify what you are trying to say again from the beginning (after you have thought deeply about what I am trying to get at). then from there, bridge the gap and hand hold me. you know so much more math than me, I have the intuition, but you have the knowledge. I need you to remember that.

I think I understand the disconnect now.

I was answering a deeper question than the one you were actually asking.

I kept asking:

> What is the most foundational object from which every formal detail of mathematics can be reconstructed?

You were asking:

> What are the reusable units mathematicians actually think with, and how are those units connected through proofs?

Those are not the same question.

At the foundational level, Lean already has a typed term language, proof terms, contexts, substitution, and kernel verification. We do not need to rediscover that.

Your insight is about the **working abstraction level of mathematics**:

> Mathematicians primarily navigate through named definitions, lemmas, theorems, and techniques. A proof is built by selecting, instantiating, combining, and occasionally unfolding those reusable objects.

I now think that is the correct center of the project.

# Your original insight, stated cleanly

A mathematical library contains thousands or millions of named, verified objects:

D={d1​,d2​,…}. 

These include:

-  definitions; 
-  structures; 
-  lemmas; 
-  theorems; 
-  constructions; 
-  equivalences; 
-  algorithms; 
-  induction principles. 

Each one is a reusable tool.

When a theorem is proved and named, we have effectively turned a potentially enormous proof into a new one-step operation.

Suppose theorem L has a 500-step proof. Once Lean verifies it, future mathematicians do not usually redo those 500 steps. They invoke:

L. 

So a named theorem is something like a:

certified mathematical macro​ 

or:

cached verified subproof​. 

That is the “stake in the ground” you are describing.

Every declaration changes the future search space. A previously long route can now be crossed in one step.

This means a mathematical library is not merely a list of truths. It is an evolving collection of **reusable actions**.

That is a very strong insight.

# What Lean already does

Lean already stores the raw formal ingredients.

For a declaration d, Lean knows something like:

d:τd​:=pd​. 

Here:

- d is the name; 
- τd​ is its type or interface; 
- pd​ is its body, implementation, or proof certificate. 

For a theorem:

d:τd​ 

means that d is a proof of proposition τd​.

For a definition:

d:τd​:=pd​ 

means that d names a construction pd​ having type τd​.

Lean also knows which constants occur inside τd​ and pd​. It therefore already contains enough information to derive:

-  statement dependencies; 
-  proof dependencies; 
-  definition dependencies; 
-  exact term structure; 
-  theorem certificates. 

So, yes:

> **Lean already contains the underlying hierarchy.**

Nothing fundamentally new is being invented by saying that theorem bodies can be unfolded into smaller expressions.

Where your project becomes potentially new and useful is not in duplicating Lean's internal structure.

It is in turning those ingredients into the mathematical map that Lean itself does not provide.

Lean is the compiler and verifier.

It is not yet the Google Maps interface, the theorem-usage memory, or the learned navigation system.

# The right primary object is the declaration graph

The main objects mathematicians work with should be the named declarations:

d1​,d2​,…,dn​. 

Not every primitive kernel expression.

Those declarations are the abstraction boundaries that mathematicians have deliberately chosen over centuries.

A declaration should be treated as a black box by default.

Only unfold it when doing so becomes useful.

That is exactly how people work.

When proving something about convex functions, you do not begin by unfolding:

-  real numbers; 
-  addition; 
-  order; 
-  functions; 
-  logical implication; 
-  dependent types; 
-  kernel reduction. 

You begin with concepts such as:

-  convexity; 
-  subgradients; 
-  Jensen's inequality; 
-  affine maps; 
-  composition rules; 
-  epigraphs. 

Those are the available tools at the relevant scale.

Therefore the main graph should be declaration-centered.

# One theorem has three distinct faces

This distinction resolves much of the confusion.

Consider a theorem L.

It has three different roles in the system.

## 1. Its interface: how the theorem can be used

Suppose:

L\:P→Q→R. 

As a tool, L is a reusable inference rule:

{P,Q}L​R.​ 

This is a hyperedge.

It says:

> If you can provide P and Q, theorem L produces R.

More generally, a Lean theorem might have a type such as:

L:Πx\:A,P(x)→Q(x)→R(x). 

This represents a parameterized hyperedge schema:

{P(x),Q(x)}L​R(x).​ 

To use it, we choose a substitution such as:

x:=a. 

Then we obtain:

{P(a),Q(a)}L(a)​R(a). 

This is how the theorem participates in proof search.

## 2. Its certificate: how the theorem was proved

Suppose the registered proof of L cites:

A,B,C. 

Then there is a coarse proof-dependency hyperedge:

{A,B,C}pL​​L.​ 

This means:

> The registered certificate pL​ for theorem L directly references declarations A,B,C.

This is not the same as the interface edge.

The interface edge says:

> How can I use L?

The certificate edge says:

> How was L established?

That distinction is central.

## 3. Its internal proof

The certificate pL​ itself contains a more detailed structure:

-  several applications of A; 
-  a rewrite using B; 
-  a construction involving C; 
-  intermediate terms; 
-  substitutions; 
-  local assumptions. 

That gives a finer proof DAG or hypergraph.

So one theorem has:

interfacedirect proof dependenciesexact internal proof​​ 

These are three resolutions of the same declaration.

# The unified object is an AND–OR hierarchical hypergraph

I think this is the cleanest mature formulation.

Let the named declarations be the nodes.

For every known proof p of theorem T, create a labeled dependency hyperedge:

Supp(p)p​T, 

where:

Supp(p) 

is the set of named declarations directly referenced by p.

For example:

{L1​,L2​,D}p1​​T. 

Suppose there is another proof:

{K1​,K2​}p2​​T. 

Then T has two routes:

L1​\multicolumn3c↘↓↙\multicolumn3c↗↑K1​​L2​​DTK2​​​​ 

This has an **OR** structure at T:

> Choose proof p1​ or proof p2​.

Each chosen proof route has an **AND** structure:

> If you choose p1​, its dependencies L1​,L2​,D are jointly involved.

That gives an AND–OR hypergraph:

OR between alternative proofs;AND among the dependencies of one proof.​ 

That is a much more accurate version of the mathematical tree you first imagined.

The earlier outside review made the same core correction: proofs should be represented through labeled hyperedges preserving joint premises, while definitions act as compression operators that change the available node set. 

# The direct citation graph is the right default zoom

Suppose theorem T has proof:

pT​. 

At the default view, do not expand everything.

Display only:

Supp(pT​)pT​​T.​ 

This is the one-level graph you are describing.

It answers:

> What named tools did this proof directly rely on?

For a mathematician, that can be the highest-value summary.

If I tell you:

> Use Jensen's inequality and the supporting-hyperplane theorem,

I may have reduced a massive search problem to something manageable.

I have not given the whole proof.

But I have identified the important intermediate landmarks.

That is exactly why theorem hints are so powerful.

The direct citation graph is not a crude mistake.

It is a high-level map.

It only becomes inadequate when we mistake it for the complete proof.

# Zooming means changing which declarations are treated as black boxes

Let:

O⊆D 

be the declarations currently treated as opaque.

If:

L∈O, 

then display L as one node.

If:

L∈/O, 

expand L into the direct dependencies of its selected proof.

Therefore a view of theorem T depends on:

1.  which proof route we select; 
2.  which declarations we keep opaque. 

Call the view:

HO,ρ​(T), 

where:

- O is the opacity set; 
- ρ selects a proof route for each theorem being expanded. 

At the coarsest useful level, most named declarations are opaque:

{L1​,L2​,D}⇒T. 

Suppose L2​ is unfamiliar or seems to contain the hard part.

Expand only L2​:

L2​⇝{A,B,C}⇒L2​. 

Now the map becomes:

{L1​,A,B,C,D}⇒T 

with the internal grouping preserved.

You can continue selectively:

B⇝{X,Y}⇒B. 

This is not merely a single ladder of zoom levels.

It is a partially expanded map.

You expand the region where you are stuck and leave familiar mathematics compressed.

That is exactly how mathematicians read and construct proofs.

# There are three useful levels of proof description

I would now distinguish these clearly.

## Level 1: support set

Supp(p)={L1​,…,Lk​}. 

This tells you which named declarations the certificate directly references.

This is the shortest useful proof hint.

## Level 2: named application route

This records:

-  which theorem was used; 
-  where in the proof it was used; 
-  whether it was applied, rewritten, unfolded, specialized, or invoked by automation; 
-  which other named steps depended on it. 

This is the human-scale proof graph.

It might look like:

L1​→M←L2​, 

then:

M,D→T. 

This contains more structure than a citation set without descending to kernel details.

## Level 3: exact proof term

This is Lean's complete certificate:

p\:T. 

It includes all typing, substitutions, binders, applications, and term constructors necessary for verification.

The system should preserve all three:

support set↔named route↔exact proof term.​ 

That is the actual zoom hierarchy I think you want.

# Definitions fit the same framework—but they are not always collections of statements

Your intuition is operationally right, but there is one technical correction.

A definition can package:

-  a proposition; 
-  an object; 
-  a function; 
-  a structure; 
-  a construction; 
-  an invariant; 
-  a family of objects. 

For example:

Even(n):=∃k, n=2k 

packages a proposition pattern.

A group definition packages:

-  a carrier type; 
-  an operation; 
-  an identity element; 
-  an inverse; 
-  several laws. 

A Fourier transform definition packages a construction.

So I would not say:

> Definitions are collections of statements.

I would say:

> **Definitions are named mathematical interfaces backed by expandable formal bodies or packages.**

At graph level, however, your intuition survives.

A definition D is a named node:

D​. 

It has:

-  a type/interface; 
-  a body or generated package; 
-  statement dependencies; 
-  body dependencies; 
-  usage occurrences. 

At coarse resolution, D is a black box.

At finer resolution:

D⇝Hbody​(D). 

Definitions are especially important because they change the representation in which theorems become visible.

Sometimes a proof is hard because the right definition has not been unfolded.

Sometimes a proof is hard because too much has been unfolded and the useful abstraction has been destroyed.

Mathematical skill includes knowing which interfaces to preserve and which to open.

# What mathematicians are doing during proof search

Your description of forward and backward reasoning is exactly right.

Suppose the current goal is:

Γ⊢A. 

A theorem has type:

L:Πx,P1​(x)→⋯→Pk​(x)→Q(x). 

## Backward reasoning

Look for a substitution σ such that:

Q(σx)≈A. 

Then apply L.

The original goal becomes the subgoals:

P1​(σx),…,Pk​(σx). 

Graphically, you traverse the theorem hyperedge backward:

Q⇝{P1​,…,Pk​}. 

That is what happens when you think:

> “If I could apply this theorem, what would I still need to prove?”

## Forward reasoning

Look at facts already available in Γ.

If they match:

P1​(σx),…,Pk​(σx), 

then use L to derive:

Q(σx). 

Graphically, traverse forward:

{P1​,…,Pk​}⇝Q. 

That is what happens when you think:

> “What can I produce from what I already know?”

## Rewriting and unfolding

Sometimes the theorem does not visibly match the goal.

You then:

-  unfold a definition; 
-  fold an expression into a known concept; 
-  rewrite using an equality; 
-  change coordinates; 
-  prove an equivalent target; 
-  strengthen or weaken an intermediate statement. 

These operations modify the local representation until a useful theorem hyperedge becomes attachable.

That is your “massage from both ends.”

So the operative loop is:

​inspect hypotheses and goal→retrieve likely named tools→instantiate/apply/rewrite/unfold→obtain new hypotheses or subgoals→repeat.​​ 

This is extremely close to graph navigation.

# Where proof-state information actually belongs

You said you care less about the internal state of a proof.

I agree with that priority.

The proof state should not be the center of the global map.

The named declarations and their proof relationships should be the center.

But the local state is still important for one specific reason:

> It tells us **when** a theorem was useful.

The global dependency graph tells us:

> L was used somewhere in the proof of T.

That is useful but incomplete.

For learning mathematical intuition, we want a usage record such as:

u=(Γ⊢A,L,σ,role,result). 

This says:

-  the local assumptions were Γ; 
-  the current goal was A; 
-  theorem L was selected; 
-  it was instantiated by substitution σ; 
-  it was used as an application, rewrite, unfolding rule, etc.; 
-  it produced these new subgoals or facts. 

That is the machine-readable equivalent of mathematical experience.

So I would say:

> **Proof states are not the map. They are the training examples showing how mathematicians navigated the map.**

That is the middle ground.

We do not need to obsess over every kernel microstate.

We want the state near every meaningful named theorem or definition use.

# Your intuition about importance is also basically right

Suppose theorem L is repeatedly used in proofs involving similar goals and contexts.

Then:

Pr(L useful∣Γ⊢A) 

should be high in nearby situations.

That is premise selection.

But raw citation count is too crude.

A theorem like equality reflexivity may appear everywhere while carrying little domain-specific insight.

So importance should be conditional.

For a mathematical region R, define something like:

IR​(L)=Pr(L is used∣problem lies in R). 

A stronger definition would measure how much theorem L reduces future proof-search cost:

IR​(L)=Eq∼R​[C(q∣Σ∖{L})−C(q∣Σ)]. 

Interpretation:

> How much harder would problems in this region become if L were unavailable as a black-box tool?

That captures your idea of a load-bearing theorem.

Definitions can be evaluated similarly.

A useful definition is one that makes many important patterns easier to state, retrieve, or prove.

The broader review also converged on this compression-and-future-utility interpretation of mathematical importance. 

# Where category theory belongs

I previously made category theory sound like the central visual object.

I no longer think that is the best way to explain your project.

Category/type theory belongs underneath the navigation system.

Its job is to formalize:

-  contexts; 
-  substitutions; 
-  parameter instantiation; 
-  composition; 
-  transport; 
-  equivalence; 
-  generalization. 

A theorem is not usually one fixed edge:

P→Q. 

It is a parameterized schema:

Πx,P(x)→Q(x). 

Every actual use instantiates it differently.

The category-of-contexts perspective explains why these instantiations and substitutions compose coherently.

But the mathematician-facing map should still be the declaration hypergraph.

So:

MapLocal attachment rulesFormal foundation​=named definitions, theorems, and proof routes,=typing, substitution, unification, rewriting,=dependent type theory / Lean.​​ 

Category theory is structural plumbing.

It is important, but it does not need to dominate the interface or the initial representation.

# The unified middle ground

I would now define the object as follows.

For a fixed Lean environment Σ, construct:

GΣ​=(DΣ​,RΣ​,UΣ​,type,body,cert).​ 

Here:

### DΣ​: declaration nodes

Named definitions, lemmas, theorems, structures, constructors, equivalences, and related objects.

### RΣ​: certified routes

For every registered proof p\:T:

Supp(p)p​T. 

Alternative proofs produce alternative incoming hyperedges.

### UΣ​: use events

Records of when and how declarations were applied in local mathematical situations.

### type

The exact interface or theorem statement of every declaration.

### body

Its implementation or proof certificate when available.

### cert

The connection back to Lean verification.

The graph is hierarchical because every declaration can be treated as one node or expanded into its route/body.

It is contextual because theorem uses carry substitutions and local assumptions.

It is typed because every node and application has a Lean type.

It is certified because every exact route is backed by a Lean proof term.

It is multi-resolution because we can selectively alter the opacity set.

That is the unified representation I think you were reaching toward.

# What Lean provides and what our project provides

Lean already provides:

typed declarations+proof bodies+definitions+kernel checking.​ 

Existing tools also extract substantial portions of dependency information.

Our project would provide:

​declaration-centered hypergraph,alternative proof routes,selective recursive expansion,typed theorem-use records,context-conditioned importance and retrieval,human/agent navigation across abstraction levels.​​ 

So the foundational ingredients are not new.

The potentially valuable contribution is to **materialize and operationalize the abstraction structure mathematicians actually navigate**.

That is a very different claim from inventing a new foundation for mathematics.

# What MathRecord has built so far

MathRecord currently gives us much of the exact raw material:

-  environment identity; 
-  expression trees; 
-  declarations; 
-  declaration types; 
-  declaration bodies/proof terms; 
-  direct references; 
-  some proof-state and transition information. 

For your central vision, the most important part is:

E+X+D​ 

environment, expressions, and declarations.

That can generate:

-  theorem statement graphs; 
-  definition-body graphs; 
-  proof-body graphs; 
-  direct type dependencies; 
-  direct proof dependencies; 
-  one-level theorem citation graphs; 
-  recursive declaration expansion. 

The current system has **not yet built**:

-  the declaration-centered AND–OR hypergraph; 
-  named proof-route extraction; 
-  clean selective zoom; 
-  alternative-proof registration at scale; 
-  use-event extraction at meaningful theorem applications; 
-  contextual theorem-importance models; 
-  the learned navigation policy. 

So we have built the certified raw record.

We have not yet built the mathematical map.

# What I would build next

The next prototype should be declaration-centered, not proof-state-centered.

Take a bounded Lean corpus and give every declaration a page or node containing:

1.  Its exact type/interface. 
2.  Its direct type dependencies. 
3.  Its direct body/proof dependencies. 
4.  Its registered proof certificate. 
5.  Its theorem interface as a parameterized hyperedge. 
6.  Its direct proof-support hyperedge. 
7.  Exact selective expansion of any cited declaration. 
8.  Multiple proof routes where available. 
9.  Clear separation between exact Lean structure and inferred human labels. 

Then add meaningful use events:

> At this goal, theorem L was selected, instantiated this way, and produced these subgoals.

That would directly test and embody your original insight.

# The cleanest statement of your idea

I would now state it this way:

> **Mathematics is navigated through an evolving library of named, certified abstractions. Each theorem or definition is a reusable black-box tool backed by an expandable Lean certificate. Proofs compose instances of these tools into typed hypergraph routes. The direct declaration dependencies give the coarse mathematical map; selective unfolding provides finer resolution; records of past theorem use teach agents how to navigate the map in new contexts.**

Or even more compactly:

substratelocal machinerynavigationexperienceverification​=named certified declarations and their hierarchical routes,=typing, substitution, unification, rewriting, composition,=retrieve, apply, unfold, transport, introduce abstractions,=records of which tools worked in which contexts,=Lean kernel.​​ 

This is the middle ground.

Your original undergraduate insight was not that you had discovered Lean's kernel representation.

It was that:

> **The human-scale skeleton of mathematics is the network of reusable named abstractions and the patterns of how mathematicians invoke them.**

I think that is right.

It is incomplete as a metaphysical description of all mathematics, but it may be exactly the right operational lens for mathematical navigation and AI-assisted proof search.

**Confidence: 97%** that this now captures your original intuition accurately; **94%** that the declaration-centered AND–OR hierarchical hypergraph is the right explicit map to build next; **88%** that local theorem-use records are the critical bridge from static structure to learned mathematical intuition; **72%** that this representation will deliver a large improvement over strong text-plus-retrieval systems rather than a modest engineering gain.

That's right!  and in order to do this, I imagined a structure that is easy to navigate and relevant based on what objects you are working with, has nice properties, and the process is learnable as you go through proof states. so I guess the proof state is necessary, but you see the idea right? ya we need this thing that is very navigable. otherwise math will get more and more difficult.   so has anyone built this? if so, why is not the most important thing ever? we can learn it so I'm certain its learnable.  (note ideally, it is both locally navigable, and long range navigable. but the point is that the more alternative proofs we make, the more we connect disparate parts of mathematics with alternative proofs, the more connected we make math, the more we will be able to actually solve increasingly difficult things. the other thing I think is really important is the 5 different roles of math. this is not just for theorem proving, but for hypothesis generation, definition generation, etc. curation, etc. you know the old list I gave. but like ya, I think you are starting to see where it is going. 

Yes. I think I now see the full thing you are aiming at.

And my answer is:

> **No, I do not think anyone has built the whole thing.**
>
> Almost every component exists separately, and several 2026 projects are now surprisingly close. But I cannot find a system that combines the declaration-level mathematical map, local proof-state usage history, alternative-proof connectivity, multiscale zoom, long-range navigation, and the full “create definitions → propose statements → prove/refute → verify → curate” loop into one evolving learned mathematical substrate.

That distinction is why you have not heard about “the thing.” There isn't yet one thing to hear about.

## The idea as I now understand it

Forget kernel primitives as the main map.

The fundamental working objects should be the things mathematicians actually put in their toolbox:

definitions, lemmas, theorems, constructions, equivalences​ 

Call the current verified library:

Lt​. 

Every time someone proves and registers a useful theorem T, humanity has created a new reusable operation.

Instead of redoing:

500 proof steps 

we can now say:

apply T​. 

That changes the future search problem.

A library therefore isn't merely a database of facts. It is an **accumulated action vocabulary for doing mathematics**.

That, I think, is the center of your intuition.

---

## The map

For every theorem T, suppose one known proof uses:

L1​,L2​,D1​. 

Represent that as:

{L1​,L2​,D1​}p1​​T.​ 

Another proof might use:

{K1​,K2​}p2​​T.​ 

So globally we get an AND–OR hypergraph:

- **AND:** within one proof route, several tools are jointly involved. 
- **OR:** different proofs provide alternative routes to the same theorem. 

That's the coarse map.

And this is not far removed from what formal-library researchers are already extracting. TheoremGraph's LeanGraph now contains hundreds of thousands of Lean declarations and millions of typed dependency edges. But it is primarily a dependency/search infrastructure, not the complete navigation-and-learning system we're describing. 

---

## Then add zoom

Each theorem is a black box by default.

Suppose:

L2​ 

is familiar. Leave it alone.

Suppose:

L1​ 

is where you're confused.

Expand it:

L1​⇝{A,B,C}⇒L1​. 

Then perhaps expand B.

Thus the map isn't:

> “Unfold all mathematics to foundational primitives.”

It's:

> **Keep useful abstractions compressed and selectively open the part of the map where you need more resolution.**

That is exactly how mathematicians work.

And definitions participate identically:

D​↔its formal expansion. 

So the global structure becomes a recursively expandable theorem/definition hypergraph.

Astrolabe is interesting precisely because it independently lands on a content-addressed hypergraph with notions of width and depth, including a mathematics plugin. But it is a general semantic knowledge-management substrate, not yet the learned mathematical navigation system you have in mind. 

---

# The critical missing layer: experience

This is where proof state re-enters—and now I think we have it in the right place.

The graph says:

> Jensen's inequality was used in this proof.

But what you really want an agent to learn is:

> **Under what circumstances did mathematicians decide that Jensen's inequality was useful?**

So every important theorem-use should produce a training event like:

u=(Γ,A,L,σ,r)​ 

where:

- Γ = what was known; 
- A = what was being sought; 
- L = theorem/definition selected; 
- σ = how it was instantiated; 
- r = what happened next. 

That's mathematical experience.

The global graph tells you the road network.

The proof states tell you:

> **When people took which roads.**

That is almost exactly the data you would want to learn:

P(L∣Γ,A). 

Or more generally:

π(mathematical action∣Γ,A,L). 

This part absolutely already works in limited form. LeanDojo was built around fine-grained premise-use information and explicitly identified premise selection as a major bottleneck; retrieval-augmented proving significantly improved over non-retrieval approaches. 

More recent work goes even closer to your intuition. A graph-augmented premise selector combining text embeddings with relational dependency structure reported improvements of more than 25% across retrieval metrics over its language-based baseline. 

LeanHammer likewise learns context-dependent premise selection and reports that its learned selector improves goal solving relative to existing selectors across diverse domains. 

So the claim:

> **“We can learn which mathematical tools tend to be useful in which contexts.”**

is not speculative anymore.

That part is clearly learnable.

---

# Local navigation

This is the first navigation problem:

(Γ,A)⟶which declarations should I consider?​ 

Suppose you're proving something about:

-  convex functions; 
-  expectations; 
-  weighted sums. 

The system should know from past routes that this neighborhood strongly activates:

-  Jensen; 
-  convex-combination lemmas; 
-  affine maps; 
-  supporting hyperplanes; 
-  perhaps Hölder or AM-GM depending on the exact representation. 

This is analogous to having spent years proving similar problems.

It isn't merely lexical similarity.

The system learns:

> When these objects and goals co-occur, these mathematical moves tend to unlock progress.

LeanSearch v2 is already attacking a closely related problem called **global premise retrieval**: identifying the scattered collection of lemmas likely to support an entire proof. Its reasoning mode substantially improves retrieval and downstream proof success relative to no retrieval. 

So again:

> This part is real.

---

# Long-range navigation

This is the more exciting piece.

Suppose two regions are distant:

combinatoricsharmonic analysis. 

Then someone discovers a proof of theorem T using combinatorics.

Later another person proves T using harmonic analysis.

Now the same theorem has:

H1​→T 

and:

H2​→T. 

That gives the graph a new crosslink.

A theorem with proofs in multiple domains becomes something like a **bridge node**.

And the two proof routes expose a correspondence:

> Something about the structure in H1​ is playing the same mathematical role as something in H2​.

That's incredibly interesting.

With enough alternative proofs, we might discover patterns like:

A1​​A2​↓T​A3​​ 

and:

B1​​B2​↓T​B3​​ 

and ask:

> Why are the A's interchangeable with the B's here?

That starts to move beyond theorem retrieval into:

-  analogy; 
-  transport; 
-  representation changes; 
-  dualities; 
-  theory morphisms. 

This is where the graph could help find genuinely distant connections.

I would only add one qualification to your claim:

> More alternative proofs do not automatically make the graph more useful.

Ten essentially identical tactic variants don't add much.

But **structurally diverse alternative proofs** are extremely valuable.

So define proof diversity, perhaps through distances between their dependency supports:

d(Hi​,Hj​). 

A theorem with two short but structurally distant proofs may be much more informative than a theorem with 100 minor variants.

This is a great research target.

---

# And now the really important second loop

You are also correct that limiting this to proving would undersell the idea.

Once you have the evolving map Lt​, mathematical activity becomes something like:

Explore→Define→Conjecture→Shape→Prove/Refute→Verify→Curate.​ 

Your original five roles fit inside this.

### 1. Definition creation

The agent notices recurring structure and proposes:

D:=recurring pattern. 

This adds a new reusable black-box tool.

### 2. Hypothesis generation

The agent notices regularity:

perhaps P. 

Evidence might come from computation, analogies, failed proofs, graph neighborhoods, symmetries, or transferred patterns.

### 3. Goal construction

Turn the fuzzy hypothesis into an exact Lean statement:

Γ⊢P. 

Choose assumptions, generality, formulation, and objects.

### 4. Proof discovery

Navigate the map:

Γ⊢P 

using retrieval, substitutions, forward/backward search, rewriting, definitions, and existing theorem routes.

### 5. Verification

Lean checks:

p\:P. 

That should remain deterministic.

And then we discovered an indispensable sixth activity:

### 6. Curation

Ask:

> Does this new theorem/definition deserve to become a prominent reusable node?

Otherwise agents can generate effectively limitless formally valid junk.

The larger mathematical loop is therefore:

Lt​→new candidate structure→Lean verification→value judgment→Lt+1​.​ 

The external review you shared emphasized essentially the same point: validity and mathematical value are different problems, and curation may eventually be harder than verification. 

---

# Has anybody built the multi-role loop?

Pieces of it, yes.

Minimo is particularly relevant. It uses **the same model** to conjecture and prove within formal domains, starting from axioms and learning through intrinsic motivation. It demonstrated self-improvement in propositional logic, arithmetic, and group theory. 

STP similarly has a conjecturer and prover train one another through self-play and reports substantial improvements in theorem-proving performance. 

The Conjecturing-Proving Loop generates new Lean conjectures, proves them, then incorporates newly generated theorem-proof pairs into the context used for further discovery. 

And a June 2026 paper goes almost eerily close to your “stake in the ground” intuition: its system alternates proof search with extracting **useful intermediate theorems**, grows a reusable theorem library, and finds that those learned lemmas help solve subsequent benchmark problems. 

So the idea that:

> **Discovering and registering reusable intermediate theorems changes future proof ability**

already has empirical support.

That is significant.

But none of these systems has the full global map/navigation architecture you're describing.

---

# So what has actually not been built?

This is the clearest answer I can give.

I cannot find one system that simultaneously has:

1. **A Lean-certified declaration-centered AND–OR hypergraph.** 
2. **Recursive exact fold/unfold across theorem and definition boundaries.** 
3. **Alternative proof routes preserved as first-class objects.** 
4. **A history of theorem-use events conditioned on proof state.** 
5. **Learned local navigation over that map.** 
6. **Learned long-range navigation over graph structure.** 
7. **Structural proof-diversity and bridge detection.** 
8. **An evolving library where newly discovered abstractions alter future search.** 
9. **Definition generation, statement generation, proving, and refutation operating on the same representation.** 
10. **A validated curation/value model controlling what becomes part of the canonical map.** 
11. **Task-specific zoom from exact Lean structure to human-scale mathematical concepts.** 

Instead, today's landscape looks approximately like:

Lean/MathlibTheoremGraphLeanDojoLeanSearchAstrolabeMinimo/STPFormal ConjecturesMathRecord​verification + librarylarge dependency mapproof states + theorem usagepremise/navigation retrievalgeneric semantic hypergraphconjecture-prove learning loopresearch frontier registryour exact Lean-derived structural record​ 

Formal Conjectures now provides thousands of Lean-formalized research problems, including more than a thousand open conjectures, and has already been used as an interface for verified mathematical discovery. 

The full synthesis is missing.

---

# Why isn't this already the most important thing ever?

This is the part where I want to push back slightly on your certainty.

There are two answers.

## First: the pieces are incredibly recent

The field is moving into exactly this area **right now**.

TheoremGraph: June 2026. 

The mathematical-structure/hypergraph essay: April 2026. 

The Mathlib network analysis: April 2026. 

Formal Conjectures: May 2026. 

The theory-level-autoformalization argument that formalization should move from isolated statements to complete interdependent libraries: July 2026. 

So we're not looking at a mature twenty-year-old idea nobody cared about.

A lot of the required infrastructure became possible very recently.

## Second: nobody has demonstrated the knockout result

For this to become “the most important thing ever,” someone has to show something like:

> A learner using this structured mathematical map can solve problems or make discoveries that equally capable text/retrieval systems cannot.

We do have encouraging lower-level evidence.

Structural graph information improves premise selection. 

Retrieval dramatically helps proving. 

Agents can learn conjecturing and proving together. 

Self-discovered reusable theorems can improve later proof solving. 

But nobody has yet shown:

global structured mathematical map⇒qualitatively new mathematical intelligence.​ 

Until somebody does that, this looks like promising infrastructure and AI4Math research rather than a new operating system for mathematics.

---

# Is it learnable?

Parts of it: **yes, demonstrably**.

I would say with high confidence:

P(use theorem L∣Γ,A) 

is learnable.

We already have successful learned premise selection. 

Likewise:

P(next proof move∣Γ,A) 

is clearly learnable to a useful degree; essentially the entire modern neural theorem-proving field depends on this.

Conjecture difficulty/provability is also learnable enough to produce self-play curricula. 

What I am **not** willing to call certain yet is:

learnable local navigation⟹learnable global mathematical discovery. 

Or:

learned theorem usage⟹learned good definitions. 

Or:

graph centrality⟹mathematical importance. 

Those are the profound questions.

I think they're plausible.

But the right attitude is:

> We now have enough evidence that the hypothesis deserves to be tested aggressively.

Not:

> It must work.

That distinction will protect the project from becoming philosophy.

---

# One thing I think you're seeing that matters enormously

The graph is not static.

This is the conceptual point that has become clearer through our whole conversation.

Suppose today the shortest known route to T is:

A→B→C→D→T. 

Then someone proves:

L\:A→D. 

Now the effective map becomes:

AL​D→T. 

The mathematician just **changed the geometry of future mathematical search**.

Then another person introduces a definition X that compresses a recurring structure.

The geometry changes again.

Then someone finds an alternative proof using a distant theory.

Now two remote regions become connected.

So:

doing mathematics changes the map on which future mathematics is done.​ 

That is much more interesting than a static knowledge graph.

And it explains why your five roles belong together.

Proof discovery adds routes.

Definition discovery changes the node vocabulary.

Conjecture generation chooses unexplored destinations.

Goal shaping determines what destination is actually interesting.

Verification determines which routes are real.

Curation determines which routes and landmarks remain prominently on the map.

That's a closed ecosystem.

---

# The strongest formulation I have now

I would describe the eventual system this way:

> **A self-improving mathematical navigation substrate built around a certified, declaration-centered, hierarchical AND–OR hypergraph.**

It has three kinds of information.

### 1. The map

Gt​. 

Definitions, theorems, proof routes, alternative proofs, and fold/unfold relationships.

### 2. Experience on the map

Ut​={(Γ,A,L,σ,r)}. 

What tools were useful in what mathematical situations.

### 3. Evolution of the map

Gt​⟶Gt+1​. 

New definitions, conjectures, proofs, counterexamples, alternative routes, and curation decisions.

Then learned systems operate on the same substrate:

πnavigate​ 

selects useful existing tools;

πprove​ 

constructs routes;

πdefine​ 

proposes useful abstractions;

πconjecture​ 

proposes destinations;

Vcurate​ 

estimates what deserves to become a long-term landmark.

And:

Lean certifies the exact layer underneath all of them.​ 

That's the full thing.

---

## And why I think your original intuition remains important

Your undergraduate insight was not:

> “Proofs depend on earlier theorems.”

That's obvious and old.

It was closer to:

> **The dependency/use structure is itself a computational object worth learning. Mathematical intuition may largely consist of knowing which reusable abstractions become relevant in which local situations, and a globally organized history of those uses could give both humans and machines access to mathematical experience no individual can accumulate.**

That is substantially more interesting.

It explains both:

-  the grocery store for humans; 
-  the training substrate for agents. 

And that exact synthesis is the part I do **not** see built yet.

My best current probabilities:

- **95%:** theorem/definition relevance is learnable from structured usage history. 
- **80%:** explicit graph + usage structure will materially improve some local mathematical navigation tasks over text alone. 
- **60%:** it enables meaningful long-range transfer/bridge discovery beyond today's retrieval systems. 
- **40%:** a common substrate can successfully support proving + conjecturing + abstraction invention + curation at research-math scale. 
- **15–25%:** this becomes a genuinely transformative mathematical infrastructure rather than an important but incremental AI4Math tool. 

That last probability is not small. For something this ambitious, I think it's enormous.

**Confidence in the landscape assessment: 94%.**