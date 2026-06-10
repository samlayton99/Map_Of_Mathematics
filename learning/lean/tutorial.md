
### Project Setup
To start a Lean project:

```

lake new project_name math
cd project_name
cursor . # (if you don't already have it open)

```

This creates a Lean project with mathlib configured and opens the project root so dependencies resolve correctly.

Next download the precompiled mathlib artifacts and build the project:

```

lake exe cache get
lake build

```

Then, at the top of your Lean file, include:

```

import Mathlib

```

### Common Lean Libraries

Lean projects typically rely on a small set of core libraries:

- `Mathlib` — the main mathematics library (algebra, analysis, topology, number theory, combinatorics, etc.) and the standard starting point for most proofs.
- `Std` — Lean’s standard utility library (data structures, algorithms, collections, basic programming utilities).
- `Batteries` — lightweight functional programming utilities and extensions to the Lean standard library.

In most proof-oriented projects, simply importing:

```
Mathlib
```

is sufficient, since `Mathlib` already depends on and includes functionality from `Std` and `Batteries`.


### Theory
Program == Expression. A series of steps to execute to evaluate to an expression/answer. 

Programs run steps. This steps can either evaluate to a simplified expression, and/or they can have side effects. 

Think about running a program or 'computing' as evaluating this expression. Programs/evaluations can have side effects (writing a file, std operations, etc.), but like a math expression, lean is not designed for that explicitly.

Note that lean variables cannot be reassigned. Lean is restricted that its memory is not mutable and its expressions try not to have side effects.


### General tips
- Always open the **project root** (`cursor .`) so Lean can detect the toolchain and dependencies.
- When you open a `.lean` file, the **InfoView** should appear automatically.
- If InfoView is closed, reopen it with **Cmd + Shift + P → "Infoview: Toggle Infoview"** or **Cmd + Shift + Enter**.
- Use `lake build` anytime dependencies change or the project needs a full rebuild.