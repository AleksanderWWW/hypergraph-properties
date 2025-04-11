from scipy.sparse import lil_array, csr_array

from hypergraph_properties.hg_model import Hypergraph
from hypergraph_properties.hg_reader.template import HypergraphReader


class SyntheticHGReader(HypergraphReader):
    def parse_hg_data(self, hg_data: list[str]) -> Hypergraph[int]:
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
