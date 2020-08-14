from math import sqrt

from StreamProcessing.Point import Point


def distanceP2P(point1, point2):
    return sqrt((point1.x - point2.x) ** 2 + ((point1.y - point2.y) ** 2))


def is_on_polygon(object, polygon):
    EPSILON = sqrt(object.width ** 2 + object.height ** 2) / 2
    point = Point(object.x_center, object.y_center)
    for i in range(len(polygon.list_points)):
        a, b = polygon.list_points[i - 1], polygon.list_points[i]
        if abs(distanceP2P(a, point) + distanceP2P(b, point) - distanceP2P(a, b)) < EPSILON:
            return True
    return False

