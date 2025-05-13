import numpy as np
import pytest
from scipy.sparse import csr_array

from hypergraph_properties.hg_properties.corr import compute_row_sums, compute_avg_column_sizes, \
    with_empty_rows_removed


@pytest.fixture(scope="session")
def matrix() -> csr_array:
    return csr_array(np.array(
        [
            [1, 1, 0, 1],  # (2 + 3 + 4) / 3
            [1, 0, 1, 0],  # (2 + 1) / 2
            [0, 0, 0, 1],  # 4 / 1
            [0, 1, 0, 1],  # (3 + 4) / 2
            [0, 1, 0, 1],  # (3 + 4) / 2
         ]
    ))


def test_compute_vertex_degrees(matrix) -> None:
    vertex_degrees = compute_row_sums(matrix)
    assert np.all(vertex_degrees == np.array([3, 2, 1, 2, 2]))


def test_compute_avg_he_sizes(matrix) -> None:
    avg_he_sizes = compute_avg_column_sizes(matrix)
    assert np.all(avg_he_sizes == np.array([
        (2 + 3 + 4) / 3,
        (2 + 1) / 2,
        4 / 1,
        (3 + 4) / 2,
        (3 + 4) / 2,
    ]))


def test_removing_singleton_vertices(matrix) -> None:
    # insert a singleton vertex and assert that it's there
    matrix_with_singleton = csr_array(np.vstack([matrix.toarray(), [0, 0, 0, 0]]))

    assert 0 in matrix_with_singleton.sum(axis=1)

    matrix_no_singleton = with_empty_rows_removed(matrix_with_singleton)

    # no singleton vertices in the result matrix
    assert not np.any(matrix_no_singleton.sum(axis=1) == 0)

    assert matrix_no_singleton.shape[0] == matrix_with_singleton.shape[0] - 1
