from dataclasses import dataclass
from typing import Generic, TypeVar, Iterable

from scipy.sparse import sparray

V = TypeVar("V")


@dataclass
class Hypergraph(Generic[V]):
    vertex_meta: Iterable[V]
    matrix: sparray
