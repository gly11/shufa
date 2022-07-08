# 提取目录下所有图片,更改尺寸后保存到另一目录
from PIL import Image
import os.path
import glob


width = height = 128


def convert_jpg(_pngfile, outdir, _width, _height):
    img = Image.open(_pngfile)
    try:
        new_img = img.resize((_width, _height), Image.BILINEAR)
        new_img.save(os.path.join(outdir, os.path.basename(_pngfile)))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    for pngfile in glob.glob("./img/*.png"):  # 图片目录，设置为该目录下的子目录，名为img
        convert_jpg(pngfile, "./converted_size/", width, height)  # 保持目录
