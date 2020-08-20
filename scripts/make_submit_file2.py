# this script is used for generating final result. It's not totally close to groundtruth right now, we need to update more

import re

from StreamProcessing.Frame import Frame
from StreamProcessing.Helpers import JsonHelper
from StreamProcessing.Object import Object
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



if __name__ == "__main__":
    submit_file = open("submits/submit_file_3.txt", "w+")
    detection_file = open("DetectionResults/final.txt", "r")
    lines = detection_file.readlines()
    processing_files = []
    processed_files_file = open("processed_files.txt", "r")
    processed_files = processed_files_file.readlines()
    number_of_camera = 25

    for i in range(1, number_of_camera + 1):
        # init processor
        cam_json = "zones-movement_paths/cam_" + "{:02d}".format(i) + ".json"
        points_of_polygon = JsonHelper.get_points_of_polygon(cam_json)
        directions = JsonHelper.get_movement_directions(cam_json)
        polygon = Polygon(directions, points_of_polygon)
        processor = StreamProcessor(polygon=polygon)
        # travel through all frames, get prediction for each frame

        index = 0
        frames = []
        for index in range(len(lines)):
            line = lines[index]
            print(index)
            if contains_image_path(line):

                file_name = get_image_path(line)  # cam_01/99
                print(file_name)
                video_name, frame_id = file_name.split("/")[0], file_name.split("/")[1]
                cam_no = int(video_name[4:6])

                if cam_no != i:
                    continue

                # save processing file to avoid repeat processing
                processed_files.append(file_name)

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
                        print(object)
                        frame.add_object(object)
                    else:
                        index = j
                        frames.append(frame)

                        break

        frames.sort(key=lambda x: int(x.frame_id))
        for frame in frames:
            movements = processor.process_new_frame(frame)
            for movement in movements:
                print(movement)
                submit_file.write(
                    frame.video_name + " " + frame.frame_id + " " + str(movement.direction.direction_id) + " " + str(
                        movement.obj.class_type) + "\n")
    processed_files_file.close()
    processed_files_file = open("processed_files.txt", "a")
    for processing_file in processing_files:
        processed_files_file.write(processing_file + "\n")
