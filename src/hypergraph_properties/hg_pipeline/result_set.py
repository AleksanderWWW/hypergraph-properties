__all__ = [
    "HGPipelineResult",
    "PearsonNodeCorrResult",
    "PearsonEdgeCorrResult",
]

from dataclasses import dataclass

from hypergraph_properties.hg_model import Hypergraph
from hypergraph_properties.hg_properties.corr import CorrResult


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
    pearson_node_corr: PearsonNodeCorrResult
    pearson_edge_corr: PearsonEdgeCorrResult
    spearman_node_corr: CorrResult
    spearman_edge_corr: CorrResult
    assortativity: CorrResult
    hg: Hypergraph

    def to_dict(self) -> dict[str, float | str]:
        return {
            "name": self.hg.name,
            **self.pearson_node_corr.to_dict(),
            **self.spearman_node_corr.to_dict(),
            **self.pearson_edge_corr.to_dict(),
            **self.spearman_edge_corr.to_dict(),
            **self.assortativity.to_dict(),
            "n_vertices": self.hg.matrix.shape[0],
            "n_edges": self.hg.matrix.shape[1],
        }
