from typing import Protocol
from dataclasses import dataclass

from scipy.stats._result_classes import PearsonRResult  # type: ignore[import-untyped]
from scipy.stats._stats_py import SignificanceResult as SpearmanRResult  # type: ignore[import-untyped]


@dataclass
class PearsonNodeCorrResultSet:
    no_log: PearsonRResult
    log_degree: PearsonRResult
    log_he_size: PearsonRResult
    both_log: PearsonRResult


@dataclass
class HypergraphStats:
    pearson_corr: PearsonNodeCorrResultSet
    spearman_corr: SpearmanRResult
    num_nodes: int
    num_he: int



class HypergraphStatsRepository(Protocol):
    def read(self, hg_name: str) -> HypergraphStats:
        ...

    def save(self, hg_name: str, hg_stats: HypergraphStats) -> None:
        ...
