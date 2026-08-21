"""Global-map edge admission for MathMap (Phase 6, Task 1).

Builds three admitted edge sets over declarations from the artifact/decl
incidence table:

  E4       top-4 per artifact under the laneD_stmt ordering
  EL0      ALL candidates with dem=0, lane=0, stmt=0 (variable-k, constant-free)
  E4_flat  control: top-4 under the flat ordering (role tier, position)

Ordering (laneD_stmt), five ordinal keys, no fitted constants:

  1. dem       0 = load-bearing universe; 1 = U1D demoted entry
               (non-Prop declarations cited only via non-load roles)
  2. lane      0 move < 1 transport (depth_stmt <= 1) < 2 infra (instance-only)
  3. stmt      0 proof-introduced first, 1 statement vocabulary
  4. -depth    deepest cited value-depth first
  5. position  first occurrence in the artifact's incidence block

Generated candidates are redirected to their owning non-generated declaration
(longest proper dot-prefix); a generated candidate owned by the artifact's own
certified declaration is INTERNAL and dropped.

All data paths derive from DATA_DIR so the final run can point at the rebuilt
arrays.  Override with $MAPGRAPH_DATA_DIR or argv[1].
"""

import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# ---- single source of truth for input arrays -------------------------------
DATA_DIR = os.environ.get(
    "MAPGRAPH_DATA_DIR", os.path.join(ROOT, "data", "v7_backup")
)
OUT_DIR = os.environ.get("MAPGRAPH_OUT_DIR", os.path.join(ROOT, "data", "map"))

# role column -> role tier
#   0 applied, 1 let-value, 2 explicit-arg, 3 implicit, 4 instance,
#   5 strict-implicit, 6 type-annotation, 7 unresolved
ROLE_TIER = np.array([0, 0, 1, 4, 5, 3, 6, 2], dtype=np.int16)
TIER_NONE = 127  # no recorded role at all

# key packing widths (validated against the arrays at runtime)
POS_BITS = 12       # max incidences per artifact
DEPTH_BITS = 10     # max declaration depth
DEPTH_MAX = (1 << DEPTH_BITS) - 1


def log(msg):
    print("[%7.1fs] %s" % (time.time() - _T0, msg), flush=True)


_T0 = time.time()


# ---------------------------------------------------------------------------
def load_arrays(data_dir=None):
    d = data_dir or DATA_DIR
    log("loading arrays from %s" % d)
    inc = np.load(os.path.join(d, "incid.npz"))
    art = np.load(os.path.join(d, "artifacts.npz"))
    nod = np.load(os.path.join(d, "nodes.npz"))
    dsc = np.load(os.path.join(d, "depth_scc.npz"))
    with open(os.path.join(d, "names.json")) as fh:
        names = json.load(fh)
    A = dict(
        artifact=inc["artifact"],
        decl=inc["decl"],
        roles=inc["roles"],
        load_bearing=inc["load_bearing"],
        in_stmt_world=inc["in_stmt_world"],
        d_cite=inc["d_cite"],
        delta_depth=inc["delta_depth"],
        certifies=art["certifies"].astype(np.int64),
        is_generated=art["is_generated"],
        n_incidences=art["n_incidences"],
        kind=nod["kind"],
        pr=nod["pr"],
        gen=nod["gen"],
        depth=nod["depth"],
        depth_stmt=dsc["depth_stmt"],
        names=names,
    )
    log("  %d incidences, %d artifacts, %d declarations"
        % (len(A["artifact"]), len(A["certifies"]), len(names)))
    return A


# ---------------------------------------------------------------------------
def build_owner_map(A):
    """owner[d] = id of the longest proper dot-prefix of name[d] that is an
    existing NON-generated declaration, else -1.  Only meaningful for gen decls.
    """
    names = A["names"]
    gen = A["gen"]
    n = len(names)
    log("building generated-owner map over %d generated declarations"
        % int(gen.sum()))
    nongen_index = {}
    for i, nm in enumerate(names):
        if not gen[i]:
            nongen_index[nm] = i
    owner = np.full(n, -1, dtype=np.int64)
    n_owned = 0
    for i in range(n):
        if not gen[i]:
            continue
        nm = names[i]
        cut = nm.rfind(".")
        while cut > 0:
            j = nongen_index.get(nm[:cut])
            if j is not None:
                owner[i] = j
                n_owned += 1
                break
            cut = nm.rfind(".", 0, cut)
    log("  %d generated declarations have a non-generated owner (%.1f%%)"
        % (n_owned, 100.0 * n_owned / max(1, int(gen.sum()))))
    return owner


