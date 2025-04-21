__all__ = [
    "PearsonNodeCor",
    "SpearmanNodeCor",
    "HGPipelineResult",
]

from dataclasses import dataclass

from scipy.stats._result_classes import PearsonRResult  # type: ignore[import-untyped]
from scipy.stats._stats_py import SignificanceResult as SpearmanRResult  # type: ignore[import-untyped]

from hypergraph_properties.hg_model import Hypergraph


class NodeCorMixIn:
    def to_dict(self) -> dict[str, float]:
        return  {
            "no_log_stat": self.no_log.statistic,
            "no_log_pvalue": self.no_log.pvalue,
            "log_degree_stat": self.log_degree.statistic,
            "log_degree_pvalue": self.log_degree.pvalue,
            "log_he_size_stat": self.log_he_size.statistic,
            "log_he_size_pvalue": self.log_he_size.pvalue,
            "both_log_stat": self.both_log.statistic,
            "both_log_pvalue": self.both_log.pvalue,
        }


@dataclass(frozen=True)
class PearsonNodeCor(NodeCorMixIn):
    no_log: PearsonRResult
    log_degree: PearsonRResult
    log_he_size: PearsonRResult
    both_log: PearsonRResult


@dataclass(frozen=True)
class SpearmanNodeCor(NodeCorMixIn):
    no_log: SpearmanRResult
    log_degree: SpearmanRResult
    log_he_size: SpearmanRResult
    both_log: SpearmanRResult


@dataclass(frozen=True)
class HGPipelineResult:
    p_cor: PearsonNodeCor
    s_cor: SpearmanNodeCor
    hg: Hypergraph

    def to_dict(self) -> dict[str, float]:
        return {
            **self.p_cor.to_dict(),
            **self.s_cor.to_dict(),
            "n_vertices": self.hg.matrix.shape[0],
            "n_edges": self.hg.matrix.shape[1],
        }
