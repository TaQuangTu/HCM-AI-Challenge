# this script is used for generating final result. It's not totally close to groundtruth right now, we need to update more

import json
import os
import random
import re
from math import sqrt

type1 = ["bicycle", "motorbike"]
type2 = ["car"]
type3 = ["bus"]
type4 = ["train", "truck"]


def contains_image_path(line):
    match = re.search(".*../cam_(.+?).jpg.*", line)
    if match:
        return True
    else:
        return False


def contains_bbox(line):
    match = re.search("(.*):.*[0-9]+.*left_x: *(\d+) *top_y: *(\d+) *width: *(\d+) *height: *(\d+)", line)
    if match:
        return True
    else:
        return False


def get_image_path(line):
    match = re.search(".*../cam_(.+?).jpg.*", line)
    if match:
        img_path = match.group(1)
        result_file = img_path
        return "cam_" + result_file
    # else return NoneType


def get_bbox(line):
    # cyclist: 71 % (left_x:  268   top_y:  240   width:  105   height:  123)
    match = re.search("(.*): *(\d+) *%.*left_x: *(\d+) *top_y: *(\d+) *width: *(\d+) *height: *(\d+)", line)
    if match:
        return match.groups(1)


def get_polygons():
    cam_polygon = []
    items = os.listdir("zones-movement_paths")
    for item in items:
        cam_polygon.append([])
    for item in items:
        cam_no = int(item[4:6])
        if item.__contains__("json"):
            json_file = json.load(open(os.path.join("zones-movement_paths", item)))
        for shape in json_file["shapes"]:
            if shape["label"] == "zone":
                continue
            else:
                for point in shape["points"]:
                    cam_polygon[cam_no].append([float(point[0]), float(point[1])])
    return cam_polygon


def get_movement_directions():
    cam_movement_directions = []
    items = os.listdir("zones-movement_paths")
    for item in items:
        cam_movement_directions.append([])
    cam_movement_directions.append([])
    for item in items:
        cam_no = int(item[4:6])
        if item.__contains__("json"):
            json_file = json.load(open(os.path.join("zones-movement_paths", item)))
            for shape in json_file["shapes"]:
                if shape["label"] == "zone":
                    continue
                else:
                    cam_movement_directions[cam_no].append(shape["label"])
    return cam_movement_directions


def dist(a, b):
    return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def point_on_polygon(point, poly):
    EPSILON = 60  # unit = px
    for i in range(len(poly)):
        a, b = poly[i - 1], poly[i]
        if abs(dist(a, point) + dist(b, point) - dist(a, b)) < EPSILON:
            return True
    return False


if __name__ == "__main__":
    file_names = []
    processed_files_txt = open("processed_files.txt","w+")
    directions = get_movement_directions()
    polygons = get_polygons()
    print(directions)
    print(polygons)
    predict_results = "result.txt"  # txt file
    detection_file = open(predict_results, "r")
    submit_file = open("submits/" + predict_results + "_submit.txt", "w+")
    lines = detection_file.readlines()
    index = 0
    number_of_files = 0
    for index in range(len(lines)):
        line = lines[index]
        if contains_image_path(line):
            number_of_files += 1
            file_name = get_image_path(line)  # cam_01/99
            file_names.append(file_name)
            video_name, frame_id = file_name.split("/")[0], file_name.split("/")[1]
            cam_no = int(video_name[4:6])
            for i in range(index + 1, len(lines)):
                next_line = lines[i]
                if contains_bbox(next_line):
                    bbox = get_bbox(next_line)
                    class_name = bbox[0]

                    has_type = False
                    if class_name in type1:
                        class_name = "1"
                        has_type = True
                    if class_name in type1:
                        class_name = "2"
                        has_type = True
                    if class_name in type1:
                        class_name = "3"
                        has_type = True
                    if class_name in type1:
                        class_name = "4"
                        has_type = True
                    if not has_type:
                        continue
                    confidence = str(float(bbox[1]) / 100.0)
                    left_x = int(bbox[2])
                    top_y = int(bbox[3])
                    width = int(bbox[4])
                    height = int(bbox[5])
                    x_center = left_x + width / 2
                    y_center = top_y + height / 2
                    if not point_on_polygon([x_center, y_center], polygons[cam_no]):
                        continue
                    content = video_name + " " + frame_id + " " + str(int(directions[cam_no][
                                                                              random.randint(0, len(
                                                                                  directions[cam_no]) - 1)][
                                                                          -2:])) + " " + class_name + "\n"
                    submit_file.write(content)
                else:
                    index = i
                    break
    file_names.sort()
    print(file_names)
    for fn in file_names:
        processed_files_txt.write(fn+"\n")
    print("found {number_of_files}", len(file_names))
