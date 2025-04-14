__all__ = [
    "PearsonNodeCor",
    "SpearmanNodeCor",
]

from dataclasses import dataclass

from scipy.stats._result_classes import PearsonRResult  # type: ignore[import-untyped]
from scipy.stats._stats_py import SignificanceResult as SpearmanRResult  # type: ignore[import-untyped]


@dataclass(frozen=True)
class PearsonNodeCor:
    no_log: PearsonRResult
    log_degree: PearsonRResult
    log_he_size: PearsonRResult
    both_log: PearsonRResult


@dataclass(frozen=True)
class SpearmanNodeCor:
    no_log: SpearmanRResult
    log_degree: SpearmanRResult
    log_he_size: SpearmanRResult
    both_log: SpearmanRResult
