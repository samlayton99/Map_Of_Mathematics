Below is a “real” program you can actually follow: sequencing, timeboxing, projects, tools, and what “mastery” means. It’s designed for someone with mathematical maturity who wants to become a genuinely excellent software engineer in the modern era (large codebases, scalability, maintainability, production, AI-native workflows), without wasting time on things likely to be commoditized.

I’ll assume you can do ~10–15 hours/week. At that pace this is ~12–18 months. If you can do ~20 hours/week, you can compress to ~9–12 months.

---

## Program design principles

**The output is not course completion. The output is engineering competence.** So the program is built around a single “spine” codebase that grows across courses, plus a few focused side projects when the spine is the wrong venue.

**Language spine (conservative, high ROI):** Python → TypeScript → Rust → Go → SQL (with Bash/Unix throughout).

**What we de-emphasize (AI will erode):** syntax memorization, CRUD boilerplate, framework-of-the-year depth, “toy” greenfield assignments with no maintenance.

**What we emphasize (AI will not erase):** specs, interfaces, invariants, debugging, performance, concurrency, distributed failure, observability, migrations, refactors, and judgment.

---

## The spine project you’ll carry through the whole program

Build a production-grade system you *maintain* over time. Example:

**“Atlas”**: a multi-tenant collaboration + task + knowledge system

* Web UI (TypeScript), API service(s), background jobs, Postgres, caching, search, file storage, event log, analytics
* CI/CD, Docker-based dev env, migrations, observability (metrics/logs/traces), on-call-style incident drills
* Clear boundaries: “core domain,” “platform,” “integration,” “UI,” “infra”
* You will deliberately refactor it, split it, migrate schemas, and operate it

You’ll also do one required external open-source contribution late in the program.

---

## Suggested sequence (followable)

I’d run this as 6 “terms” of 6–8 weeks each. Each term is 2–4 courses running in parallel with one major deliverable.

### Term 0 (2 weeks): Setup sprint

* Developer Environment, Toolchain, and Open Source Practice (Course 3)

### Term 1 (6–8 weeks): Programming as disciplined craft

* Programs, State, and Abstraction (Course 1)
* Software Construction and Maintainability (Course 4)
* Reasoning About Programs and Computation (Course 2)

### Term 2 (6–8 weeks): Algorithmic judgment + language power

* Data Structures and Algorithmic Engineering (Course 5)
* Programming Languages, Type Systems, and Interpreters (Course 7)

### Term 3 (6–8 weeks): Machines and concurrency

* Computer Systems from the Programmer’s View (Course 6)
* Concurrency, Async I/O, and Parallelism (Course 8)
* Operating Systems and Runtime Systems (Course 9)

### Term 4 (6–8 weeks): Systems that talk and store

* Networks and Internet Systems (Course 10)
* Databases and Data-Intensive Systems (Course 11)
* Testing, Debugging, Static Analysis, Lightweight Formal Methods (Course 12)

### Term 5 (6–10 weeks): Scale, reliability, and AI-native workflows

* Large Codebase Engineering, Architecture, and Refactoring (Course 13)
* Distributed Systems and Cloud Platforms (Course 14)
* Performance, Reliability, and Observability (Course 15)
* AI-Native Software Engineering (Course 16)

### Term 6 (8–12 weeks): Practicum (the “real world”)

* End-to-End Production Practicum I (Course 17)
* End-to-End Production Practicum II (Course 18)

---

# Course-by-course details (objectives, topics, deliverables)

I’ll keep a consistent format so this reads like a curriculum, not a blog post.

---

## 1) Programs, State, and Abstraction

**Goal:** turn ambiguous problems into clean, correct programs with good structure.

**Prereq:** none.

**You should be able to do, by the end:**
Write 1–3k LOC programs that are readable, tested, and decomposed into modules with clear boundaries, without getting lost in state.

**Core topics (in the order I’d teach them):**

* Data modeling: choosing representations; making illegal states unrepresentable (where feasible)
* Control flow and state: pure vs impure; mutation; scoped state; lifetimes of data
* Functional patterns that matter in practice: map/filter/reduce; iterators; closures; immutability as a design tool
* Error handling: exceptions vs result types; failure modes; retries vs hard failures
* Decomposition: functions, modules, packages; dependency direction; “who knows what”
* Testing basics: unit tests that don’t rot; fixtures; avoiding brittle tests
* Debugging fundamentals: reading tracebacks; stepping with a debugger; logging with intent
* Complexity basics: big-O as a rough tool; when it matters

