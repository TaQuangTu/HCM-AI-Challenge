from math import sqrt

from numpy.linalg import norm
from shapely.geometry import Point as Pt
from shapely.geometry.polygon import Polygon as Pn
import numpy as np
from StreamProcessing.Point import Point


def distanceP2Line(p1, p2, p3):
    p1 = np.asarray((p1.x,p1.y))
    p2 = np.asarray((p2.x, p2.y))
    p3 = np.asarray((p3.x, p3.y))
    return np.abs(np.cross(p2 - p1, p1 - p3)) / norm(p2 - p1)


def distanceP2P(point1, point2):
    return sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)


def is_on_polygon(object, polygon):
    EPSILON = 6  # sqrt(object.width ** 2 + object.height ** 2) / 2
    point = Point(object.x_center, object.y_center)
    for i in range(len(polygon.list_points)):
        a, b = polygon.list_points[i - 1], polygon.list_points[i]
        if abs(distanceP2P(a, point) + distanceP2P(b, point) - distanceP2P(a, b)) <= EPSILON and distanceP2Line(a,b,Point(object.x_center,object.y_center))<16:
            return True
    return False


def is_in_polygon(object, polygon):
    point = Pt(object.x_center, object.y_center)
    points = []
    for p in polygon.list_points:
        points.append((p.x, p.y))
    polygon = Pn(points)
    return polygon.contains(point)
