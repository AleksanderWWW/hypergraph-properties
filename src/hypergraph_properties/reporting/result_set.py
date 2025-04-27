__all__ = [
    "HGPipelineResult",
    "PearsonNodeCorrResultSet"
]

from dataclasses import dataclass

from scipy.stats._stats_py import SignificanceResult as SpearmanRResult  # type: ignore[import-untyped]

from hypergraph_properties.hg_model import Hypergraph


@dataclass
class PearsonResult:
    statistic: float
    p_value: float

    def to_dict(self) -> dict[str, float]:
        return {
            "statistic": self.statistic,
            "p_value": self.p_value,
        }


@dataclass
class PearsonNodeCorrResultSet:
    no_log: PearsonResult
    log_degree: PearsonResult
    log_he_size: PearsonResult
    both_log: PearsonResult

    def to_dict(self) -> dict[str, dict[str, float]]:
        return {
            "pearson_no_log": self.no_log.to_dict(),
            "pearson_log_degree": self.log_degree.to_dict(),
            "pearson_log_he_size": self.log_he_size.to_dict(),
            "pearson_both_log": self.both_log.to_dict(),
        }


@dataclass(frozen=True)
class HGPipelineResult:
    p_cor: PearsonNodeCorrResultSet
    s_cor: SpearmanRResult
    hg: Hypergraph

    def to_dict(self) -> dict[str, float | str]:
        return {
            "name": self.hg.name,
            **self.p_cor.to_dict(),
            **self.s_cor.to_dict(),
            "n_vertices": self.hg.matrix.shape[0],
            "n_edges": self.hg.matrix.shape[1],
        }
