#this script is used for generating testing image paths going to be predicted

import os


def get_all_images(dir, all):
    ls = os.listdir(dir)
    for item in ls:
        path = os.path.join(dir, item)
        if os.path.isfile(path) and path.__contains__("cam_") and path.__contains__(".jpg"):
            all.append(path)
        else:
            if os.path.isdir(path):
                get_all_images(path, all)


if __name__ == "__main__":
    txt_file = open("test_all_images.txt", "w+")
    processed_files = open("detected_files.txt").readlines()
    processed_files = [x.replace("\n","") for x in processed_files]
    print(processed_files)
    for i in range(1,25):
        cam = "cam_"+"{:02d}".format(i)
        for frame in range(1,13501):
            file = cam+"/"+str(frame)
            print(file)
            if file in processed_files:
                print("ignore========================================================================",file)
                continue
            else:
                txt_file.write("../"+file+".jpg"+"\n")