**Tools:** Python 3.12+, pytest, ruff, mypy (light use), uv/venv, VS Code/PyCharm, git.

**Deliverables:**

1. A CLI tool that processes real data (e.g., log analyzer, markdown publisher, CSV pipeline) with tests and docs.
2. First “Atlas” component: a small domain module (tasks/notes/users) with clean interfaces and tests.

**Mastery checks:**
You can explain invariants, show tests that catch regressions, and refactor without breaking behavior.

---

## 2) Reasoning About Programs and Computation

**Goal:** give you durable “programmer’s theory” that improves correctness and judgment.

**Prereq:** Course 1 (or equivalent).

**You should be able to do:**
Write correctness arguments for core logic, recognize undecidable/uncomputable boundaries, and reason about complexity *without* turning software into pure math.

**Core topics:**

* Specifications and invariants (loop invariants, data invariants, representation invariants)
* Induction as a programming tool (recursive correctness; structural induction on trees/graphs)
* Complexity: asymptotics, amortized analysis, randomized reasoning (high-level)
* Graphs as the universal modeling tool (reachability, shortest paths, topological constraints)
* Computability: what cannot be automated; reductions as “impossibility transfer”
* Practical correctness: pre/postconditions; contracts; where formalism pays

**Deliverables:**

* Prove correctness (informally but rigorously) for 2–3 algorithms you implement in Course 5.
* Write a spec (not code) for a subsystem in Atlas and identify its invariants and failure modes.

**Mastery checks:**
You can articulate the invariant behind a design and point to where it’s enforced in code/tests.

---

## 3) Developer Environment, Toolchain, Build/Release, and Open Source Practice (Setup Sprint)

**Goal:** make you operationally fluent so you stop bleeding time on basics.

**Prereq:** none.

**You should be able to do:**
Set up a professional dev environment on macOS/Linux, contribute to an open-source project via PR, and run a repo with CI, formatting, testing, releases.

**Core topics:**

* Shell literacy: pipes, processes, permissions, grep/sed/awk basics, SSH, tmux
* Git beyond basics: branching models, rebasing vs merging, bisect, blame, reflog, submodules (just awareness)
* Editor/IDE setup: debugging, test runner integration, language servers, keybindings, snippets
* Build and packaging: Python packaging basics, Node workspace basics, Rust/Go build basics
* CI/CD fundamentals: lint/test gates, caching, artifacts, release tags, semantic versioning
* Containers: Docker images, compose, networking, volumes; devcontainers as optional
* Open source norms: issues, triage, contributing guides, maintainers, etiquette, changelogs

**Deliverables:**

* A “workstation bootstrap” repo: dotfiles + setup scripts + documentation.
* Convert Atlas into a reproducible dev environment (one command to run tests; one command to run services).
* One micro PR to a real open-source repo (docs fix or small bug) to learn the workflow.

**Mastery checks:**
You can clone, run, test, and contribute to an unfamiliar repo without flailing.

---

## 4) Software Construction and Maintainability

**Goal:** build software that survives contact with time, teammates, and changing requirements.

**Prereq:** Course 1 + Course 3.

**You should be able to do:**
Design stable APIs, build maintainable modules, and enforce quality through tests, typing, linting, and review.

**Core topics:**

* Interface design: stable boundaries; dependency inversion; error surfaces
* Type-driven development (practical): using types to prevent classes of bugs (TS + some Python typing)
* Code organization patterns: layering, hexagonal/clean-ish architecture (without ideology)
* Refactoring mechanics: extracting seams, deprecations, migration paths
* Testing strategy: unit vs integration; contract tests; test isolation
* Documentation that pays: READMEs, ADRs, design docs, docstrings, examples
* Human systems: code review checklists; PR hygiene; commit discipline

**Tools:** TypeScript, Node, pnpm, ESLint/Prettier, Vitest/Jest, OpenAPI tooling (light), Python + mypy (moderate).

**Deliverables:**

* Build Atlas API (initial monolith): authentication, multi-tenancy model, tasks CRUD, minimal UI.
* Introduce “definition of done”: CI gates, formatting, tests, basic docs.

**Mastery checks:**
You can hand the repo to a strong engineer and they can navigate it fast.

---

## 5) Data Structures and Algorithmic Engineering

**Goal:** algorithmic judgment for real systems.

**Prereq:** Course 1 (Course 2 helps).

**You should be able to do:**
Choose the right representation and algorithm under performance, memory, and complexity constraints.

