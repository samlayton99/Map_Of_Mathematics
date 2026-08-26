#!/usr/bin/env python
"""Deliverable A: source-accessibility audit of every discovered proof.

For each solved theorem in a prover output file, check every constant of
the discovered proof term against the CONSERVATIVE universe (transitively
imported modules; own module excluded).  Because an accessible lemma's own
dependencies lie inside its module's import closure, which is contained in
ours, auditing the proof term's direct constants is sound and complete for
term-level dependencies.  This catches the unaudited channels: global
[simp] lemmas, synthesized instances, coercions - and any use of the
target theorem itself or its file siblings.

Pass condition (per handoff): ZERO forbidden dependencies in counted
solutions.

Run: ~/venv/general_ml/bin/python proof_audit.py prover_out_v2_sbrp.jsonl ...
Writes tools/output/proof_accessibility_audit.json
"""
import json
import sys
import time
from pathlib import Path

import numpy as np

from atlas import load_dump, BIG
from accessibility import Accessibility

OUT = Path(__file__).resolve().parent / "output"


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", file=sys.stderr, flush=True)


def main():
    files = sys.argv[1:] or ["prover_out_v2_sbrp.jsonl"]
    log("loading atlas + accessibility...")
    a = load_dump()
    acc = Accessibility(a)
    report = {}
    for fn in files:
        path = BIG / fn
        if not path.exists():
            continue
        rows = [json.loads(l) for l in open(path)]
        solved = [r for r in rows if r["solved"]]
        audit_rows = []
        clean = 0
        for r in solved:
            t = a.idx.get(r["n"])
            if t is None:
                audit_rows.append({"n": r["n"], "status": "TARGET_UNKNOWN"})
                continue
            vis = acc.module_visible(t)
            own_mod = int(acc.mod_of[t])
            # statement-referenced constants are given by the problem itself:
            # anything in the statement's dependency closure is legitimate.
            stmt_ok = a.cone_from(a.type_deps(t))
            viol_same, viol_future, viol_unmapped, self_use = [], [], [], False
            for cn in r.get("used_consts", []):
                # the target and its derived auxiliaries are always forbidden
                if cn == r["n"] or cn.startswith(r["n"] + "."):
                    self_use = True
                    continue
                ci = a.idx.get(cn)
                if ci is None:
                    viol_unmapped.append(cn)
                    continue
                if ci in stmt_ok:
                    continue
                m = int(acc.mod_of[ci])
                if m < 0:
                    viol_unmapped.append(cn)
                elif m == own_mod:
                    viol_same.append(cn)
                elif not vis[m]:
                    viol_future.append(cn)
            ok = not (viol_same or viol_future or self_use)
            if ok:
                clean += 1
            audit_rows.append({
                "n": r["n"], "clean": ok,
                "self_use": self_use,
                "same_module": viol_same[:10],
                "not_imported": viol_future[:10],
                "unmapped": viol_unmapped[:10],
                "n_consts": len(r.get("used_consts", [])),
            })
        report[fn] = {
            "attempted": len(rows),
            "solved_raw": len(solved),
            "solved_clean": clean,
            "clean_rate": round(clean / len(rows), 4) if rows else None,
            "proofs": audit_rows,
        }
        log(f"{fn}: raw {len(solved)}/{len(rows)}, CLEAN {clean}/{len(rows)}")
    OUT.mkdir(exist_ok=True)
    (OUT / "proof_accessibility_audit.json").write_text(
        json.dumps(report, indent=1))
    print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk != "proofs"}
                      for k, v in report.items()}, indent=1))


if __name__ == "__main__":
    main()
