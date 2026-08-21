"""Corpus: the exact citation record, loaded once and shared.

Nothing here filters, ranks, or judges. It exposes the complete incidence
record plus derived per-node and per-incidence signals that rankings and
inclusion policies may use. Candidate UNIVERSES are named masks over the
record -- they are declared, never silently applied.
"""
from __future__ import annotations

import glob
import json
import os
from dataclasses import dataclass, field
from functools import cached_property

import numpy as np

DEFAULT_DATA = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data"))
DEFAULT_PROV = ("/private/tmp/claude-501/-Users-sam-my-repos-research-Map-Of-"
                "Mathematics/b1ceda4c-2b8d-4f52-b481-6fdafa0f5cb5/scratchpad/prov")

# declaration kind codes as written by build_incidence.py
KIND_NAMES = ["theorem", "def", "inductive", "constructor", "recursor",
              "opaque", "quot", "axiom", "?"]
DEFINITION_KINDS = (1, 2, 5, 6, 7)      # def / inductive / opaque / quot / axiom
LOAD_ROLES = (0, 1, 2, 7)               # applied / let-value / explicit / unresolved
ROLE_NAMES = ["applied", "let-value", "explicit-arg", "implicit-arg",
              "instance-slot", "strict-implicit", "type-annotation", "unresolved"]


