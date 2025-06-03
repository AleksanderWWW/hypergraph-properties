from dataclasses import dataclass
from typing import Iterable

import numpy as np
from scipy.sparse import csr_array  # type: ignore[import-untyped]

from hypergraph_properties.hg_properties.utils import with_empty_rows_removed


@dataclass
class Hypergraph:
    name: str
    vertex_meta: Iterable[int]
    matrix: csr_array
    _degrees: np.ndarray | None = None
    _he_sizes: np.ndarray | None = None

    def __post_init__(self) -> None:
        self.matrix = with_empty_rows_removed(self.matrix)

    @property
    def degrees(self) -> np.ndarray:
        if self._degrees is None:
            self._degrees = self.matrix.sum(axis=1)
        return self._degrees

    @property
    def he_sizes(self) -> np.ndarray:
        if self._he_sizes is None:
            self._he_sizes = self.matrix.sum(axis=0)
        return self._he_sizes
