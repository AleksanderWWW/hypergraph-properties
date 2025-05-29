__all__ = ["with_empty_rows_removed", "CorAlgorithm", "ALGOS"]

from enum import Enum, auto

import numpy as np
from scipy.sparse import csr_array
from scipy import stats  # type: ignore[import-untyped]


def with_empty_rows_removed(matrix: csr_array) -> csr_array:
    num_nonzeros = np.diff(matrix.indptr)
    return matrix[num_nonzeros != 0]


class CorAlgorithm(Enum):
    PEARSON = auto()
    SPEARMAN = auto()
    KENDALLTAU = auto()


ALGOS = {
    CorAlgorithm.PEARSON: stats.pearsonr,
    CorAlgorithm.SPEARMAN: stats.spearmanr,
    CorAlgorithm.KENDALLTAU: stats.kendalltau,
}
