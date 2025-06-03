__all__ = ["run_pipeline"]

import itertools
import os
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Generator

from tqdm import tqdm

from hypergraph_properties.hg_pipeline.result_set import (
    HGPipelineResult,
    PearsonEdgeCorrResult,
    PearsonNodeCorrResult,
    HGDescriptiveStats,
)
from hypergraph_properties.hg_properties.corr import (
    pearson_edge_corr,
    pearson_node_corr,
    purge_cache,
    spearman_edge_corr,
    spearman_node_corr,
    kendalltau_node_corr,
    kendalltau_edge_corr,
)
from hypergraph_properties.hg_properties.assortativity_corr import corr_assort
from hypergraph_properties.hg_properties.descriptive_stats import (
    get_avg_degree,
    get_avg_he_size,
    get_degree_sd,
    get_he_size_sd,
    get_min_degree,
    get_max_degree,
    get_min_he_size,
    get_max_he_size,
    get_n_incidence_edges, get_degree_skew, get_he_skew,
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

    with tqdm(total=14, desc="calculating correlations") as pbar:
        # Node-centric correlations
        with with_cache_purged(hg.name):
            for log_avg_he_sizes, log_degrees in combinations:
                corr_p = pearson_node_corr(hg, log_avg_he_sizes, log_degrees)
                pbar.update(1)
                cors_node_p.append(corr_p)

            s_cor_node = spearman_node_corr(hg)
            pbar.update(1)

            k_cor_node = kendalltau_node_corr(hg)
            pbar.update(1)

        # Edge-centric correlations
        with with_cache_purged(hg.name):
            for log_avg_edge_sizes, log_degrees in combinations:
                corr_p = pearson_edge_corr(hg, log_avg_edge_sizes, log_degrees)
                pbar.update(1)
                cors_edge_p.append(corr_p)

            s_cor_edge = spearman_edge_corr(hg)
            pbar.update(1)

            k_cor_edge = kendalltau_edge_corr(hg)
            pbar.update(1)

        a_cor = corr_assort(hg)
        pbar.update(3)

    p_node_cor = PearsonNodeCorrResult(*cors_node_p)
    p_edge_cor = PearsonEdgeCorrResult(*cors_edge_p)

    desc_stats = HGDescriptiveStats(
        avg_degree=get_avg_degree(hg),
        avg_he_size=get_avg_he_size(hg),
        degree_sd=get_degree_sd(hg),
        he_size_sd=get_he_size_sd(hg),
        min_degree=get_min_degree(hg),
        max_degree=get_max_degree(hg),
        min_he_size=get_min_he_size(hg),
        max_he_size=get_max_he_size(hg),
        n_incidence_edges=get_n_incidence_edges(hg),
        degree_skew=get_degree_skew(hg),
        he_size_skew=get_he_skew(hg),
    )

    return HGPipelineResult(
        desc_stats=desc_stats,
        pearson_node_corr=p_node_cor,
        pearson_edge_corr=p_edge_cor,
        spearman_node_corr=s_cor_node,
        spearman_edge_corr=s_cor_edge,
        kendalltau_node_corr=k_cor_node,
        kendalltau_edge_corr=k_cor_edge,
        pearson_assortativity=a_cor[0],
        spearman_assortativity=a_cor[1],
        kendalltau_assortativity=a_cor[2],
        hg=hg,
    )
