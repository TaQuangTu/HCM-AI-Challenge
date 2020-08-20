import os
import re


def contains_image_path(line):
    match = re.search(".*../cam_(.+?).jpg.*", line)
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


def get_files(dir):
    detection_files = []
    files = os.listdir(dir)
    for file in files:
        if file.endswith("txt") and file != "final.txt":
            detection_files.append(dir+"/"+file)
    return detection_files


if __name__ == "__main__":
    detected_file_name = "detected_files.txt"
    detected_files = open(detected_file_name,"w+")
    detection_result = get_files("DetectionResults")
    detection_result.sort()
    for file in detection_result:
        lines = open(file, "r").readlines()
        index = 0
        for index in range(len(lines)):
            line = lines[index]
            if contains_image_path(line):
                file_name = get_image_path(line)  # cam_01/99
                print(index,file_name)
                detected_files.write(file_name+"\n")
            index +=1
    detected_files.close()

    print("found",len(open(detected_file_name,"r").readlines()),"files")