# ---------------------------------------------------------------------------
def role_tier(roles):
    """min over occurring roles of ROLE_TIER; TIER_NONE when no role recorded."""
    tier = np.full(roles.shape[0], TIER_NONE, dtype=np.int16)
    for r in range(roles.shape[1]):
        present = roles[:, r] > 0
        np.minimum(tier, np.where(present, ROLE_TIER[r], TIER_NONE), out=tier)
    return tier


def block_positions(n_incidences, n_rows):
    """position of each incidence within its artifact's row block."""
    starts = np.zeros(len(n_incidences), dtype=np.int64)
    np.cumsum(n_incidences[:-1], out=starts[1:])
    return np.arange(n_rows, dtype=np.int64) - np.repeat(starts, n_incidences)


# ---------------------------------------------------------------------------
def build_candidates(A, owner):
    """Per-row laneD_stmt candidate table, restricted to non-generated artifacts.

    Returns a dict of parallel arrays over surviving rows.
    """
    artifact = A["artifact"]
    decl = A["decl"].astype(np.int64)
    n_rows = len(artifact)

    log("computing incidence positions")
    pos = block_positions(A["n_incidences"], n_rows)
    assert pos.max() < (1 << POS_BITS), "POS_BITS too small"

    log("computing role tiers")
    tier = role_tier(A["roles"])
    log("  rows with no recorded role: %d" % int((tier == TIER_NONE).sum()))

    # --- restrict to human-written (non-generated) artifacts ----------------
    keep = ~A["is_generated"][artifact]
    log("rows on non-generated artifacts: %d / %d (%.1f%%)"
        % (keep.sum(), n_rows, 100.0 * keep.sum() / n_rows))

    # --- universe / demotion (U1D) ------------------------------------------
    lb = A["load_bearing"]
    is_prop = A["pr"][decl]
    dem = np.where(lb, 0, 1).astype(np.int8)
    # non-load-bearing rows only enter if the cited declaration is non-Prop
    keep &= lb | (~is_prop)
    log("rows after universe (load-bearing + U1D non-Prop): %d" % keep.sum())

    # --- generated redirect --------------------------------------------------
    g = A["gen"][decl]
    own = owner[decl]
    target = A["certifies"][artifact]
    # generated candidate with no owner, or owned by the artifact's own target,
    # is internal -> drop
    drop_gen = g & ((own < 0) | (own == target))
    keep &= ~drop_gen
    log("rows after dropping internal/ownerless generated candidates: %d"
        % keep.sum())

    idx = np.flatnonzero(keep)
    del keep

    artifact = artifact[idx]
    decl = decl[idx]
    g = g[idx]
    own = own[idx]
    dem = dem[idx]
    tier = tier[idx]
    pos = pos[idx]
    stmt = A["in_stmt_world"][idx].astype(np.int8)
    d_cite = A["d_cite"][idx].astype(np.int64)
    target = target[idx]

    # candidate id: owner for generated, else the cited declaration
    cand = np.where(g, own, decl)

    # depth key source: owner's node depth for redirected candidates
    depth = np.where(g, A["depth"][np.where(g, own, 0)], d_cite)
    depth = np.clip(depth, 0, DEPTH_MAX)

    # lane: 2 instance-only, 1 transport (depth_stmt <= 1), 0 move.
    # redirected candidates take the owner's depth_stmt and never lane 2.
    ds_src = np.where(g, own, decl)
    ds = A["depth_stmt"][ds_src]
    lane = np.where(ds <= 1, 1, 0).astype(np.int8)
    lane = np.where((~g) & (tier == 5), 2, lane).astype(np.int8)

    # drop self-loops (candidate == the declaration the artifact certifies)
    self_loop = cand == target
    if self_loop.any():
        log("dropping %d self-loop candidates" % int(self_loop.sum()))
        m = ~self_loop
        artifact, cand, dem, lane, stmt, depth, pos, target, tier = (
            artifact[m], cand[m], dem[m], lane[m], stmt[m], depth[m],
            pos[m], target[m], tier[m])

    log("candidate rows: %d" % len(cand))
    return dict(artifact=artifact, cand=cand, dem=dem, lane=lane, stmt=stmt,
                depth=depth, pos=pos, target=target, tier=tier)


