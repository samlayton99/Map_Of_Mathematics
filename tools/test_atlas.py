"""Tests for the full-Mathlib atlas engine.

The ground truth is tools/study_path.py (exact python-int bitmask engine,
already validated against CONES_REPORT).  The atlas engine must agree
bit-for-bit on the six-file corpus, and must handle cycles (which the
corpus does not have but full Mathlib does) via SCC condensation.

Run: ~/venv/general_ml/bin/python -m pytest tools/test_atlas.py -q
"""
import numpy as np
import pytest

import study_path
from atlas import Atlas, batch_cones, build_path, _col, theorem_roots


def atlas_from_lists(names, kind, cls, t_lists, v_lists):
    from atlas import _csr_from_lists
    t_indptr, t_indices = _csr_from_lists(t_lists)
    v_indptr, v_indices = _csr_from_lists(v_lists)
    return Atlas(names, kind, cls, t_indptr, t_indices, v_indptr, v_indices)


def atlas_from_corpus(c):
    t_lists = [sorted(c.type_out[i].keys()) for i in range(c.n)]
    v_lists = [sorted(c.body_out[i].keys()) for i in range(c.n)]
    return atlas_from_lists(c.names, list(c.kind), list(c.p3), t_lists, v_lists)


def scc_set(atlas, mask, j):
    """Node-id set for root j from a packed mask matrix."""
    out = set()
    for s in np.where(_col(mask, j))[0]:
        for m in atlas.scc_members[atlas.scc_indptr[s]:atlas.scc_indptr[s + 1]]:
            out.add(int(m))
    return out


# --------------------------------------------------------------------- toy

NAMES = ["B", "L", "S1", "M1", "M2", "T"]


def toy_atlas():
    t_lists = [(), (), (), (), (), (2,)]
    v_lists = [(), (0,), (0,), (1,), (0,), (3, 4)]
    return atlas_from_lists(NAMES, ["theorem"] * 6,
                           [(), (), (), ("internal-detail",), (), ()],
                           t_lists, v_lists)


def test_toy_depths_match_study_path():
    a = toy_atlas()
    assert [int(a.depth[i]) for i in range(6)] == [0, 1, 1, 2, 1, 3]


def test_toy_cones_exact():
    a = toy_atlas()
    maskS, maskP = batch_cones(a, [a.idx["T"]])
    a_s = scc_set(a, maskS, 0)
    a_p = scc_set(a, maskP, 0)
    assert {a.names[i] for i in a_s} == {"S1", "B"}
    assert {a.names[i] for i in a_p} == {"M1", "M2", "L", "B"}


def test_toy_build_path_matches_study_path_shape():
    a = toy_atlas()
    r = build_path(a, "T")
    assert r["statement_cone_size"] == 2
    assert r["proof_cone_size"] == 4
    assert r["new_count"] == 3
    assert [m["name"] for m in r["proof_moves"]][0] == "M1"


# ------------------------------------------------------------------- cycles

def test_cycle_condensation():
    # A <-> C mutual recursion; T's proof uses A; A also uses B.
    # closure(T.body) must contain A, C, B.
    names = ["B", "A", "C", "T"]
    t_lists = [(), (), (), ()]
    v_lists = [(), (2, 0), (1,), (1,)]
    a = atlas_from_lists(names, ["theorem"] * 4, [()] * 4, t_lists, v_lists)
    assert a.ncomp == 3            # {A,C} collapsed
    maskS, maskP = batch_cones(a, [a.idx["T"]])
    assert {a.names[i] for i in scc_set(a, maskP, 0)} == {"A", "C", "B"}
    r = build_path(a, "T")
    assert r["proof_cone_size"] == 3


def test_self_loop_dropped():
    names = ["B", "P", "T"]     # P is a partial def referring to itself
    t_lists = [(), (), ()]
    v_lists = [(), (1, 0), (1,)]
    a = atlas_from_lists(names, ["def"] * 3, [()] * 3, t_lists, v_lists)
    maskS, maskP = batch_cones(a, [a.idx["T"]])
    assert {a.names[i] for i in scc_set(a, maskP, 0)} == {"P", "B"}


# -------------------------------------------------------------- real corpus

@pytest.fixture(scope="module")
def corpus():
    return study_path.load_corpus()


@pytest.fixture(scope="module")
def catlas(corpus):
    return atlas_from_corpus(corpus)


