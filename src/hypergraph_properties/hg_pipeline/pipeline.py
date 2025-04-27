__all__ = ["run_pipeline"]

import itertools
import os
from pathlib import Path

from tqdm import tqdm

from hypergraph_properties.hg_properties.corr import pearson_node_corr, spearman_node_corr, purge_cache
from hypergraph_properties.hg_reader import HypergraphReader
from hypergraph_properties.hg_pipeline.result_set import HGPipelineResult, PearsonNodeCorrResult


def run_pipeline(
        reader: HypergraphReader, filename: str | Path | os.PathLike,
) -> HGPipelineResult:
    hg = reader.read_graph(str(filename))

    cors_p = []

    combinations = list(itertools.product([False, True], repeat=2))

    with tqdm(total=5, desc="calculating correlations") as pbar:
        for (log_avg_he_sizes, log_degrees) in combinations:
            corr_p = pearson_node_corr(hg, log_avg_he_sizes, log_degrees)
            pbar.update(1)
            cors_p.append(corr_p)

        s_cor = spearman_node_corr(hg)
        pbar.update(1)

    purge_cache(hg.name)

    p_cor = PearsonNodeCorrResult(*cors_p)

    return HGPipelineResult(
        pearson_node_corr=p_cor,
        spearman_node_corr=s_cor,
        hg=hg,
    )