# ---------------------------------------------------------------------------
def order_and_dedup(C, n_artifacts):
    """Sort by (artifact, dem, lane, stmt, -depth, pos); dedup candidates per
    artifact keeping the best key; return per-artifact rank."""
    art_bits = int(np.ceil(np.log2(max(2, n_artifacts))))
    shift_pos = 0
    shift_depth = shift_pos + POS_BITS
    shift_stmt = shift_depth + DEPTH_BITS
    shift_lane = shift_stmt + 1
    shift_dem = shift_lane + 2
    shift_art = shift_dem + 1
    assert shift_art + art_bits < 63, "key overflow"
    log("packing sort key (artifact bits=%d, total=%d)"
        % (art_bits, shift_art + art_bits))

    key = (C["artifact"].astype(np.int64) << shift_art)
    key |= C["dem"].astype(np.int64) << shift_dem
    key |= C["lane"].astype(np.int64) << shift_lane
    key |= C["stmt"].astype(np.int64) << shift_stmt
    key |= (DEPTH_MAX - C["depth"]) << shift_depth   # deepest first
    key |= C["pos"]

    log("sorting %d candidate rows" % len(key))
    order = np.argsort(key, kind="stable")
    del key

    # dedup (artifact, cand) keeping first in sorted order
    log("deduplicating after redirect")
    comb = (C["artifact"][order].astype(np.int64) << 32) | C["cand"][order]
    _, first = np.unique(comb, return_index=True)
    keep = np.sort(first)
    del comb, first
    order = order[keep]
    log("  %d unique (artifact, candidate) pairs" % len(order))

    # rank within artifact
    arts = C["artifact"][order]
    newblk = np.empty(len(arts), dtype=bool)
    newblk[0] = True
    np.not_equal(arts[1:], arts[:-1], out=newblk[1:])
    starts = np.flatnonzero(newblk)
    sizes = np.diff(np.append(starts, len(arts)))
    rank = np.arange(len(arts), dtype=np.int64) - np.repeat(starts, sizes)
    return order, rank


# ---------------------------------------------------------------------------
def flat_edges(A):
    """Control: top-4 per non-generated artifact under (role tier, position)
    over load-bearing candidates only; no lanes, no redirect."""
    log("building E4_flat control")
    artifact = A["artifact"]
    decl = A["decl"].astype(np.int64)
    pos = block_positions(A["n_incidences"], len(artifact))
    tier = role_tier(A["roles"])
    keep = (~A["is_generated"][artifact]) & A["load_bearing"]
    idx = np.flatnonzero(keep)
    art = artifact[idx]
    target = A["certifies"][art]
    cand = decl[idx]
    m = cand != target
    idx, art, target, cand = idx[m], art[m], target[m], cand[m]
    t = np.clip(tier[idx].astype(np.int64), 0, 127)
    p = pos[idx]
    art_bits = int(np.ceil(np.log2(max(2, len(A["certifies"])))))
    key = (art.astype(np.int64) << (POS_BITS + 7)) | (t << POS_BITS) | p
    assert (POS_BITS + 7 + art_bits) < 63
    order = np.argsort(key, kind="stable")
    arts = art[order]
    newblk = np.empty(len(arts), dtype=bool)
    newblk[0] = True
    np.not_equal(arts[1:], arts[:-1], out=newblk[1:])
    starts = np.flatnonzero(newblk)
    sizes = np.diff(np.append(starts, len(arts)))
    rank = np.arange(len(arts), dtype=np.int64) - np.repeat(starts, sizes)
    sel = order[rank < 4]
    return target[sel].astype(np.int32), cand[sel].astype(np.int32)


