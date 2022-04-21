from dataclasses import dataclass
from model.Point import Point
import numpy as np


@dataclass(frozen=False)
class Triangle:
    nodes: np.ndarray
    indices_neighbours = np.array([], dtype=int)
    contamination_level: int = 0
    coefficient_diffusion: float = 0.
    index_selected_neighbor: int = None

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

    def check_contain_point(self, x, y, z=None):
        def get_triangle_area(point1, point2, point3) -> float:
            return abs((point1.x - point3.x) * (point2.y - point3.y) + (point2.x - point3.x) * (point3.y - point1.y))

        area = get_triangle_area(self.nodes[0], self.nodes[1], self.nodes[2])

        point = Point(x=x, y=y, z=z)
        area1 = get_triangle_area(self.nodes[0], self.nodes[1], point)
        area2 = get_triangle_area(self.nodes[0], point, self.nodes[2])
        area3 = get_triangle_area(self.nodes[1], point, self.nodes[2])
        return area == area1 + area2 + area3

    def select_index_neighbour(self, method, neighbours):
        def is_boundary():
            return not self.indices_neighbours.shape[0] == 3

        def find_common_points(triangle):
            return list(filter(lambda point: point in triangle.nodes, self.nodes))

        random_value = np.random.randint(0, 100)
        if len(self.indices_neighbours) == 1:
            self.index_selected_neighbor = -1 if 0 <= random_value < 50 else self.indices_neighbours[0]
        else:
            if method == "equally probable":
                ghostly_neighbor = is_boundary()
                probable = 100 / (self.indices_neighbours.shape[0] + ghostly_neighbor)
                for index, index_neighbour in enumerate(self.indices_neighbours):
                    if index * probable <= random_value < (index + 1) * probable:
                        self.index_selected_neighbor = index_neighbour
                        return
                self.index_selected_neighbor = -1
            else:
                distances = np.array([])
                for neighbour in neighbours:
                    common_point_1, common_point_2 = find_common_points(triangle=neighbour)
                    distances = np.append(distances, common_point_1.get_distance(point=common_point_2))
                index_max_value = int(np.argmax(distances))
                index_min_value = int(np.argmin(distances))
                index_middle_value = list({0, 1, 2} - {index_min_value, index_max_value})[0]
                if len(self.indices_neighbours) == 2:
                    self.index_selected_neighbor = -1 if 0 <= random_value < 20 else \
                        self.indices_neighbours[index_max_value if 20 <= random_value < 40 else index_min_value]
                else:
                    self.index_selected_neighbor = self.indices_neighbours[
                        index_max_value if 0 <= random_value < 20 else
                        index_middle_value if 20 <= random_value < 50 else
                        index_min_value
                    ]
