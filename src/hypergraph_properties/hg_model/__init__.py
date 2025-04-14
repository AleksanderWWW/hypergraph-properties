from dataclasses import dataclass
from typing import Iterable

from scipy.sparse import csr_array  # type: ignore[import-untyped]


@dataclass
class Hypergraph:
    name: str
    vertex_meta: Iterable[int]
    matrix: csr_array
