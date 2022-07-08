from cgitb import grey
import cv2
import os
from tqdm import tqdm
import cv2
from skimage import io

#import os
path = r"C:/Pywork/shufa1/test_cv2/" #path后面记得加 /
#西瓜6的代码
fileList = os.listdir(path)
for i in tqdm(fileList):
    image = io.imread(path+i)  # image = io.imread(os.path.join(path, i))
    image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGRA)
    cv2.imencode('.png',image)[1].tofile(path+i)
##解除由版本升级导致的"libpng warning: iCCP: known incorrect sRGB profile"问题

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
            #将图片转换成灰度图片
            pic = path + "\\" + str(file[1])
            original_img = cv2.imread(pic)
            gray = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
            
            #将灰度图像二值化，设定阈值为100
            img_thre = gray
            cv2.threshold(gray,100,255,cv2.THRESH_BINARY_INV,img_thre)

            #保存黑白图片
            cv2.imwrite(path + "\\" + str(file[1]), gray)

            #分割字符
            white = []          #记录每一列的白色像素总和
            black = []          #....黑色...
            height = img_thre.shape[0]
            width = img_thre.shape[1]
            white_max = 0
            black_max = 0

                #计算每一列的黑白色像素总和
            for i in range(width):
                s = 0   #这一列的白色总数
                t = 0   #这一列的黑色总数
                for i in range(height):
                    if img_thre[j][i] == 255:
                        s += 1
                    if  img_thre[j][i] == 0:
                        t += 1
                    white_max = max(white_max,s)
                    black_max = max(black_max,t)
                    white.append(s)
                    black.append(t)
                print(s)
                print(t)
            arg = False #False表示白底黑字；True表示黑底白字
            if black_max > white_max:
                arg = True
            
            #分割图像
            def find_end(start_):
                end_ = start_+1
                for m in range(start_+1, width-1):
                    if (black[m] if arg else white[m]) > (0.95 * black_max if arg else 0.95 * white_max): 
                        # 0.95这个参数请多调整，对应下面的0.05
                        end_ = m
                    break
                return end_
            n = 1
            start = 1
            end = 2
            while n < width-2:
                n += 1
            if (white[n] if arg else black[n]) > (0.05 * white_max if arg else 0.05* black_max):
                start = n
                end = find_end(start)
                n = end 
                if end - start >5:
                    cj = img_thre[1:height, start:end]
                    cv2.imwrite(path)
        except:
            continue

path = r'C:\Pywork\shufa1\test_cv2'
#re_name(path)
try:
    gray_pic(path)        #实现灰度转换

    #将黑底白字转换为白底黑字
    nn = 1
    str_name1 = 'cut'
    str_name3 = '.png'
    rootdir = r'C:\Pywork\shufa1\test_cv2'
    for parent, dirnames, filenames in os.walk(rootdir):
        for filename in filenames:
            print('parent is :' , parent)
            print('filename is :' , filename)
            currentPath = os.path.join(parent, filename)
            print('THe full filename is:' , currentPath)
            image = cv2.imread(currentPath)           #打开当前文件夹中图片
            #计算白色和黑色像素分别的总和
            white1 = []          #记录每一列的白色像素总和
            black1 = []          #....黑色...
            height1 = image.shape[0]
            width1 = image.shape[1]
            white_max1 = 0
            black_max1 = 0

                #计算图像的黑白色像素总和
            for i in range(width1):
                s = 0   #这一列的白色总数
                t = 0   #这一列的黑色总数
                for j in range(height1):
                    if image[j,i] == 255:      #在此处需要弄清楚为什么image[j][i] == 255不能表示像素
                        s += 1
                    if  image[j,i] == 0:
                        t += 1
                    white_max = max(white_max1,s)
                    black_max = max(black_max,t)
                    white1.append(s)
                    black1.append(t)
                print(s)
                print(t)

                #将黑底白字的图片转换为白底黑字的图片
            if white_max  < black_max :
                image2=cv2.bitwise_not(image)
                dizhi = r'C:\Pywork\shufa1\test_cv2'
                dizhi = dizhi + str_name1 + str(nn) + str_name3
                cv2.imwrite(dizhi, image2)
            nn = 1

except Exception as err:
    print(f'Error! Info: {err}')