# 筛选出图片个数大于x的字(须在分好文件夹后使用)
import os
import shutil
from tqdm import tqdm


def dir_exist(path):
    if not os.path.exists(path):
        os.mkdir(path)


def filter(root, x):
    dst_root = f"{root}_{x}"
    dir_exist(dst_root)
    for parent, _, filenames in os.walk(root):
        if len(filenames) >= x:
            word = os.path.split(parent)[-1]
            for filename in tqdm(filenames):
                src = parent + "/" + filename
                dst_path = f"{dst_root}/{word}"
                dir_exist(dst_path)
                shutil.copy(src=src, dst=f"{dst_path}/{filename}")


if __name__ == "__main__":
    path = "../data/img_selected"
    filter(path, 30)
