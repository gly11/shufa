import cv2
import  numpy as np
import os

try:
    # 将黑底白字转换为白底黑字
    str_name1 = 'cut'
    str_name3 = '.png'
    rootdir = r'./test_cv2'
    for parent, dirnames, filenames in os.walk(rootdir):
        # parent: 即rootdir(当前目录); filenames: 当前目录下的子文件夹列表; filenames: 当前目录下的文件列表
        for filename in filenames:
            # print('parent is:' , parent)
            # print('filename is:' , filename)
            # currentPath = os.path.join(parent, filename)
            currentPath = f"{parent}/{filename}"
            print('The full filename is:' , currentPath)
            img = cv2.imread(currentPath)           #打开当前文件夹中图片
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)           #并进行灰度化
            
            #打印长宽
            x,y= img.shape
            # print(img.shape)
            cv2.threshold(img,128,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU,img)
            black = 0
            white = 0
            #计算黑白比例：遍历二值图，为 0 则black+1，否则white+1
            for i in range(x):
                for j in range(y):
                    if img[i,j]==0:
                        black+=1
                    else:
                        white+=1
            # print("白色个数:",white)
            # print("黑色个数:",black)
            rate1 = white/(x*y) #白色像素占比
            rate2 = black/(x*y) #黑色像素占比
            #round()第二个值为保留几位有效小数。
            # print("白色占比:", round(rate1*100,2),'%')
            # print("黑色占比:", round(rate2*100,2),'%')
            #将黑色像素大于白色像素的图片进行Bitwise 的反转
            if rate1 < rate2:
                img = cv2.bitwise_not(img)    #image2是反转后的图像
            dizhi = r'./test_cv2_converted/'           #保存地址
            dizhi = dizhi + filename
            cv2.imwrite(dizhi, img)
            print(f"{dizhi}已保存！")

except:
    print(f'Error!')

"""
版权声明：本文为CSDN博主「用余生去守护」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/qq_45365214/article/details/122935575
"""