import numpy as np
import pytest
from scipy.sparse import csr_array

from hypergraph_properties.hg_properties.corr import compute_vertex_degrees, compute_avg_he_sizes


@pytest.fixture(scope="session")
def matrix() -> csr_array:
    return csr_array(np.array(
        [
            [1, 1, 0, 0, 1],
            [1, 0, 1, 0, 0],
            [0, 0, 0, 0, 1],
         ]
    ))


def test_compute_vertex_degrees(matrix) -> None:
    vertex_degrees = compute_vertex_degrees(matrix)
    assert np.all(vertex_degrees == np.array([3, 2, 1]))


def test_compute_avg_he_sizes(matrix) -> None:
    avg_he_sizes = compute_avg_he_sizes(matrix)
    assert np.all(avg_he_sizes == np.array([5 / 3, 3 / 2, 2]))
