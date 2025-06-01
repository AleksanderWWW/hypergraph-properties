from dataclasses import dataclass
from typing import Iterable

import numpy as np
from scipy.sparse import csr_array  # type: ignore[import-untyped]


@dataclass
class Hypergraph:
    name: str
    vertex_meta: Iterable[int]
    matrix: csr_array

    @property
    def degrees(self) -> np.ndarray:
        return self.matrix.sum(axis=1)

    @property
    def he_sizes(self) -> np.ndarray:
        return self.matrix.sum(axis=0)
