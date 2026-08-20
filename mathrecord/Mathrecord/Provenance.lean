import Mathrecord.Frontend
import Mathrecord.Extract

/-! Elaboration-provenance sidecar (Phase 4).

A separate channel from the kernel record: what the SOURCE, as resolved by
the elaborator, actually referenced — independent of what survives in the
final proof term. Never mixed into the canonical kernel structure.

Per declaration in one file:
  refs     resolved global constants whose use site is a source identifier
           (InfoTree TermInfo nodes with `.const` expressions and ident
           syntax), with occurrence counts
  tactics  tactic syntax kinds observed inside the declaration, with counts

Uses: extraction-independent recall ground truth; tactic-heavy proofs;
written-move vs surviving-kernel-move comparison; intent provenance.
-/

namespace Mathrecord.Provenance

open Lean Elab Mathrecord

partial def collectInfos (t : InfoTree) (ctx? : Option ContextInfo := none) :
    List (ContextInfo × Info) :=
  match t with
  | .context pctx t => collectInfos t (pctx.mergeIntoOuter? ctx?)
  | .node i cs =>
    let rest := cs.toList.flatMap (collectInfos · ctx?)
    match ctx? with
    | some ctx => (ctx, i) :: rest
    | none => rest
  | .hole _ => []

def provenance (path : System.FilePath) (out : System.FilePath) : IO Unit := do
  let pf ← Mathrecord.processFile path
  let mut refs : Std.HashMap Name (Std.HashMap Name Nat) := {}
  let mut tacs : Std.HashMap Name (Std.HashMap Name Nat) := {}
  for tree in pf.trees do
    for (ctx, info) in collectInfos tree do
      let decl := ctx.parentDecl?.getD Name.anonymous
      match info with
      | .ofTermInfo ti =>
        if ti.stx.isIdent then
          if let .const c _ := ti.expr then
            let m := refs.getD decl {}
            refs := refs.insert decl (m.insert c (m.getD c 0 + 1))
      | .ofTacticInfo ti =>
        let k := ti.stx.getKind
        let m := tacs.getD decl {}
        tacs := tacs.insert decl (m.insert k (m.getD k 0 + 1))
      | _ => pure ()
  let declNames := (refs.keys ++ tacs.keys).eraseDups
  let decls := declNames.map fun d =>
    let rj := (refs.getD d {}).toList.map fun (c, k) => (toString c, Json.num k)
    let tj := (tacs.getD d {}).toList.map fun (c, k) => (toString c, Json.num k)
    Json.mkObj [("name", Json.str (toString d)),
                ("refs", Json.mkObj rj),
                ("tactics", Json.mkObj tj)]
  let j := Json.mkObj [
    ("schema", Json.str "mathrecord-provenance-0.1"),
    ("file", Json.str path.toString),
    ("channel", Json.str "elaboration-provenance (sidecar; not kernel content)"),
    ("decls", Json.arr decls.toArray)]
  IO.FS.writeFile out (j.pretty ++ "\n")
  IO.println s!"provenance {path} -> {out} ({decls.length} decls)"

end Mathrecord.Provenance
