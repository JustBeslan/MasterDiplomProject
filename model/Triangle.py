from dataclasses import dataclass
from model.Point import Point
import numpy as np


@dataclass(frozen=False)
class Triangle:
    nodes: np.ndarray
    indices_neighbours = np.array([], dtype=int)
    contamination_level: int = 0
    coefficient_diffusion: float = 0.

    def __dict__(self):
        return {"nodes": [node.__str__() for node in self.nodes],
                "neighbours": ' '.join([str(neighbour) for neighbour in self.indices_neighbours])}

    @staticmethod
    def get_object_from_str(dictionary):
        nodes = np.array([Point.get_object_from_str(node_str) for node_str in dictionary["nodes"]])
        assert len(nodes) == 3
        triangle = Triangle(nodes=nodes)
        indices_neighbours = \
            np.array(list(
                map(float, dictionary["neighbours"].split(" "))
            ), dtype=int)
        assert len(indices_neighbours) <= 3
        triangle.indices_neighbours = indices_neighbours
        return triangle

    def find_common_points(self, triangle):
        return list(filter(lambda point: point in triangle.nodes, self.nodes))