**Core topics:**

* Hashing, maps/sets; collision behavior; load factors
* Heaps, priority queues; scheduling and simulation use cases
* Trees (B-trees awareness later), tries, union-find
* Graph algorithms that show up constantly: BFS/DFS, shortest paths, DAG scheduling
* Dynamic programming as caching; when it’s overkill
* Streaming and sketches (basic): approximate distinct counts, reservoir sampling (optional but high leverage)
* Practical profiling mindset: don’t guess, measure

**Deliverables:**

* Implement a library of DS/algorithms with tests and small benchmarks.
* Apply to Atlas: e.g., build a fast search/index module (in-memory first), rate limiter, or scheduling subsystem.

**Mastery checks:**
You can justify choices in terms of asymptotics *and* constants and operational context.

---

## 6) Computer Systems from the Programmer’s View

**Goal:** understand what your code becomes and why performance/bugs happen.

**Prereq:** Course 1.

**You should be able to do:**
Reason about memory layout, stack/heap behavior, compilation/linking, and low-level performance costs.

**Core topics:**

* Bits/bytes, endianness, integer overflow, floating point reality
* Call stack, heap allocation, object layout; pointers/references
* Compilation pipeline: source → IR → machine; linking; symbol resolution
* CPU caches, locality, branch prediction (conceptual)
* Debugging native crashes: stack traces, core dumps (basic), sanitizers
* “Just enough assembly” to read compiler output (the x-ray, not the lifestyle)

**Tools:** C (minimal), Rust (preferred), compiler flags, gdb/lldb, perf basics.

**Deliverables:**

* Write a small memory allocator or arena (simplified).
* Build a performance-sensitive component in Rust (e.g., parsing/serialization) used by Atlas.

**Mastery checks:**
You can explain why something is slow in terms of memory and I/O, not vibes.

---

## 7) Programming Languages, Type Systems, and Interpreters

**Goal:** become the kind of programmer who can *design* abstractions, not just use them.

**Prereq:** Course 1.

**You should be able to do:**
Build a small language runtime, understand parsing/ASTs, and use type systems as design tools.

**Core topics:**

* Parsing: recursive descent; ASTs; syntax vs semantics
* Interpretation: environments, closures, scoping, evaluation strategies
* Types that matter: generics, unions, ADTs, variance (practical), effect-ish thinking
* Runtime issues: memory management basics, recursion, tail calls (awareness)
* Language design tradeoffs: expressiveness vs safety vs complexity

**Tools:** Rust or TypeScript for the interpreter; property-based tests for parser/interpreter correctness.

**Deliverables:**

* Build “MiniLang”: expressions, functions, records, pattern matching (optional), errors.
* Apply insights to Atlas: tighten APIs/types, reduce runtime errors via type modeling.

**Mastery checks:**
You can read a new language and quickly grok its semantics and design tradeoffs.

---

## 8) Concurrency, Async I/O, and Parallelism

**Goal:** write correct and scalable concurrent systems.

**Prereq:** Course 6 strongly recommended.

**You should be able to do:**
Build systems with concurrency without race conditions, deadlocks, or uncontrolled fanout.

**Core topics:**

* Threads vs async; shared memory vs message passing
* Locks, atomics, channels; deadlocks and avoidance
* Structured concurrency; cancellation; timeouts; backpressure
* Work queues and worker pools; rate limiting; circuit breakers
* Data parallelism vs task parallelism
* Debugging concurrency: tracing, deterministic tests, stress tests

**Tools:** Go (goroutines/channels), Rust (tokio + ownership), profiling tools.

**Deliverables:**

* Build a concurrent job runner (with retries, cancellation, timeouts).
* Integrate background jobs into Atlas (emailing, indexing, scheduled tasks).

**Mastery checks:**
You can explain and test your concurrency model and its failure behavior.

---

## 9) Operating Systems and Runtime Systems

**Goal:** understand the OS and runtime substrate your software stands on.

**Prereq:** Course 6.

**You should be able to do:**
Explain scheduling, virtual memory, filesystems, and runtime memory management, and diagnose OS-level performance/pathology.

**Core topics:**

* Processes/threads, scheduling basics, context switching
* Virtual memory, paging, memory mapping; file I/O
* Filesystems: journaling concepts, durability vs performance tradeoffs
* Isolation: permissions, namespaces/containers concepts
* Runtime systems: garbage collection vs ownership; allocators; JIT awareness
* Practical ops: load, memory pressure, file descriptor exhaustion

**Deliverables:**

