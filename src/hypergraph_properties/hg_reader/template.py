import os

from abc import ABC, abstractmethod
from typing import TypeVar

from hypergraph_properties.hg_model import Hypergraph


V = TypeVar("V")


class HypergraphReader(ABC):
    @abstractmethod
    def parse_hg_data[V](self, hg_data: list[str]) -> Hypergraph[V]:
        ...

    def read_graph[V](self, filepath: str | os.PathLike, mode: str = "r") -> Hypergraph[V]:
        with open(filepath, mode) as fp:
            return self.parse_hg_data(fp.readlines())
