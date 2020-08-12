#this script is used for generating testing image paths going to be predicted

import os


def get_all_images(dir, all):
    ls = os.listdir(dir)
    for item in ls:
        path = os.path.join(dir, item)
        if os.path.isfile(path) and path.__contains__(".jpg"):
            all.append(path)
        else:
            if os.path.isdir(path):
                get_all_images(path, all)


if __name__ == "__main__":
    all_images = []
    get_all_images(".", all_images)
    print("found", len(all_images), " images")
    print(all_images)
    txt_file = open("test_all_images.txt", "w+")
    for image in all_images:
        txt_file.write("." + image + "\n")
