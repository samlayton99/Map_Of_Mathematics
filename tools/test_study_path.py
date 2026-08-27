"""Tests for the study-path engine: synthetic fixture + real-corpus invariants.

Run: ~/venv/general_ml/bin/python -m pytest tools/test_study_path.py -q
"""
import pytest

from study_path import Corpus, load_corpus, cones, build_path, corpus_index

#            T
#   type: T -> S1 ; body: T -> M1, M2
#   S1 -> B ; M1 -> L ; M2 -> B ; L -> B     (all body-layer)
# depths: B=0, L=1, S1=1, M2=1, M1=2, T=3
NAMES = ["B", "L", "S1", "M1", "M2", "T"]


def toy():
    n = len(NAMES)
    type_out = [dict() for _ in range(n)]
    body_out = [dict() for _ in range(n)]
    type_out[5] = {2: 1}                       # statement of T uses S1
    body_out[5] = {3: 2, 4: 1}                 # proof of T uses M1, M2
    body_out[2] = {0: 1}
    body_out[3] = {1: 1}
    body_out[4] = {0: 1}
    body_out[1] = {0: 1}
    return Corpus(NAMES, ["theorem"] * n, [1] * n,
                  [(), (), (), ("internal-detail",), (), ()],
                  [["F"]] * n, type_out, body_out)


def test_depths_longest_chain():
    c = toy()
    assert [c.depth[c.idx[x]] for x in NAMES] == [0, 1, 1, 2, 1, 3]


def test_cones_exact():
    c = toy()
    a_s, a_p, new = cones(c, c.idx["T"])
    assert {c.names[i] for i in a_s} == {"S1", "B"}
    assert {c.names[i] for i in a_p} == {"M1", "M2", "L", "B"}
    assert {c.names[i] for i in new} == {"M1", "M2", "L"}


def test_moves_ranked_new_then_depth_and_machinery_marked():
    c = toy()
    r = build_path(c, "T")
    moves = [m["name"] for m in r["proof_moves"]]
    assert moves[0] == "M1"                    # deepest new fact first
    assert set(moves) == {"M1", "M2", "L"}
    by = {m["name"]: m for m in r["proof_moves"]}
    assert by["M1"]["machinery"] == ["internal-detail"]
    assert by["M2"]["machinery"] == []


def test_statement_path_ordered_and_reversible_filter():
    c = toy()
    r = build_path(c, "T")
    depths = [layer["depth"] for layer in r["statement_path"]]
    assert depths == sorted(depths)
    names = [i["name"] for layer in r["statement_path"] for i in layer["items"]]
    assert names == ["B", "S1"]
    # drop_machinery must not change the statement path here (no machinery in A_S)
    r2 = build_path(c, "T", drop_machinery=True)
    names2 = [i["name"] for layer in r2["statement_path"] for i in layer["items"]]
    assert names2 == names


def test_unknown_target_raises():
    with pytest.raises(KeyError):
        build_path(toy(), "Nope")


# ------------------------------------------------------------ real corpus

@pytest.fixture(scope="module")
def real():
    return load_corpus()


def test_real_corpus_shape(real):
    assert real.n == 3662
    assert sum(len(u) for u in real.unfold) > 0


def test_real_invariants_on_stored_theorems(real):
    checked = 0
    for t in range(real.n):
        if real.kind[t] != "theorem" or not real.stored[t] or not real.body_out[t]:
            continue
        a_s, a_p, new = cones(real, t)
        assert new == a_p - a_s
        assert t not in a_s and t not in a_p          # DAG: no self-ancestry
        checked += 1
        if checked >= 50:
            break
    assert checked == 50


def test_real_known_example_runs_and_is_deterministic(real):
    r1 = build_path(real, "Real.log_mul")
    r2 = build_path(real, "Real.log_mul")
    assert r1 == r2
    assert r1["proof_cone_size"] > 0
    all_names = {i["name"] for l in r1["statement_path"] for i in l["items"]}
    a_s, _, _ = cones(real, real.idx["Real.log_mul"])
    assert all_names <= {real.names[i] for i in a_s}


def test_index_covers_stored_theorems(real):
    rows = corpus_index(real)
    assert len(rows) > 500
    by = {r["name"]: r for r in rows}
    assert "Real.log_mul" in by
    r = by["Real.log_mul"]
    assert r["proof_cone"] >= r["new"]
    assert len(r["top_moves"]) <= 5