* Write small “OS labs”: toy shell, toy filesystem abstraction, concurrency primitives (simplified).
* Instrument Atlas to detect and report OS-level limits (fds, memory).

**Mastery checks:**
You can reason about resource leaks and system-level bottlenecks competently.

---

## 10) Networks and Internet Systems

**Goal:** build networked software that behaves well on the real internet.

**Prereq:** Course 8 helps.

**You should be able to do:**
Design robust APIs with retries/timeouts, handle partial failure, and understand why latency dominates.

**Core topics:**

* TCP/UDP basics; congestion and latency intuition
* HTTP lifecycle; headers; caching semantics; idempotency
* DNS, TLS basics (no deep security course, but practical understanding)
* API design: REST vs RPC; pagination; versioning; compatibility
* Distributed failure patterns: retries, timeouts, jitter, hedging, fallbacks
* Queues and pub/sub as networked design tools

**Tools:** Go for services, curl, mitmproxy/Wireshark (light), load testing.

**Deliverables:**

* Implement an API gateway or service boundary in Atlas.
* Introduce rate limiting + request tracing across calls.

**Mastery checks:**
You stop “accidentally DDoSing yourself” and your APIs are stable under client misuse.

---

## 11) Databases and Data-Intensive Systems

**Goal:** database competence at both usage and internal behavior levels.

**Prereq:** Course 4.

**You should be able to do:**
Design schemas, write good SQL, understand indexes/transactions, and execute migrations safely.

**Core topics:**

* Relational modeling; constraints; normalization (pragmatic, not dogmatic)
* SQL mastery: joins, window functions, CTEs, query plans
* Indexes: B-trees conceptually; selectivity; composite indexes
* Transactions: isolation levels, anomalies, locks
* Migrations: forward/backward compatible schema changes
* Beyond relational: key-value, document, log-structured; when to use them
* Caching patterns: read-through, write-through, invalidation pain

**Tools:** Postgres, migrations (Flyway/Liquibase or Prisma/Drizzle), EXPLAIN, connection pooling.

**Deliverables:**

* Atlas: multi-tenant schema + migrations + query tuning for one slow query.
* Build a small storage engine toy (optional) or write a simplified log-structured store.

**Mastery checks:**
You can explain a slow query using its query plan and fix it with data/index changes.

---

## 12) Testing, Debugging, Static Analysis, Lightweight Formal Methods

**Goal:** become the person who can keep systems correct as they evolve.

**Prereq:** Courses 4–5.

**You should be able to do:**
Build verification harnesses that make refactors safe and catch subtle bugs early.

**Core topics:**

* Testing pyramid done right; integration testing without flakiness
* Property-based testing; fuzzing concepts; metamorphic tests
* Static analysis: linters, type checkers, invariants, contracts
* Runtime checking: assertions, sanitizers, feature flags
* Debugging workflow: bisect, repro minimization, tracing
* Lightweight formal: state machines, temporal thinking (TLA+ concepts), spec-first for protocols

**Deliverables:**

* Add property tests for critical Atlas modules.
* Write a small spec (state machine + invariants) for a workflow like “task assignment” or “billing-like ledger” and validate it with tests.

**Mastery checks:**
You can design tests that survive refactors and catch “impossible” edge cases.

---

## 13) Large Codebase Engineering, Architecture, and Refactoring

**Goal:** learn to work inside big systems without breaking them.

**Prereq:** Atlas has to exist by now.

**You should be able to do:**
Map dependencies, write migration plans, implement deprecations, and refactor safely.

**Core topics:**

* Architectural boundaries: layering, domain boundaries, service cuts
* Dependency graphs; build graph health; modularization strategies
* RFCs/ADRs; technical decision-making; long-lived documentation
* Refactor playbooks: seams, strangler patterns, codemods, “dual write” migrations
* Ownership models: teams, modules, CODEOWNERS, review rules
* Developer experience: internal tooling, templates, scaffolding

**Deliverables:**

* Take one messy Atlas subsystem and redesign it with an ADR + migration plan.
* Execute a multi-step refactor with compatibility preserved throughout.

**Mastery checks:**
You can improve the system without “big-bang rewrite” fantasies.

---

## 14) Distributed Systems and Cloud Platforms

**Goal:** understand multi-machine systems and how they fail.

**Prereq:** Courses 10–11.

**You should be able to do:**
Design services with replication, partitions, and partial failure in mind.

**Core topics:**

