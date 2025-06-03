import functools
from typing import Callable, Any

import numpy as np
from scipy.stats import skew

from hypergraph_properties.hg_model import Hypergraph


def get_avg_degree(hg: Hypergraph) -> float:
    return float(np.mean(hg.degrees))


def get_avg_he_size(hg: Hypergraph) -> float:
    return float(np.mean(hg.he_sizes))


def get_degree_sd(hg: Hypergraph) -> float:
    return float(np.std(hg.degrees))


def get_he_size_sd(hg: Hypergraph) -> float:
    return float(np.std(hg.he_sizes))


def get_min_degree(hg: Hypergraph) -> float:
    return float(np.min(hg.degrees))


def get_max_degree(hg: Hypergraph) -> float:
    return float(np.max(hg.degrees))


def get_min_he_size(hg: Hypergraph) -> float:
    return float(np.min(hg.he_sizes))


def get_max_he_size(hg: Hypergraph) -> float:
    return float(np.max(hg.he_sizes))


def get_n_incidence_edges(hg: Hypergraph) -> int:
    matrix = hg.matrix

    rows, _ = matrix.nonzero()

    return len(rows)


def get_degree_skew(hg: Hypergraph) -> float:
    return float(skew(hg.degrees))


def get_he_skew(hg: Hypergraph) -> float:
    return float(skew(hg.he_sizes))
