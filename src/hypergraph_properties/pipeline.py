import os
from pathlib import Path

from tqdm import tqdm

from hypergraph_properties.hg_properties.corr_slow import node_corr
from hypergraph_properties.hg_reader import HypergraphReader
from hypergraph_properties.reporting.result_set import HGPipelineResult, PearsonNodeCorrResultSet


def run_pipeline(
        reader: HypergraphReader, filename: str | Path | os.PathLike,
) -> HGPipelineResult:
    hg = reader.read_graph(str(filename))

    breakpoint()

    cors_p = []
    cors_s = []

    with tqdm(total=8, desc="calculating correlations") as pbar:
        for log_avg_he_sizes in [False, True]:
            for log_degrees in [False, True]:
                corr_p = node_corr(
                    hg, log_degrees=log_degrees, log_avg_he_sizes=log_avg_he_sizes
                )
                pbar.update(1)
                # corr_s = node_corr(
                #     hg,
                #     log_degrees=log_degrees,
                #     log_avg_he_sizes=log_avg_he_sizes,
                #     algorithm=CorAlgorithm.SPEARMAN,
                # )
                pbar.update(1)

                cors_p.append(corr_p)
                # cors_s.append(corr_s)

    p_cor = PearsonNodeCorrResultSet(*cors_p)
    # s_cor = SpearmanNodeCor(*cors_s)

    return HGPipelineResult(
        p_cor=p_cor,
        s_cor=None,
        hg=hg,
    )
