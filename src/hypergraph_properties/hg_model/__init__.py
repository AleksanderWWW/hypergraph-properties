from dataclasses import dataclass
from typing import Iterable

from scipy.sparse import csr_array


@dataclass
class Hypergraph:
    vertex_meta: Iterable[int]
    matrix: csr_array
