import functools
from typing import Callable, Any

import numpy as np

from hypergraph_properties.hg_model import Hypergraph
from hypergraph_properties.hg_properties.utils import with_empty_rows_removed


def preprocessed(f: Callable[[Hypergraph], Any]) -> Callable:
    @functools.wraps(f)
    def wrapper(hg: Hypergraph) -> Any:
        hg.matrix = with_empty_rows_removed(hg.matrix)
        return f(hg)

    return wrapper


@preprocessed
def get_avg_degree(hg: Hypergraph) -> float:
    return float(np.mean(hg.degrees))


@preprocessed
def get_avg_he_size(hg: Hypergraph) -> float:
    return float(np.mean(hg.he_sizes))


@preprocessed
def get_degree_sd(hg: Hypergraph) -> float:
    return float(np.std(hg.degrees))


@preprocessed
def get_he_size_sd(hg: Hypergraph) -> float:
    return float(np.std(hg.he_sizes))


@preprocessed
def get_min_degree(hg: Hypergraph) -> float:
    return float(np.min(hg.degrees))


@preprocessed
def get_max_degree(hg: Hypergraph) -> float:
    return float(np.max(hg.degrees))


@preprocessed
def get_min_he_size(hg: Hypergraph) -> float:
    return float(np.min(hg.he_sizes))


@preprocessed
def get_max_he_size(hg: Hypergraph) -> float:
    return float(np.max(hg.he_sizes))


@preprocessed
def get_n_incidence_edges(hg: Hypergraph) -> int:
    matrix = hg.matrix

    rows, _ = matrix.nonzero()

    return len(rows)
