# this class abstracts for intersection between a direction and polygon segments
from StreamProcessing.Point import Point


class Intersection:
    MAX_X = 1290
    MAX_Y = 790
    MIN_X = -10
    MIN_Y = -10

    def __init__(self, direction, vertice1, vertice2):
        self.vertice1 = vertice1
        self.vertice2 = vertice2
        self.point = self.__find_intersection(direction, vertice1, vertice2)
        self.direction = direction

    def is_out_roi(self):
        return self.point.x >= Intersection.MAX_X or self.point.y >= Intersection.MAX_Y or self.point.x <= Intersection.MIN_X or self.point.y <= Intersection.MIN_Y

    def __str__(self):
        return str(self.point.x) + "," + str(self.point.y)

    def __find_intersection(self, direction, vertice1, vertice2):
        x1 = direction.start_point.x
        y1 = direction.start_point.y
        x2 = direction.end_point.x
        y2 = direction.end_point.y
        x3 = vertice1.x
        y3 = vertice1.y
        x4 = vertice2.x
        y4 = vertice2.y

        denumorator_x = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if denumorator_x == 0:
            return Point(Intersection.MAX_X, Intersection.MAX_Y)
        numerator_x = (x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)
        numerator_y = (x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)
        px = numerator_x / denumorator_x
        py = numerator_y / denumorator_x
        return Point(px, py)
