__all__ = ["pearson_node_corr", "spearman_node_corr", "CorrResult", "purge_cache"]


from dataclasses import dataclass
from enum import Enum, auto

import numpy as np
from numpy.typing import NDArray
from scipy import stats  # type: ignore[import-untyped]
from scipy.sparse import csr_array

from hypergraph_properties.hg_model import Hypergraph


class CorAlgorithm(Enum):
    PEARSON = auto()
    SPEARMAN = auto()


@dataclass
class CorrResult:
    statistic: float
    pvalue: float
    name: str

    def to_dict(self) -> dict:
        return {
            f"{self.name}_statistic": self.statistic,
            f"{self.name}_pvalue": self.pvalue,
        }


def pearson_node_corr(hg, log_degrees, log_avg_he_sizes) -> CorrResult:
    return node_corr(hg, log_degrees, log_avg_he_sizes)


def spearman_node_corr(hg) -> CorrResult:
    return node_corr(hg, False, False, algorithm=CorAlgorithm.SPEARMAN)


_cache = {}


def purge_cache(name: str) -> None:
    global _cache
    del _cache[name]


def node_corr(
    hg: Hypergraph,
    log_degrees: bool = False,
    log_avg_he_sizes: bool = False,
    algorithm: CorAlgorithm = CorAlgorithm.PEARSON,
) -> CorrResult:
    matrix = hg.matrix
    global _cache

    if hg.name in _cache:
        degrees = _cache[hg.name]["degrees"]
        avg_he_sizes = _cache[hg.name]["avg_he_sizes"]
    else:
        degrees = compute_vertex_degrees(matrix)
        avg_he_sizes = compute_avg_he_sizes(matrix)
        _cache[hg.name] = {
            "degrees": degrees,
            "avg_he_sizes": avg_he_sizes,
        }

    if log_degrees:
        degrees = np.log(degrees + 1)

    if log_avg_he_sizes:
        avg_he_sizes = np.log(avg_he_sizes + 1)

    func = stats.pearsonr if algorithm == CorAlgorithm.PEARSON else stats.spearmanr

    corr = func(degrees, avg_he_sizes)

    return CorrResult(
        corr.statistic,
        corr.pvalue,
        name=f"{algorithm.name}_{log_degrees}_{log_avg_he_sizes}",
    )


def compute_vertex_degrees(matrix: csr_array) -> NDArray[np.int64]:
    return matrix.sum(axis=1)


def compute_avg_he_sizes(
    matrix: csr_array,
) -> NDArray[np.int64]:
    he_sizes = np.asarray(matrix.sum(axis=0))

    n_vertices = matrix.shape[0]
    avg_deg = np.zeros(n_vertices, dtype=np.float64)

    for i in range(n_vertices):
        start, end = matrix.indptr[i], matrix.indptr[i + 1]
        hyper_edges = matrix.indices[start:end]

        avg_deg[i] = 0.0 if len(hyper_edges) == 0 else he_sizes[hyper_edges].mean()

    return avg_deg
