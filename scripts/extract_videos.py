import cv2
import os


def get_all_video(dir, all_folders):
    ls = os.listdir(dir)

    for item in ls:
        path = os.path.join(dir, item)
        if os.path.isfile(path):
            all_folders.append(path)


if __name__ == "__main__":
    all_folders = []
    get_all_video("videos", all_folders)
    print("found", len(all_folders), " videos")
    print(all_folders)

    for file in all_folders:
        file = file[:-4]
        octets = file.split("/")
        print("Writing to ", octets[1])
        vidcap = cv2.VideoCapture(file + ".mp4")
        success, image = vidcap.read()
        count = 1
        while success:
            print("write to", octets[1] + "/" + str(count) + ".jpg")
            cv2.imwrite(octets[1] + "/" + str(count) + ".jpg", image)  # save frame as JPEG file
            success, image = vidcap.read()
            count += 1
