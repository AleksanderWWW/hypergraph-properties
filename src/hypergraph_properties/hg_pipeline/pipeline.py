__all__ = ["run_pipeline"]

import itertools
import os
from pathlib import Path
from contextlib import contextmanager
from typing import Any, Generator

from tqdm import tqdm

from hypergraph_properties.hg_pipeline.result_set import (
    HGPipelineResult,
    PearsonNodeCorrResult, PearsonEdgeCorrResult,
)
from hypergraph_properties.hg_properties.corr import (
    pearson_node_corr,
    purge_cache,
    spearman_node_corr,
    pearson_edge_corr,
    spearman_edge_corr,
)
from hypergraph_properties.hg_reader import HypergraphReader


@contextmanager
def with_cache_purged(hg_name: str) -> Generator[None, Any, None]:
    yield

    purge_cache(hg_name)


def run_pipeline(
    reader: HypergraphReader,
    filename: str | Path | os.PathLike,
) -> HGPipelineResult:
    hg = reader.read_graph(str(filename))

    cors_node_p = []
    cors_edge_p = []

    combinations = list(itertools.product([False, True], repeat=2))

    with tqdm(total=10, desc="calculating correlations") as pbar:

        # Node-centric correlations
        with with_cache_purged(hg.name):
            for log_avg_he_sizes, log_degrees in combinations:
                corr_p = pearson_node_corr(hg, log_avg_he_sizes, log_degrees)
                pbar.update(1)
                cors_node_p.append(corr_p)

            s_cor = spearman_node_corr(hg)
            pbar.update(1)

        # Edge-centric correlations
        with with_cache_purged(hg.name):
            for log_avg_edge_sizes, log_degrees in combinations:
                corr_p = pearson_edge_corr(hg, log_avg_edge_sizes, log_degrees)
                pbar.update(1)
                cors_edge_p.append(corr_p)

            s_cor = spearman_node_corr(hg)
            pbar.update(1)


    p_node_cor = PearsonNodeCorrResult(*cors_node_p)
    p_edge_cor = PearsonEdgeCorrResult(*cors_edge_p)


    return HGPipelineResult(
        pearson_node_corr=p_node_cor,
        pearson_edge_corr=p_edge_cor,
        spearman_node_corr=s_cor,
        spearman_edge_corr=s_cor,
        hg=hg,
    )
