__all__ = [
    "pearson_node_corr",
    "spearman_node_corr",
    "pearson_edge_corr",
    "spearman_edge_corr",
    "kendalltau_node_corr",
    "kendalltau_edge_corr",
    "CorrResult",
    "purge_cache",
]


from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray
from scipy.sparse import csr_array

from hypergraph_properties.hg_model import Hypergraph
from hypergraph_properties.hg_properties.utils import (
    CorAlgorithm,
    ALGOS,
)


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


def pearson_node_corr(
    hg: Hypergraph, log_degrees: bool, log_avg_he_sizes: bool
) -> CorrResult:
    return corr(hg, log_degrees=log_degrees, log_avg_col_sizes=log_avg_he_sizes)


def spearman_node_corr(hg: Hypergraph) -> CorrResult:
    return corr(hg, False, False, algorithm=CorAlgorithm.SPEARMAN)


def kendalltau_node_corr(hg: Hypergraph) -> CorrResult:
    return corr(hg, False, False, algorithm=CorAlgorithm.KENDALLTAU)


def pearson_edge_corr(
    hg: Hypergraph, log_degrees: bool, log_avg_node_sizes: bool
) -> CorrResult:
    hg.matrix = hg.matrix.transpose().tocsr()
    return corr(
        hg,
        log_degrees=log_degrees,
        log_avg_col_sizes=log_avg_node_sizes,
        centric="edge",
    )


def spearman_edge_corr(hg: Hypergraph) -> CorrResult:
    hg.matrix = hg.matrix.transpose().tocsr()
    return corr(hg, False, False, algorithm=CorAlgorithm.SPEARMAN, centric="edge")


def kendalltau_edge_corr(hg: Hypergraph) -> CorrResult:
    hg.matrix = hg.matrix.transpose().tocsr()
    return corr(hg, False, False, algorithm=CorAlgorithm.KENDALLTAU)


_cache = {}


def purge_cache(name: str) -> None:
    global _cache
    del _cache[name]


def corr(
    hg: Hypergraph,
    log_degrees: bool = False,
    log_avg_col_sizes: bool = False,
    algorithm: CorAlgorithm = CorAlgorithm.PEARSON,
    centric: str = "node",
) -> CorrResult:
    if algorithm not in ALGOS:
        raise ValueError(f"'{algorithm}' is not a valid algorithm.")

    matrix = hg.matrix

    global _cache

    if hg.name in _cache:
        degrees = _cache[hg.name]["row_sums"]
        avg_col_sizes = _cache[hg.name]["avg_column_sizes"]
    else:
        degrees = compute_row_sums(matrix)
        avg_col_sizes = compute_avg_column_sizes(matrix)
        _cache[hg.name] = {
            "row_sums": degrees,
            "avg_column_sizes": avg_col_sizes,
        }

    if log_degrees:
        degrees = np.log(degrees)

    if log_avg_col_sizes:
        avg_col_sizes = np.log(avg_col_sizes)

    func = ALGOS[algorithm]

    result = func(degrees, avg_col_sizes)

    return CorrResult(
        result.statistic,
        result.pvalue,
        name=f"[{centric}]{algorithm.name}_{log_degrees}_{log_avg_col_sizes}",
    )


def compute_row_sums(matrix: csr_array) -> NDArray[np.int64]:
    return matrix.sum(axis=1)


def compute_avg_column_sizes(
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
