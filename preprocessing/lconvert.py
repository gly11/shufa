import cv2
import os
from tqdm import tqdm


def lconvert():
    # 将黑底白字转换为白底黑字
    root_dir = '../data/test'
    for parent, dirnames, filenames in os.walk(root_dir):
        # parent: 即rootdir(当前目录); filenames: 当前目录下的子文件夹列表; filenames: 当前目录下的文件列表
        for filename in tqdm(filenames):
            try:
                if filename.split('.')[-1] == 'png':
                    currentPath = f"{parent}/{filename}"
                    # print('The full filename is:' , currentPath)
                    src = cv2.imread(currentPath, cv2.IMREAD_UNCHANGED)           # 打开当前文件夹中图片
                    # 判断是否为透明背景图片
                    if src.shape[2] == 4:
                        img = transparence2white(src)
                        print(img.shape)
                    # ## 仅选取出透明背景图片 ##
                    # else:
                    #     continue
                    else:
                        img = cv2.cvtColor(src, cv2.COLOR_BGRA2GRAY)           # 进行灰度化
                        # print(f'{filename}:{src.shape}')
                        cv2.threshold(img, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU, img)  # 进行二值化
                        x,y= img.shape                  # 长宽
                        # img = cv2.GaussianBlur(img, (5, 5), 0)        # 高斯滤波去噪
                        img = cv2.medianBlur(img, 5)                    # 均值滤波去噪(均值去噪效果好于高斯，数值越大去噪效果越好，但从7开始某些过于细小的笔画丢失)
                        black = 0
                        white = 0
                        # 计算黑白比例：遍历二值图，为 0 则black+1，否则white+1
                        for i in range(x):
                            for j in range(y):
                                if img[i,j]==0:
                                    black+=1
                                else:
                                    white+=1
                        #将黑色像素大于白色像素的图片进行Bitwise 的反转
                        # print(f"{black}, {white}")
                        if white < black:
                            img = cv2.bitwise_not(img)    #image2是反转后的图像

                    # odir = "img_selected"               # 设定输出文件夹
                    odir = "../data/img_out"  # 设定输出文件夹
                    # 判断文件夹是否存在，若不存在则创建之
                    if not os.path.exists(odir):
                        os.mkdir(odir)
                    path = f'{odir}/{filename}'           #保存地址
                    cv2.imwrite(path, img)
                    # print(f"{path}已保存！")

            except Exception as err:
                print(f'Error: {err}')


# 将透明4通道png转化为3通道白底黑字
def transparence2white(img):
    sp = img.shape
    w = sp[0]   # width of img
    h = sp[1]   # height of img
    for y in range(h):
        for x in range(w):
            if img[x, y][3] == 0:
                img[x, y] = (255, 255, 255, 255)
    img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
    return img


if __name__ == '__main__':
    lconvert()
