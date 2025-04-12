import numpy as np
from numba import njit
from numpy.typing import NDArray
from scipy import stats
from scipy.sparse import csr_array

from hypergraph_properties.hg_model import Hypergraph


def node_corr(
    hg: Hypergraph,
    log_degrees: bool = False,
    log_avg_he_sizes: bool = False,
) -> np.float64:
    vertex_indices = np.array([v - 1 for v in hg.vertex_meta], dtype=np.int32)
    matrix = hg.matrix

    degrees = row_sums(matrix.indptr, matrix.data, matrix.shape[0])[vertex_indices]
    if log_degrees:
        degrees = np.log(degrees) + 1

    avg_he_sizes = compute_avg_he_sizes(
        vertex_indices, matrix.indptr, matrix.indices, matrix.data, *matrix.shape
    )

    if log_avg_he_sizes:
        avg_he_sizes = np.log(avg_he_sizes) + 1

    return stats.pearsonr(degrees, avg_he_sizes)


@njit
def row_sums(indptr, data, n_rows) -> NDArray[np.int64]:
    result = np.zeros(n_rows, dtype=np.float64)
    for i in range(n_rows):
        result[i] = np.sum(data[indptr[i] : indptr[i + 1]])
    return result


@njit
def compute_avg_he_sizes(vertex_indices, indptr, indices, data, n_rows, n_cols):
    avg_sizes = np.zeros(len(vertex_indices), dtype=np.float64)

    col_degrees = np.zeros(n_cols, dtype=np.float64)
    for row in range(n_rows):
        for j in range(indptr[row], indptr[row + 1]):
            col = indices[j]
            col_degrees[col] += data[j]

    for idx, v in enumerate(vertex_indices):
        start = indptr[v]
        end = indptr[v + 1]
        if start == end:
            avg_sizes[idx] = 0.0
            continue

        connected_cols = indices[start:end]
        total = 0.0
        for col in connected_cols:
            total += col_degrees[col]

        avg_sizes[idx] = total / (end - start)

    return avg_sizes


def vertex_degree(matrix: csr_array, vertex: int) -> np.int64:
    return matrix[vertex].sum()


def avg_he_size(matrix: csr_array, vertex: int) -> np.float64:
    return matrix[:, matrix[vertex]].sum() / vertex_degree(matrix, vertex)