@dataclass
class Corpus:
    """The complete record. Arrays are parallel; `inc_*` are per incidence."""
    data_dir: str = DEFAULT_DATA
    prov_dir: str = DEFAULT_PROV
    _loaded: bool = field(default=False, repr=False)

    # ---------------------------------------------------------------- load
    def load(self) -> "Corpus":
        if self._loaded:
            return self
        d = self.data_dir
        inc = np.load(os.path.join(d, "incid.npz"))
        arts = np.load(os.path.join(d, "artifacts.npz"))
        nodes = np.load(os.path.join(d, "nodes.npz"))
        v8 = np.load(os.path.join(d, "v8_mask.npz"))

        self.inc_artifact = inc["artifact"].astype(np.int64)
        self.inc_decl = inc["decl"].astype(np.int64)
        self.inc_roles = inc["roles"]
        self.inc_load_bearing = inc["load_bearing"]
        self.inc_in_stmt_world = inc["in_stmt_world"]
        self.inc_d_target = inc["d_target"].astype(np.int32)
        self.inc_d_cite = inc["d_cite"].astype(np.int32)
        self.inc_delta_depth = inc["delta_depth"].astype(np.int32)

        self.art_certifies = arts["certifies"].astype(np.int64)
        self.node_kind = nodes["kind"]
        self.node_depth = nodes["depth"].astype(np.int32)
        self.node_gen = nodes["gen"]
        self.node_in_degree = nodes["in_degree"]
        self.node_stated = nodes["stated"]

        # kernel-local TYPE facts (exposed as documented properties below)
        self._node_pr = nodes["pr"]
        self._node_ps = nodes["ps"]
        self._node_ar = nodes["ar"].astype(np.int32)

        # frozen V8 categories, used as SIGNALS only (never as deletions)
        self.decl_is_claim = v8["decl_is_claim"]
        self.decl_logic_only = v8["decl_logic_only"]
        self.inc_machinery = v8["machinery"]

        self.names = json.load(open(os.path.join(d, "names.json")))
        self.name_to_id = {nm: i for i, nm in enumerate(self.names)}
        self._loaded = True
        return self

    # ------------------------------------------------------------ derived
    @property
    def n_nodes(self) -> int:
        return len(self.node_depth)

    @property
    def n_incidences(self) -> int:
        return len(self.inc_artifact)

    # ------------------------------------------------- kernel-local signals
    # The three below are properties of a declaration's OWN TYPE, decided by
    # the kernel when that declaration is elaborated. They read nothing about
    # the rest of the library -- no usage counts, no thresholds, no
    # neighbourhoods -- so they are APPEND-SAFE: adding theorems to Mathlib
    # can never change the value already recorded for an existing
    # declaration. This is the property `decl_logic_only` (v8_mask.npz) does
    # NOT have; that one is derived from library-wide usage frequencies.

    @property
    def node_is_proof(self) -> np.ndarray:
        """Per declaration: its type IS a Prop, i.e. the constant is a proof.

        Kernel fact (`Meta.isProp` on the declaration's type), decided from
        the type alone. Append-safe: independent of the rest of the library.
        """
        self.load()
        return self._node_pr

    @property
    def node_is_prop(self) -> np.ndarray:
        """Per declaration: its type telescopes to Sort 0, i.e. the constant
        is a proposition or a predicate (`True`, `Even`, `Membership.mem`)
        rather than data (`Nat`, `Finset`).

        Kernel fact (telescope the type, whnf the body, ask if the sort is
        Prop). Append-safe: independent of the rest of the library.
        """
        self.load()
        return self._node_ps

    @property
    def node_arity(self) -> np.ndarray:
        """Per declaration: number of binders its type telescopes through.

        Kernel fact, read off the declaration's own type. Append-safe:
        independent of the rest of the library. With `node_is_prop` it
        separates BARE propositions (is_prop and arity 0 -- `True`, `False`,
        named conjectures) from PREDICATES (is_prop and arity > 0).
        """
        self.load()
        return self._node_ar

    @cached_property
    def inc_target(self) -> np.ndarray:
        """Declaration certified by the artifact this incidence belongs to."""
        return self.art_certifies[self.inc_artifact]

    @cached_property
    def art_of_decl(self) -> dict:
        return {d: a for a, d in enumerate(self.art_certifies)}

    @cached_property
    def inc_is_definition(self) -> np.ndarray:
        return np.isin(self.node_kind[self.inc_decl], DEFINITION_KINDS)

    @cached_property
    def inc_is_theorem(self) -> np.ndarray:
        return self.node_kind[self.inc_decl] == 0

    @cached_property
    def inc_glue(self) -> np.ndarray:
        """Descriptive role statistic, NOT a semantic judgement (audit item 5)."""
        return self.decl_logic_only[self.inc_decl] | self.inc_machinery

    @cached_property
    def inc_strongest_role(self) -> np.ndarray:
        return np.argmax(self.inc_roles, axis=1)

    @cached_property
    def decl_popularity(self) -> np.ndarray:
        """How many incidences cite each declaration, over the whole record."""
        return np.bincount(self.inc_decl, minlength=self.n_nodes).astype(np.float64)

    @cached_property
    def decl_idf(self) -> np.ndarray:
        n_art = float(len(np.unique(self.inc_artifact)))
        return np.maximum(np.log(n_art / np.maximum(self.decl_popularity, 1.0)), 0.0)

    def kind_group(self, decl_ids: np.ndarray) -> np.ndarray:
        """theorem / definition / constructor-recursor, as a string array."""
        k = self.node_kind[decl_ids]
        out = np.full(len(k), "constructor/recursor", dtype=object)
        out[k == 0] = "theorem"
        out[np.isin(k, DEFINITION_KINDS)] = "definition/construction"
        return out

    # ----------------------------------------------------------- universes
    def universe(self, name: str) -> np.ndarray:
        """Named candidate universes (audit item 3: declare, never assume).

        U0  every exact occurrence, any role
        U1  load-bearing roles only (the historical filter)
        U1D U1 for theorems, but ALL roles for definitions -- the audit's
            observation that definitions are used in type/implicit/instance
            positions, restored WITH roles preserved
        """
        self.load()
        no_self = self.inc_target != self.inc_decl
        if name == "U0":
            return no_self
        if name == "U1":
            return self.inc_load_bearing & no_self
        if name == "U1D":
            return (self.inc_load_bearing | self.inc_is_definition) & no_self
        raise KeyError(f"unknown universe {name!r} (have U0, U1, U1D)")

    # -------------------------------------------------------- ground truth
    @cached_property
    def source_refs(self) -> dict:
        """Elaborator-resolved identifiers the human wrote, per declaration.

        This never passes through our extraction and uses no naming rules.
        """
        out = {}
        for f in glob.glob(os.path.join(self.prov_dir, "*.json")):
            for e in json.load(open(f))["decls"]:
                if e.get("refs"):
                    out[e["name"]] = set(e["refs"])
        return out

    def evaluation_set(self, universe: str = "U1", proof_written_only: bool = True):
        """Proofs with ground truth, as (artifact, incidence positions, gt ids,
        target depth).

        `proof_written_only` subtracts identifiers already implied by the
        declaration's own statement, approximating what the human typed as
        part of the argument. The answer key is NEVER filtered by any
        ranking's own predicate (the circular-harness defect).
        """
        self.load()
        base = np.where(self.universe(universe))[0]
        by_art = {}
        for p in base:
            by_art.setdefault(self.inc_artifact[p], []).append(p)
        out = []
        for nm, refs in self.source_refs.items():
            di = self.name_to_id.get(nm)
            if di is None:
                continue
            ai = self.art_of_decl.get(di)
            if ai is None:
                continue
            pl = by_art.get(ai)
            if not pl:
                continue
            if proof_written_only:
                stmt = {self.names[self.inc_decl[p]] for p in pl
                        if self.inc_in_stmt_world[p]}
            else:
                stmt = set()
            gt = {self.name_to_id[c] for c in refs
                  if c != nm and c not in stmt and c in self.name_to_id}
            if not gt:
                continue
            out.append((ai, np.array(pl), gt, int(self.node_depth[di])))
        return out


_CORPUS: Corpus | None = None


def get_corpus(**kw) -> Corpus:
    """Process-wide singleton so repeated runs do not reload 130MB."""
    global _CORPUS
    if _CORPUS is None:
        _CORPUS = Corpus(**kw).load()
    return _CORPUS