# ---------------------------------------------------------------------------
def save_edges(name, src, dst, stats):
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, "edges_%s.npz" % name)
    np.savez_compressed(path, src_decl=src.astype(np.int32),
                        dst_decl=dst.astype(np.int32))
    stats[name] = dict(
        n_edges=int(len(src)),
        n_unique_edges=int(len(np.unique(
            (src.astype(np.int64) << 32) | dst.astype(np.int64)))),
        n_src=int(len(np.unique(src))),
        n_dst=int(len(np.unique(dst))),
        n_nodes=int(len(np.unique(np.concatenate([src, dst])))),
    )
    log("saved %s: %d edges (%d unique), %d nodes -> %s"
        % (name, len(src), stats[name]["n_unique_edges"],
           stats[name]["n_nodes"], path))


def main():
    global DATA_DIR
    if len(sys.argv) > 1:
        DATA_DIR = sys.argv[1]
    A = load_arrays(DATA_DIR)
    owner = build_owner_map(A)
    os.makedirs(OUT_DIR, exist_ok=True)
    np.save(os.path.join(OUT_DIR, "owner.npy"), owner)
    C = build_candidates(A, owner)
    order, rank = order_and_dedup(C, len(A["certifies"]))

    stats = {"data_dir": DATA_DIR}

    # --- E4 ------------------------------------------------------------------
    sel = order[rank < 4]
    save_edges("E4", C["target"][sel], C["cand"][sel], stats)

    # --- EL0 -----------------------------------------------------------------
    o = order
    mask = (C["dem"][o] == 0) & (C["lane"][o] == 0) & (C["stmt"][o] == 0)
    selL = o[mask]
    save_edges("EL0", C["target"][selL], C["cand"][selL], stats)

    # k distribution of EL0 over non-generated artifacts
    n_art = len(A["certifies"])
    k = np.bincount(C["artifact"][selL], minlength=n_art)
    nongen_art = np.flatnonzero(~A["is_generated"])
    kk = k[nongen_art]
    stats["EL0_k"] = dict(
        n_artifacts=int(len(kk)),
        mean=float(kk.mean()),
        median=float(np.median(kk)),
        p90=float(np.percentile(kk, 90)),
        p99=float(np.percentile(kk, 99)),
        max=int(kk.max()),
        frac_zero=float((kk == 0).mean()),
        mean_nonzero=float(kk[kk > 0].mean()) if (kk > 0).any() else 0.0,
    )
    log("EL0 k: mean %.2f median %.0f p90 %.0f p99 %.0f max %d zero-frac %.3f"
        % (stats["EL0_k"]["mean"], stats["EL0_k"]["median"],
           stats["EL0_k"]["p90"], stats["EL0_k"]["p99"],
           stats["EL0_k"]["max"], stats["EL0_k"]["frac_zero"]))

    # k distribution of E4 (how many artifacts even reach 4)
    k4 = np.bincount(C["artifact"][sel], minlength=n_art)[nongen_art]
    stats["E4_k"] = dict(mean=float(k4.mean()), frac_zero=float((k4 == 0).mean()),
                         frac_full4=float((k4 == 4).mean()))

    # lane / dem / stmt composition of the whole candidate pool
    stats["pool"] = dict(
        n_candidates=int(len(C["cand"])),
        dem1_frac=float((C["dem"] == 1).mean()),
        lane_frac=[float((C["lane"] == i).mean()) for i in range(3)],
        stmt1_frac=float((C["stmt"] == 1).mean()),
    )

    # --- E4_flat -------------------------------------------------------------
    fs, fd = flat_edges(A)
    save_edges("E4_flat", fs, fd, stats)

    with open(os.path.join(OUT_DIR, "edge_stats.json"), "w") as fh:
        json.dump(stats, fh, indent=2)
    log("wrote %s" % os.path.join(OUT_DIR, "edge_stats.json"))
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
