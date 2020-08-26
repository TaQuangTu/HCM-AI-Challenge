from math import sqrt

from numpy.linalg import norm
from shapely.geometry import Point as Pt
from shapely.geometry.polygon import Polygon as Pn
import numpy as np

import StreamProcessing.Object
import StreamProcessing.Point
from shapely.geometry import LineString


def two_lines_intersect(p1, p2, p3, p4):
    line = LineString([(p1.x, p1.y), (p2.x, p2.y)])
    other = LineString([(p3.x, p3.y), (p4.x, p4.y)])
    return line.intersects(other)


def distanceP2Line(p1, p2, p3):
    p1 = np.asarray((p1.x, p1.y))
    p2 = np.asarray((p2.x, p2.y))
    p3 = np.asarray((p3.x, p3.y))
    return np.abs(np.cross(p2 - p1, p1 - p3)) / norm(p2 - p1)


def distanceP2P(point1, point2):
    return sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)


def is_intersecting(object, polygon):
    p1 = Pn([(o.x, o.y) for o in polygon.list_points])
    obj_half_width = object.width / 2
    obj_half_height = object.height / 2
    top_left = (object.x_center - obj_half_width, object.y_center - obj_half_height)
    bottom_right = (object.x_center + obj_half_width, object.y_center + obj_half_height)
    top_right = (object.x_center + obj_half_width, object.y_center - obj_half_height)
    bottom_left = (object.x_center - obj_half_width, object.y_center + obj_half_height)
    p2 = Pn([top_left, top_right, bottom_left, bottom_right])
    return p1.intersects(p2)


def is_on_polygon(object, polygon):
    obj_half_width = object.width / 2
    obj_half_height = object.height / 2
    EPSILON = 0
    top_left = StreamProcessing.Object.Object(class_name="None", confident_score=0,
                                              x_center=object.x_center - EPSILON - obj_half_width,
                                              y_center=object.y_center - EPSILON - obj_half_height, width=-1, height=-1)
    bottom_right = StreamProcessing.Object.Object(class_name="None", confident_score=0,
                                                  x_center=object.x_center + EPSILON + obj_half_width,
                                                  y_center=object.y_center + EPSILON + obj_half_height, width=-1,
                                                  height=-1)
    top_right = StreamProcessing.Object.Object(class_name="None", confident_score=0,
                                               x_center=object.x_center + EPSILON + obj_half_width,
                                               y_center=object.y_center - EPSILON - obj_half_height, width=-1,
                                               height=-1)
    bottom_left = StreamProcessing.Object.Object(class_name="None", confident_score=0,
                                                 x_center=object.x_center - EPSILON - obj_half_width,
                                                 y_center=object.y_center + EPSILON + obj_half_height, width=-1,
                                                 height=-1)

    object_polygon = Pn([(top_left.x_center, top_left.y_center),
                         (top_right.x_center, top_right.y_center),
                         (bottom_right.x_center, bottom_right.y_center),
                         (bottom_left.x_center, bottom_left.y_center)])
    for i in range(len(polygon.list_points)):
        a, b = polygon.list_points[i], polygon.list_points[i - 1]
        p_ab = Pn([(a.x, a.y), (b.x, b.y), (b.x + 0.1, b.y + 0.1)])
        if p_ab.intersects(object_polygon):
            return a.x, a.y, b.x, b.y
    return None
    # has_in = False
    # has_out = False
    # for p in (top_left, top_right, bottom_left, bottom_right):
    #     if is_in_polygon(p, polygon):
    #         has_in = True
    #     else:
    #         has_out = True
    # return has_in and has_out


def is_in_polygon(object, polygon):
    point = Pt(object.x_center, object.y_center)
    points = []
    for p in polygon.list_points:
        points.append((p.x, p.y))
    polygon = Pn(points)
    return polygon.contains(point)


def is_middle(p, p1, p2): #check if p is in middle of two other points
    if (p1.x - p.x + 0.0001) / (p.x - p2.x + 0.0001) < 0:
        return False
    if (p1.y - p.y + 0.0001) / (p.y - p2.y + 0.0001) < 0:
        return False
    return True

def findIntersection(x1, y1, x2, y2, x3, y3, x4, y4):
    numerator_x = (x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)
    denumorator_x = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    numerator_y = (x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)
    px = numerator_x / denumorator_x
    py = numerator_y / denumorator_x
    return [px, py]
