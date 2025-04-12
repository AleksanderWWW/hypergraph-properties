import os
from abc import ABC, abstractmethod

from hypergraph_properties.hg_model import Hypergraph
from hypergraph_properties.utils.logger import get_logger

logger = get_logger()


class HypergraphParsingError(Exception):
    def __init__(self, msg: str) -> None:
        self.message = msg


class HypergraphReader(ABC):
    @abstractmethod
    def parse_hg_data(self, hg_data: list[str]) -> Hypergraph: ...

    def read_graph(self, filepath: str | os.PathLike, mode: str = "r") -> Hypergraph:
        logger.info(f"reading file {filepath}")

        try:
            with open(filepath, mode) as fp:
                hg = self.parse_hg_data(fp.readlines())
                logger.info(f"reading {filepath} complete")
                return hg

        except Exception as e:
            logger.error(f"error while reading {filepath}: {e}")
            raise HypergraphParsingError(f"error while reading {filepath}: {e}") from e
