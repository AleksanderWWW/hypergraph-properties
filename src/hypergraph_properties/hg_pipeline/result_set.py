__all__ = [
    "HGDescriptiveStats",
    "HGPipelineResult",
    "PearsonNodeCorrResult",
    "PearsonEdgeCorrResult",
]

from dataclasses import dataclass

from hypergraph_properties.hg_model import Hypergraph
from hypergraph_properties.hg_properties.corr import CorrResult


@dataclass(frozen=True)
class HGDescriptiveStats:
    avg_degree: float
    avg_he_size: float
    degree_sd: float
    he_size_sd: float
    min_degree: float
    max_degree: float
    min_he_size: float
    max_he_size: float
    n_incidence_edges: int

    def to_dict(self) -> dict:
        return {
            "avg_degree": self.avg_degree,
            "avg_he_size": self.avg_he_size,
            "degree_sd": self.degree_sd,
            "he_size_sd": self.he_size_sd,
            "min_degree": self.min_degree,
            "max_degree": self.max_degree,
            "min_he_size": self.min_he_size,
            "max_he_size": self.max_he_size,
            "n_incidence_edges": self.n_incidence_edges,
        }


@dataclass(frozen=True)
class PearsonNodeCorrResult:
    pearson_no_log: CorrResult
    pearson_log_v_degree: CorrResult
    pearson_log_avg_he_size: CorrResult
    pearson_both_log: CorrResult

    def to_dict(self) -> dict:
        return {
            **self.pearson_no_log.to_dict(),
            **self.pearson_log_v_degree.to_dict(),
            **self.pearson_log_avg_he_size.to_dict(),
            **self.pearson_both_log.to_dict(),
        }


@dataclass(frozen=True)
class PearsonEdgeCorrResult:
    pearson_no_log: CorrResult
    pearson_log_he_degree: CorrResult
    pearson_log_avg_node_size: CorrResult
    pearson_both_log: CorrResult

    def to_dict(self) -> dict:
        return {
            **self.pearson_no_log.to_dict(),
            **self.pearson_log_he_degree.to_dict(),
            **self.pearson_log_avg_node_size.to_dict(),
            **self.pearson_both_log.to_dict(),
        }


@dataclass(frozen=True)
class HGPipelineResult:
    desc_stats: HGDescriptiveStats
    pearson_node_corr: PearsonNodeCorrResult
    pearson_edge_corr: PearsonEdgeCorrResult
    spearman_node_corr: CorrResult
    spearman_edge_corr: CorrResult
    kendalltau_node_corr: CorrResult
    kendalltau_edge_corr: CorrResult
    pearson_assortativity: CorrResult
    spearman_assortativity: CorrResult
    kendalltau_assortativity: CorrResult
    hg: Hypergraph

    def to_dict(self) -> dict[str, float | str]:
        return {
            "name": self.hg.name,
            **self.desc_stats.to_dict(),
            **self.pearson_node_corr.to_dict(),
            **self.spearman_node_corr.to_dict(),
            **self.pearson_edge_corr.to_dict(),
            **self.spearman_edge_corr.to_dict(),
            **self.kendalltau_node_corr.to_dict(),
            **self.kendalltau_edge_corr.to_dict(),
            **self.pearson_assortativity.to_dict(),
            **self.spearman_assortativity.to_dict(),
            **self.kendalltau_assortativity.to_dict(),
            "n_vertices": self.hg.matrix.shape[0],
            "n_edges": self.hg.matrix.shape[1],
        }
