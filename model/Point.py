from dataclasses import dataclass
from numpy import sqrt


@dataclass(frozen=False)
class Point:
    x: int
    y: int
    z: int

    def __str__(self):
        return " ".join([str(self.x), str(self.y), str(self.z)])

    @staticmethod
    def get_object_from_str(point_str):
        point = list(map(int, point_str.split(' ')))
        assert len(point) == 3
        return Point(x=point[0],
                     y=point[1],
                     z=point[2])

    def __eq__(self, other):
        if isinstance(other, Point):
            return True if all([self.x == other.x, self.y == other.y, self.z == other.z]) else False
        else:
            return False

    def get_distance(self, point):
        return sqrt((self.x - point.x) ** 2 + (self.y - point.y) ** 2 + (self.z - point.z) ** 2)