* Core truths: time, clocks, partitions, and failure are unavoidable
* Consistency models; replication strategies; leader/follower
* Consensus concepts (not a full proof course): what it solves, what it costs
* Sharding and rebalancing; id generation; hotspot handling
* Messaging semantics: at-most/at-least/exactly-once (practical reality)
* Cloud primitives: containers, orchestration concepts, infra as code, managed services tradeoffs

**Tools:** Docker, Kubernetes concepts (can be local kind/minikube), Terraform/Pulumi (light but real).

**Deliverables:**

* Split Atlas into at least two services or components (e.g., API + worker) with reliable messaging.
* Implement “exactly-once-ish” processing with idempotency keys and dedupe.

**Mastery checks:**
You design around failure instead of being surprised by it.

---

## 15) Performance, Reliability, and Observability

**Goal:** make systems fast, stable, and diagnosable.

**Prereq:** Courses 10–14.

**You should be able to do:**
Measure performance, identify bottlenecks, and run incident-style debugging.

**Core topics:**

* Benchmarking methodology; profiling; flamegraphs; regression detection
* Latency budgeting; queueing intuition; tail latency
* Caching and invalidation strategy; load shedding
* Observability: logs, metrics, tracing; correlation IDs; sampling
* Reliability: SLOs, error budgets (conceptually), incident response, postmortems
* Capacity planning basics; cost vs performance tradeoffs

**Tools:** OpenTelemetry, Prometheus/Grafana (or equivalent), structured logging, load testing.

**Deliverables:**

* Instrument Atlas with traces + dashboards.
* Run a controlled “incident”: inject latency/errors, detect, mitigate, and write a postmortem.

**Mastery checks:**
You can answer “what happened?” quickly and confidently.

---

## 16) AI-Native Software Engineering

**Goal:** make AI a force multiplier without surrendering judgment.

**Prereq:** Courses 3–4 (and ideally you’re already using AI day-to-day).

**You should be able to do:**
Use coding agents to accelerate work while keeping correctness, maintainability, and security baseline intact.

**Core topics:**

* Prompting as specification: making tasks verifiable; defining acceptance criteria
* Repo context management: documentation for agents, project maps, “how to run” instructions
* Diff supervision: reviewing machine code; spotting subtle bugs; avoiding style drift
* AI-driven refactors and migrations: codemods, test amplification, doc generation
* Evals for engineering: unit/integration harnesses as “truth,” synthetic repros
* Boundaries: what not to delegate; how to “trust but verify”

**Deliverables:**

* Produce an “agent playbook” for Atlas: how to run, how to test, how to propose changes.
* Use an agent to do a non-trivial refactor, but require tests + review rubric + postmortem of what it got wrong.

**Mastery checks:**
You can reliably get speedups without increasing defect rate.

---

## 17) End-to-End Production Practicum I

**Goal:** design and ship a v1 of a real system with production standards.

**You should be able to do:**
Deliver a cohesive product slice: UI + API + persistence + ops readiness.

**Core components:**

* Written design doc, API contract, schema, deployment plan
* CI, integration tests, observability, docs
* User-facing “happy path” plus basic reliability features (retries, timeouts, idempotency)

**Deliverable:**
Ship Atlas v1 as a deployed service (even if only self-hosted), with a runbook.

---

## 18) End-to-End Production Practicum II

**Goal:** learn maintenance under pressure.

**Core components:**

* Midstream requirement changes
* Dependency upgrades and breaking changes
* Data migrations with rollback strategy
* “On-call” drills: incidents, postmortems, reliability improvements
* One external open-source contribution of meaningful size (not just docs)

**Deliverable:**
Atlas v2 with measurable improvements (performance, reliability, maintainability), plus a portfolio-quality engineering write-up.

---

# How to grade yourself (so this stays real)

If you want this to be “best-in-the-world,” you need clear gates. By the end, you should be able to do these without heroics:

1. Clone a medium-to-large repo and become productive in a day.
2. Design an API + schema that survives iteration and migration.
3. Debug a production issue with tracing/logs and fix it safely.
4. Add concurrency without race conditions and with tests that catch regressions.
5. Make performance improvements with evidence (profiles + benchmarks).
6. Use AI tools to go faster while maintaining a high bar for correctness and code health.

---

If you want, I can also turn this into a week-by-week syllabus (readings, exact projects, checkpoints, and recommended “canonical” references per course) tailored to your preferred stack: (A) startup SaaS, (B) infrastructure/platform, or (C) systems-heavy (Rust-first).

**Confidence: 88%**
