# this script is used for generating final result. It's not totally close to groundtruth right now, we need to update more
import os
import random
import re
import shutil
from math import sqrt
import cv2
import numpy as np

from StreamProcessing.Frame import Frame
from StreamProcessing.Helpers import JsonHelper, MathHelper
from StreamProcessing.Object import Object
from StreamProcessing.Point import Point
from StreamProcessing.Polygon import Polygon
from StreamProcessing.StreamProcessor import StreamProcessor

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


def dist(a, b):
    return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def point_on_polygon(point, poly):
    EPSILON = 60  # unit = px
    for i in range(len(poly)):
        a, b = poly[i - 1], poly[i]
        if abs(dist(a, point) + dist(b, point) - dist(a, b)) < EPSILON:
            return True
    return False


def get_most_similar(obje, list_of_object):
    weights = [0.25, 0.75]
    obje_diagonal_line = obje.calculate_diagonal_line()
    for obj in list_of_object:
        diagonal_line = obj.calculate_diagonal_line()
        obj.similar_score = weights[0] * 1 / abs(diagonal_line - obje_diagonal_line + 0.001) + weights[
            1] * obj.similar_score
    list_of_object.sort(key=lambda x: x.similar_score)
    highest_score = -1
    chosen_obj = None
    for obj in list_of_object:
        print(obj.confident_score)
        distance = MathHelper.distanceP2P(Point(obje.x_center, obje.y_center), Point(obj.x_center, obj.y_center))
        if obj.similar_score > highest_score and obj.class_type == obje.class_type and float(
                obj.confident_score) > 0.4 and distance < obje_diagonal_line:
            chosen_obj = obj
            highest_score = obj.similar_score
    return chosen_obj


def draw_rectangle(obje, frame,polygon):
    image = cv2.imread(frame.video_name + "/" + frame.frame_id + ".jpg")
    half_width = obje.width / 2
    half_height = obje.height / 2
    is_on = MathHelper.is_on_polygon(obje,polygon)
    is_in = MathHelper.is_in_polygon(obje,polygon)
    if is_on:
        name = "ON"
    else:
        if is_in:
            name = "IN"
        else:
            name = "OUT"
    image = cv2.rectangle(image, (int(obje.x_center - half_width), int(obje.y_center - half_height)),
                          (int(obje.x_center + half_width), int(obje.y_center + half_height)), (36, 255, 12), 1)
    cv2.putText(image, name, (int(obje.x_center - half_width), int(obje.y_center - half_height - 10)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
    return image

def draw_directions(image, directions):
    for dir in directions:
        points = [[dir.start_point.x,dir.start_point.y],[dir.end_point.x,dir.end_point.y]]
        pts = np.array(points,
                       np.int32)

        pts = pts.reshape((-1, 1, 2))

        isClosed = True

        # Blue color in BGR
        color = (255, 0, 0)

        # Line thickness of 2 px
        thickness = 2

        # Using cv2.polylines() method
        # Draw a Blue polygon with
        # thickness of 1 px
        image = cv2.polylines(image, [pts],
                              isClosed, color, thickness)
def draw_polyline(image,points):
    points = [[p.x,p.y] for p in points]
    pts = np.array(points,
                   np.int32)

    pts = pts.reshape((-1, 1, 2))

    isClosed = True

    # Blue color in BGR
    color = (255, 0, 0)

    # Line thickness of 2 px
    thickness = 2

    # Using cv2.polylines() method
    # Draw a Blue polygon with
    # thickness of 1 px
    image = cv2.polylines(image, [pts],
                          isClosed, color, thickness)


if __name__ == "__main__":
    detection_file = open("DetectionResults/result.txt", "r")
    lines = detection_file.readlines()
    processing_files = []

    # init processor
    cam_json = "zones-movement_paths/cam_01.json"
    points_of_polygon = JsonHelper.get_points_of_polygon(cam_json)
    directions = JsonHelper.get_movement_directions(cam_json)
    polygon = Polygon(directions, points_of_polygon)
    processor = StreamProcessor(polygon=polygon)

    index = 0
    frames = []
    for index in range(len(lines)):
        line = lines[index]
        if contains_image_path(line):

            file_name = get_image_path(line)  # cam_01/99
            print(file_name)
            video_name, frame_id = file_name.split("/")[0], file_name.split("/")[1]
            cam_no = int(video_name[4:6])

            if cam_no != 1:
                if len(frames) > 100:
                    break

            # create new frame object and put into processor
            frame = Frame(video_name, frame_id)
            for j in range(index + 1, len(lines)):
                next_line = lines[j]
                if contains_bbox(next_line):
                    bbox = get_bbox(next_line)
                    class_name = bbox[0]

                    has_type = False
                    if class_name in Object.ObjectType[1]:
                        has_type = True
                    if class_name in Object.ObjectType[2]:
                        has_type = True
                    if class_name in Object.ObjectType[3]:
                        has_type = True
                    if class_name in Object.ObjectType[4]:
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

                    object = Object(class_name=class_name, confident_score=confidence, x_center=x_center,
                                    y_center=y_center, width=width, height=height)
                    frame.add_object(object)
                else:
                    index = j
                    frames.append(frame)

                    break

    frames.sort(key=lambda x: int(x.frame_id))
    while True:
        if os.path.exists("visual"):
            shutil.rmtree("visual")
        os.mkdir("visual")
        os.mkdir("visual/cam_01")
        test = random.randint(0, len(frames) - 1)
        test_frame = frames[test]
        obj_index = random.randint(0, len(test_frame.objects) - 1)
        obje = test_frame.objects[obj_index]
        image = draw_rectangle(obje, test_frame,polygon)
        draw_polyline(image,polygon.list_points)
        draw_directions(image,directions)
        cv2.imwrite("visual/cam_01/" + test_frame.frame_id + ".jpg", image)
        num_of_similar_for_each_frame = 3
        for i in range(test, min(test + 20, len(frames))):
            next_frame = frames[i]
            if len(next_frame.objects) > 0:
                for obj in next_frame.objects:
                    similar_score = obje.get_similar_score(obj)
                    obj.similar_score = similar_score
                next_frame.objects.sort(key=lambda x: x.similar_score)
                # pick up 2 objects that are most similar to obje
                if len(next_frame.objects) > num_of_similar_for_each_frame:
                    most_similar = get_most_similar(obje, next_frame.objects[-num_of_similar_for_each_frame:])
                else:
                    most_similar = get_most_similar(obje, next_frame.objects)
                if most_similar is None:
                    continue
                obje = most_similar
                image = draw_rectangle(obje, next_frame,polygon)
                draw_polyline(image, polygon.list_points)
                draw_directions(image, directions)
                cv2.imwrite("visual/cam_01/" + next_frame.frame_id + ".jpg", image)
