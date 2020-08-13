# as mentioned in thread, each polygon includes moving directions and vertices that form the polygon
class Polygon:
    def __init__(self):
        self.moving_directions = []
        self.list_points = []

    def add_direction(self, direction):
        self.moving_directions.append(direction)

    def add_point(self, point):
        self.list_points.append(point)
