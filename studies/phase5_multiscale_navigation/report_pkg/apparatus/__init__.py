"""mathmap_eval -- the evaluation apparatus for citation rankings and
inclusion policies.

Three things are kept strictly apart:

    corpus       the exact record (nothing filtered, nothing judged)
    rankings     how incidences are ORDERED            (ours to get right)
    inclusion    how much of that order a view ADMITS  (the user's knob)

Quick start:

    from mathmap_eval import run, RunConfig, compare_table
    out = run(RunConfig(universe="U1"))
    print(compare_table(out))

Add a ranking without touching the suite:

    from mathmap_eval import ranking
    @ranking("R_mine", features=2)
    def _mine(c, base):
        "Doc becomes the published description."
        return (c.inc_in_stmt_world[base].astype("int8"),
                -c.inc_d_cite[base].astype(float))

Add an inclusion policy the same way:

    from mathmap_eval import inclusion
    @inclusion("my_policy", "per-proof", monotone_param="k")
    def _mine(c, base, ranks, k=1):
        return ranks < k
"""
from .corpus import Corpus, get_corpus
from .rankings import ranking, REGISTRY as RANKINGS, names as ranking_names
from .inclusions import inclusion, REGISTRY as INCLUSIONS, names as inclusion_names, check_nested
from .runner import RunConfig, run, compare_table, depth_table, graph_table
from . import metrics

__all__ = ["Corpus", "get_corpus", "ranking", "inclusion", "RANKINGS",
           "INCLUSIONS", "ranking_names", "inclusion_names", "check_nested",
           "RunConfig", "run", "compare_table", "depth_table", "graph_table",
           "metrics"]
