# 将图片按照不同的字归入文件夹，并以该字命名文件夹
import os
from tqdm import tqdm
import csv
import shutil
import glob


def move_file(srcfile, dstpath):  # 移动函数
    _, fname = os.path.split(srcfile)  # 分离文件名和路径
    if not os.path.exists(dstpath):
        os.mkdir(dstpath)  # 创建路径
    shutil.move(srcfile, dstpath + fname)  # 移动文件
    # print("move %s -> %s" % (srcfile, dstpath + fname))


def restruct(root_dir):
    with open("../data/csv_files/data.csv", encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        dic = dict(reader)
    filenames = glob.glob(f"{root_dir}/*.png")
    # print(filenames)
    for file in tqdm(filenames):
        try:
            # print(file)
            num = file.split("/")[-1].split(".")[0]
            num = num.split('\\')[-1]       # win平台下使用
            word = dic[num]
            odir = f"{root_dir}/{word}/"  # 设定输出文件夹
            move_file(file, odir)
        except Exception as err:
            print(f'Error: {err}')


if __name__ == "__main__":
    restruct(root_dir="../data/img_selected")
