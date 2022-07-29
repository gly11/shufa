import cv2
import os
from tqdm import tqdm


def main():
    # 将黑底白字转换为白底黑字
    rootdir = r'./img'
    for parent, dirnames, filenames in os.walk(rootdir):
        # parent: 即rootdir(当前目录); filenames: 当前目录下的子文件夹列表; filenames: 当前目录下的文件列表
        for filename in tqdm(filenames):
            try:
                if filename.split('.')[-1] == 'png':
                    currentPath = f"{parent}/{filename}"
                    # print('The full filename is:' , currentPath)
                    src = cv2.imread(currentPath, cv2.IMREAD_UNCHANGED)           # 打开当前文件夹中图片
                    img = cv2.cvtColor(src, cv2.COLOR_BGRA2GRAY)           # 进行灰度化
                    if cv2.countNonZero(img) == 0:
                        # 判断是否为纯黑，若是，则直接返回原值，不做处理
                        img = src

                    ## 仅选取出透明背景图片 ##
                    else:
                        continue

                    '''
                    else:
                        # 若不是，则进行二值化、反色等处理
                        x,y= img.shape                  # 长宽
                        # img = cv2.GaussianBlur(img, (5, 5), 0)        # 高斯滤波去噪
                        img = cv2.medianBlur(img, 7)                    # 均值滤波去噪(均值去噪效果好于高斯，数值越大去噪效果越好，但从7开始某些过于细小的笔画丢失)
                        cv2.threshold(img,128,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU,img)
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
                    '''
                    odir = "img_selected"               # 设定输出文件夹
                    # 判断文件夹是否存在，若不存在则创建之
                    if not os.path.exists(odir):
                        os.mkdir(odir)
                    path = f'./{odir}/{filename}'           #保存地址
                    cv2.imwrite(path, img)
                    # print(f"{path}已保存！")

            except Exception as err:
                print(f'Error: {err}')


if __name__ == '__main__':
    main()


"""
版权声明：本文为CSDN博主「用余生去守护」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/qq_45365214/article/details/122935575
"""
