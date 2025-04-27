from typing import Any

import numpy as np
from scipy.sparse import csr_array, dok_array, lil_array, coo_array  # type: ignore[import-untyped]

from hypergraph_properties.hg_model import Hypergraph
from hypergraph_properties.hg_reader.template import HypergraphLineReader, JSONHGReader
from hypergraph_properties.utils.logger import get_logger

logger = get_logger()


class SyntheticHGReader(HypergraphLineReader):
    def parse_hg_data(self, hg_data: list[str]) -> Hypergraph:
        v_max = 1
        num_hedges = 0

        for line in hg_data:
            num_hedges += 1
            for vertex in line.split("," if "," in line else " "):
                if int(vertex) > v_max:
                    v_max = int(vertex)

        matrix = lil_array((v_max, num_hedges), dtype=bool)

        for idx_he, line in enumerate(hg_data):
            for vertex in line.split("," if "," in line else " "):
                matrix[int(vertex) - 1, idx_he] = True

        assert self.hg_name is not None
        return Hypergraph(
            name=self.hg_name, vertex_meta=range(1, v_max + 1), matrix=csr_array(matrix)
        )


class EmpiricalHGReader(HypergraphLineReader):
    def parse_hg_data(self, hg_data: list[str]) -> Hypergraph:
        v_max = 1
        num_hedges = 0

        reading_nodes = True

        edge_start_idx = 0

        for idx, line in enumerate(hg_data):
            if idx == 0:
                continue

            if line.strip() == "edges":
                edge_start_idx = idx
                reading_nodes = False
                continue

            if reading_nodes:
                v = int(line.strip())
                v_max = v if v > v_max else v_max

            else:
                num_hedges += 1

        logger.debug(f"dimensions parsed: {v_max} vertices, {num_hedges} hyperedges")
        if v_max >= 100_000:
            matrix = dok_array((v_max, num_hedges), dtype=bool)
        else:
            matrix = lil_array((v_max, num_hedges), dtype=bool)
        logger.debug("matrix instantiated")

        for idx_he, line in enumerate(hg_data[edge_start_idx + 1 :]):
            logger.debug(f"parsing line {edge_start_idx + 1 + idx_he}")
            line = line.replace("{", "").replace(
                "}", ""
            )  # remove the '{' and '}' at each end

            for vertex in line.split(","):
                matrix[int(vertex.replace("'", "").strip()) - 1, idx_he] = True

        assert self.hg_name is not None
        return Hypergraph(
            name=self.hg_name, vertex_meta=range(1, v_max + 1), matrix=csr_array(matrix)
        )


class HGFReader(HypergraphLineReader):
    def parse_hg_data(self, hg_data: list[str]) -> Hypergraph:
        meta = hg_data[0].split(" ")
        v_max, num_hedges = int(meta[0]), int(meta[1])

        matrix = lil_array((v_max, num_hedges), dtype=bool)

        for idx_he, line in enumerate(hg_data[1:]):
            line = line.replace("=true", "").replace("=1", "")

            for vertex in line.split(" "):
                if vertex.strip() == "":
                    continue
                matrix[int(vertex.strip()) - 1, idx_he] = True

        assert self.hg_name is not None
        return Hypergraph(
            name=self.hg_name, vertex_meta=range(1, v_max + 1), matrix=csr_array(matrix)
        )


class XGIReader(JSONHGReader):
    def parse_hg_data(self, hg_data: dict[str, Any]) -> Hypergraph:
        name = hg_data["hypergraph-data"]["name"]

        nodes = [int(i) for i in hg_data["node-data"].keys()]
        edges = sorted([int(i) for i in hg_data["edge-data"].keys()])

        v_max = max(nodes)
        num_hedges = max(edges) + 1

        logger.debug(f"dimensions parsed: {v_max} vertices, {num_hedges} hyperedges")
        col_idx = []
        row_idx = []
        col_dict = hg_data["edge-dict"]

        for col, rows in col_dict.items():
            col_idx.extend([int(col)] * len(rows))
            row_idx.extend([int(i) - 1 for i in rows])

        data = np.ones(len(row_idx), dtype=bool)
        matrix = coo_array((data, (row_idx, col_idx)), shape=(v_max, num_hedges))

        return Hypergraph(
            name=name, vertex_meta=range(1, v_max + 1), matrix=csr_array(matrix)
        )
