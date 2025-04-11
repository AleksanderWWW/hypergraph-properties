import os

from abc import ABC, abstractmethod
from typing import TypeVar

from hypergraph_properties.hg_model import Hypergraph
from hypergraph_properties.utils.logger import get_logger


V = TypeVar("V")

logger = get_logger()


class HypergraphReader(ABC):
    @abstractmethod
    def parse_hg_data[V](self, hg_data: list[str]) -> Hypergraph[V]: ...

    def read_graph[V](
        self, filepath: str | os.PathLike, mode: str = "r"
    ) -> Hypergraph[V]:
        logger.info(f"reading file {filepath}")

        try:
            with open(filepath, mode) as fp:
                hg = self.parse_hg_data(fp.readlines())
                logger.info(f"reading {filepath} complete")
                return hg

        except Exception as e:
            logger.error(f"error while reading {filepath}: {e}")
            raise e
