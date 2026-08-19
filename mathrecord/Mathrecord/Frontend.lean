import Lean

/-! Minimal frontend driver: elaborate a Lean source file in-process and return
the resulting `Environment`, `InfoTree`s, and message log. This is the access
path to exact elaboration data (local contexts, goals, tactic states) without
any pretty-printer parsing. -/

namespace Mathrecord

open Lean Elab

structure ProcessedFile where
  env      : Environment
  trees    : List InfoTree
  messages : MessageLog
  fileName : String

/-- Elaborate `path` and capture environment, info trees, and messages.
`opts` mirrors the project's `leanOptions` (e.g. Mathlib's `autoImplicit false`)
so elaboration matches the corpus project's own build semantics. -/
def processFile (path : System.FilePath) (opts : Options := {}) : IO ProcessedFile := do
  let input ← IO.FS.readFile path
  let fileName := path.toString
  let inputCtx := Parser.mkInputContext input fileName
  let (header, parserState, messages) ← Parser.parseHeader inputCtx
  let (env, messages) ← Elab.processHeader header opts messages inputCtx
  let env := env.setMainModule (Name.mkSimple (path.fileStem.getD "Main"))
  let cmdState := Command.mkState env messages opts
  let cmdState := { cmdState with infoState := { cmdState.infoState with enabled := true } }
  let s ← Elab.IO.processCommands inputCtx parserState cmdState
  return {
    env      := s.commandState.env
    trees    := s.commandState.infoState.trees.toList
    messages := s.commandState.messages
    fileName := fileName
  }

end Mathrecord