def test_corpus_is_dag_and_depths_agree(corpus, catlas):
    assert catlas.ncomp == corpus.n
    assert [int(catlas.depth[i]) for i in range(corpus.n)] == corpus.depth


def test_corpus_batch_cones_agree_with_exact_engine(corpus, catlas):
    roots = [t for t in range(corpus.n)
             if corpus.kind[t] == "theorem" and corpus.stored[t]
             and corpus.body_out[t]][:130]
    maskS, maskP = batch_cones(catlas, roots)
    for j, t in enumerate(roots):
        a_s, a_p, new = study_path.cones(corpus, t)
        assert scc_set(catlas, maskS, j) == a_s
        assert scc_set(catlas, maskP, j) == a_p
        assert scc_set(catlas, maskP & ~maskS, j) == new


def test_corpus_multiword_batch(corpus, catlas):
    """Roots spanning several 64-bit words land in the right columns."""
    roots = [t for t in range(corpus.n)
             if corpus.kind[t] == "theorem" and corpus.body_out[t]][:200]
    maskS, maskP = batch_cones(catlas, roots)
    for j in (0, 63, 64, 129, 199):
        t = roots[j]
        a_s, a_p, _ = study_path.cones(corpus, t)
        assert scc_set(catlas, maskS, j) == a_s
        assert scc_set(catlas, maskP, j) == a_p


def test_corpus_build_path_agrees(corpus, catlas):
    r1 = study_path.build_path(corpus, "Real.log_mul")
    r2 = build_path(catlas, "Real.log_mul")
    assert r2["statement_cone_size"] == r1["statement_cone_size"]
    assert r2["proof_cone_size"] == r1["proof_cone_size"]
    assert r2["new_count"] == r1["new_count"]
    assert {m["name"] for m in r2["proof_moves"]} >= \
           {m["name"] for m in r1["proof_moves"][:10]}


def test_load_dump_streaming_parser_and_cache(tmp_path):
    """Deps referenced before their own rows get ids early; CSR rows must be
    permuted back to node-id order, and the npz cache must round-trip."""
    import json
    from atlas import load_dump
    rows = [
        {"n": "T", "k": "theorem", "c": [], "t": ["S1"], "v": ["M1", "M2"]},
        {"n": "S1", "k": "theorem", "c": [], "t": [], "v": ["B"]},
        {"n": "M1", "k": "theorem", "c": ["internal-detail"], "t": [], "v": ["L"]},
        {"n": "M2", "k": "theorem", "c": [], "t": [], "v": ["B"]},
        {"n": "L", "k": "def", "c": [], "t": [], "v": ["B"]},
        {"n": "B", "k": "def", "c": [], "t": [], "v": []},
    ]
    dump = tmp_path / "dump.jsonl"
    dump.write_text("\n".join(json.dumps(r) for r in rows) + "\n")
    a = load_dump(dump, tmp_path / "c.npz", tmp_path / "n.txt")
    r1 = build_path(a, "T")
    assert (r1["statement_cone_size"], r1["proof_cone_size"],
            r1["new_count"]) == (2, 4, 3)
    a2 = load_dump(dump, tmp_path / "c.npz", tmp_path / "n.txt")  # from cache
    assert a2.names == a.names and build_path(a2, "T") == r1
    assert a2.cls[a2.idx["M1"]] == ("internal-detail",)


def test_run_index_counters_and_rows(tmp_path, corpus, catlas):
    from atlas import run_index
    roots = theorem_roots(catlas)[:64]
    out = tmp_path / "idx.jsonl"
    inS, inP, asNew = run_index(catlas, roots, out, batch=32, topk=5,
                                log=lambda m: None)
    import json
    rows = [json.loads(l) for l in out.read_text().splitlines()]
    assert len(rows) == len(roots)
    r0 = rows[0]
    t0 = catlas.idx[r0["name"]]
    a_s, a_p, new = study_path.cones(corpus, t0)
    assert r0["statement_cone"] == len(a_s)
    assert r0["proof_cone"] == len(a_p)
    assert r0["new"] == len(new)
    # counters: node in as many proof cones as index rows claim
    total_inP = sum(r["proof_cone"] for r in rows)
    assert int(inP.sum()) == total_inP
    total_new = sum(r["new"] for r in rows)
    assert int(asNew.sum()) == total_new
