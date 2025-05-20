__all__ = ["with_empty_rows_removed", "CorAlgorithm"]

from enum import Enum, auto

import numpy as np
from scipy.sparse import csr_array


def with_empty_rows_removed(matrix: csr_array) -> csr_array:
    num_nonzeros = np.diff(matrix.indptr)
    return matrix[num_nonzeros != 0]


class CorAlgorithm(Enum):
    PEARSON = auto()
    SPEARMAN = auto()
