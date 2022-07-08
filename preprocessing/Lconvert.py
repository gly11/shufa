import cv2
import os


def re_name(path):
    files = os.listdir(path)
    for i, file in enumerate(files):
        try:
            new_file_name = os.path.join(path, str(i) + '.jpg')
            old_file_name = os.path.join(path, file)
            os.rename(old_file_name, new_file_name)
        except:
            continue


def gray_pic(path):
    files = os.listdir(path)
    for file in enumerate(files):
        try:
            pic = path + str(file[1])
            original_img = cv2.imread(pic)
            gray = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(path + str(file[1]), gray)
        except:
            continue


path = r'./converted_size/'
#re_name(path)
gray_pic(path)

