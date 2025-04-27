import numpy as np
from scipy import stats
from scipy.sparse import csr_array

from hypergraph_properties.hg_model import Hypergraph


def node_corr(
    hg: Hypergraph,
    log_degrees: bool = False,
    log_avg_he_sizes: bool = False,
) -> np.float64:
    degrees = [vertex_degree(hg.matrix, vertex - 1) for vertex in hg.vertex_meta]
    if log_degrees:
        degrees = [np.log(degree) + 1 for degree in degrees]

    avg_he_sizes = [avg_he_size(hg.matrix, vertex - 1) for vertex in hg.vertex_meta]
    if log_avg_he_sizes:
        avg_he_sizes = [np.log(size) + 1 for size in avg_he_sizes]

    return stats.pearsonr(degrees, avg_he_sizes)


def vertex_degree(matrix: csr_array, vertex: int) -> np.int64:
    return matrix[vertex].sum()


def avg_he_size(matrix: csr_array, vertex: int) -> np.float64:
    return matrix[:, matrix[vertex]].sum() / vertex_degree(matrix, vertex)
