# as mentioned in thread, each polygon includes moving directions and vertices that form the polygon
from StreamProcessing.Helpers import MathHelper
from StreamProcessing.Intersection import Intersection


class Polygon:
    def __init__(self, moving_directions, points):
        self.moving_directions = moving_directions
        self.list_points = points
        self.intersections = self.build_intersections(self.moving_directions,
                                                      self.list_points)  # calculate all intersections between direction and edges

    def add_direction(self, direction):
        self.moving_directions.append(direction)

    def add_point(self, point):
        self.list_points.append(point)

    def build_intersections(self, directions, points):
        intersections = []
        for direction in directions:
            for i in range(len(points)):
                a, b = points[i], points[i - 1]
                intersection = Intersection(direction, a, b)
                if not intersection.is_out_roi():
                    intersections.append(intersection)
        return intersections
