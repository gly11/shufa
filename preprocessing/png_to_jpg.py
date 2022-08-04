from PIL import Image
import os
from tqdm import tqdm


def PNG_JPG(png_path):
    outfile = os.path.splitext(png_path)[0] + ".jpg"
    img = Image.open(png_path)
    try:
        if len(img.split()) == 4:
            # prevent IOError: cannot write mode RGBA as BMP
            img = pure_pil_alpha_to_color_v2(img)
            img.save(outfile ,quality=90)
            os.remove(png_path)
        else:
            img.convert('RGB').save(outfile, quality=90)
            os.remove(png_path)
        return outfile
    except Exception as e:
        print("PNG转换JPG 错误", e)


def pure_pil_alpha_to_color_v2(image, color=(255, 255, 255)):
    """Alpha composite an RGBA Image with a specified color.
    Simpler, faster version than the solutions above.
    Source: http://stackoverflow.com/a/9459208/284318

    Keyword Arguments:
    image -- PIL RGBA Image object
    color -- Tuple r, g, b (default 255, 255, 255)
    """
    image.load()  # needed for split()
    background = Image.new('RGB', image.size, color)
    background.paste(image, mask=image.split()[3])  # 3 is the alpha channel
    return background


def rgb_to_1(file):
    img = Image.open(file)
    # print(len(img.split()))
    if len(img.split()) == 3:
        # RGB
        img.convert("1").save(file, quality=90)


if __name__ == "__main__":
    path_root = os.getcwd()
    path = '../data/test_img'  # 结尾不加/
    for parent, _, filenames in os.walk(path):
        # print(parent)
        for filename in tqdm(filenames):
            file = f"{parent}/{filename}"
            if filename.endswith('.png'):
                PNG_JPG(file)
            # if filename.endswith('.jpg'):
            #     rgb_to_1(file)
