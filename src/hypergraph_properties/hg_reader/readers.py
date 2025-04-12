from scipy.sparse import csr_array, lil_array

from hypergraph_properties.hg_model import Hypergraph
from hypergraph_properties.hg_reader.template import HypergraphReader


class SyntheticHGReader(HypergraphReader):
    def parse_hg_data(self, hg_data: list[str]) -> Hypergraph:
        v_max = 1
        num_hedges = 0

        for line in hg_data:
            num_hedges += 1
            for vertex in line.split(","):
                if int(vertex) > v_max:
                    v_max = int(vertex)

        matrix = lil_array((v_max, num_hedges), dtype=bool)

        for idx_he, line in enumerate(hg_data):
            for vertex in line.split(","):
                matrix[int(vertex) - 1, idx_he] = True

        return Hypergraph(vertex_meta=range(1, v_max + 1), matrix=csr_array(matrix))


class EmpiricalHGReader(HypergraphReader):
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

        matrix = lil_array((v_max, num_hedges), dtype=bool)

        for idx_he, line in enumerate(hg_data[edge_start_idx + 1 :]):
            line = line.replace("{", "").replace(
                "}", ""
            )  # remove the '{' and '}' at each end

            for vertex in line.split(","):
                matrix[int(vertex.replace("'", "").strip()) - 1, idx_he] = True

        return Hypergraph(vertex_meta=range(1, v_max + 1), matrix=csr_array(matrix))
