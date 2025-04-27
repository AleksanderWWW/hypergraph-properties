import json
import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from hypergraph_properties.hg_model import Hypergraph
from hypergraph_properties.utils.logger import get_logger

logger = get_logger()


class HypergraphParsingError(Exception):
    def __init__(self, msg: str) -> None:
        self.message = msg


class HypergraphReader:
    def __init__(self) -> None:
        self.hg_name: str | None = None

    def read_graph(
            self, filepath: str | os.PathLike | Path, mode: str = "r"
    ) -> Hypergraph:
        ...


class HypergraphLineReader(ABC, HypergraphReader):
    @abstractmethod
    def parse_hg_data(self, hg_data: list[str]) -> Hypergraph: ...

    def read_graph(
        self, filepath: str | os.PathLike | Path, mode: str = "r"
    ) -> Hypergraph:
        logger.info(f"reading file {filepath}")

        self.hg_name = Path(filepath).stem

        try:
            with open(filepath, mode) as fp:
                hg = self.parse_hg_data(fp.readlines())
                logger.info(f"reading {filepath} complete")
                return hg

        except Exception as e:
            logger.error(f"error while reading {filepath}: {e}")
            raise HypergraphParsingError(f"error while reading {filepath}: {e}") from e


class JSONHGReader(ABC, HypergraphReader):
    @abstractmethod
    def parse_hg_data(self, hg_data: dict[str, Any]) -> Hypergraph: ...

    def read_graph(
        self, filepath: str | os.PathLike | Path, mode: str = "r"
    ) -> Hypergraph:
        logger.info(f"reading file {filepath}")

        self.hg_name = Path(filepath).stem

        try:
            with open(filepath, mode) as fp:
                hg = self.parse_hg_data(json.load(fp))
                logger.info(f"reading {filepath} complete")
                return hg

        except Exception as e:
            logger.error(f"error while reading {filepath}: {e}")
            raise HypergraphParsingError(f"error while reading {filepath}: {e}") from e
