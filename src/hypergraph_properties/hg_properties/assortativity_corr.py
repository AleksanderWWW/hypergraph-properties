import numpy as np
from scipy.stats import stats

from hypergraph_properties.hg_model import Hypergraph
from hypergraph_properties.hg_properties.corr import CorrResult
from hypergraph_properties.hg_properties.utils import with_empty_rows_removed


def corr_assort(hg: Hypergraph) -> CorrResult:
    matrix = with_empty_rows_removed(matrix=hg.matrix)

    row_sums = np.array(matrix.sum(axis=1)).ravel()
    col_sums = np.array(matrix.sum(axis=0)).ravel()

    rows, cols = matrix.nonzero()

    degrees = row_sums[rows]
    he_sizes = col_sums[cols]

    corr = stats.pearsonr(degrees, he_sizes)

    return CorrResult(
        statistic=corr.statistic,
        pvalue=corr.pvalue,
        name="assortativity_pearsonr",
    )
