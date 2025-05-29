from pathlib import Path

import numpy as np
from scipy.stats import stats

from hypergraph_properties.hg_model import Hypergraph
from hypergraph_properties.hg_properties.corr import CorrResult
from hypergraph_properties.hg_properties.utils import with_empty_rows_removed, ALGOS


def corr_assort(hg: Hypergraph) -> list[CorrResult]:
    matrix = with_empty_rows_removed(matrix=hg.matrix)

    row_sums = np.array(matrix.sum(axis=1)).ravel()
    col_sums = np.array(matrix.sum(axis=0)).ravel()

    rows, cols = matrix.nonzero()

    degrees = row_sums[rows]
    he_sizes = col_sums[cols]

    ### TEMP CODE
    # import pandas as pd
    #
    # pd.DataFrame(data={
    #     "degrees": degrees,
    #     "he_sizes": he_sizes,
    # }).to_csv(
    #     Path(__file__).parent.parent.parent.parent / "temp" / f"assortativity_{hg.name}.csv", header=True, index=False,
    # )

    results = []
    for algo in ALGOS.values():
        corr = stats.pearsonr(degrees, he_sizes)
        results.append(
            CorrResult(
                statistic=corr.statistic,
                pvalue=corr.pvalue,
                name=f"assortativity_{algo.__name__}",
            )
        )

    return results
