import os
import json

from StreamProcessing.Direction import Direction
from StreamProcessing.Point import Point


def get_points_of_polygon(json_file_path):
    cam_polygon = []
    file = open(json_file_path,"r")
    json_file = json.load(file)
    for shape in json_file["shapes"]:
        if shape["label"] == "zone":
            for point in shape["points"]:
                cam_polygon.append(Point(float(point[0]), float(point[1])))
    return cam_polygon


def get_movement_directions(json_file_path):
    file = open(json_file_path, "r")
    cam_movement_directions = []

    json_file = json.load(file)
    for shape in json_file["shapes"]:
        if shape["shape_type"]== "line":
            first_point = Point(shape["points"][0][0], shape["points"][0][1])
            last_point = Point(shape["points"][1][0], shape["points"][1][1])
            direction_id = int(shape["label"][-2:])
            direction = Direction(first_point, last_point, direction_id)
            cam_movement_directions.append(direction)
    return cam_movement_directions
