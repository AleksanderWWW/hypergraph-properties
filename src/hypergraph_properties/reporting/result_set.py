__all__ = [
    "PearsonNodeCor",
]

from dataclasses import dataclass

from scipy.stats._result_classes import PearsonRResult


@dataclass(frozen=True)
class PearsonNodeCor:
    no_log: PearsonRResult
    log_degree: PearsonRResult
    log_he_size: PearsonRResult
    both_log: PearsonRResult
