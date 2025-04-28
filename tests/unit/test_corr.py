import numpy as np
import pytest
from scipy.sparse import csr_array

from hypergraph_properties.hg_properties.corr import compute_vertex_degrees, compute_avg_he_sizes


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
    vertex_degrees = compute_vertex_degrees(matrix)
    assert np.all(vertex_degrees == np.array([3, 2, 1, 2, 2]))


def test_compute_avg_he_sizes(matrix) -> None:
    avg_he_sizes = compute_avg_he_sizes(matrix)
    assert np.all(avg_he_sizes == np.array([
        (2 + 3 + 4) / 3,
        (2 + 1) / 2,
        4 / 1,
        (3 + 4) / 2,
        (3 + 4) / 2,
    ]))
