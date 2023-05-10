import cv2
import numpy as np

def split(t, input_pic = './test_col.png'):
    # t: type:类型
    
    out_path = './output/'
    # dsize = 28
    img = cv2.imread(input_pic)
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)            # 灰度化
    cv2.threshold(img,128,255,cv2.THRESH_BINARY,img)        # 二值化
    # cv2.imshow("img", img)                                  # 显示二值化结果
    # cv2.waitKey(5000)                                       # 等待1秒
    data = np.array(img)
    len_x = data.shape[0]           # 纵向高度
    len_y = data.shape[1]           # 横向宽度
    print("{}, {}".format(len_x, len_y))
    if t == 'x':
        split_x(data, len_x, len_y, out_path)
    elif t == 'y':
        split_y(data, len_x, len_y, out_path)
    else:
        print("WORONG INPUT!")


# 用于横向书写文字
def split_x(data, len_x, len_y, out_path):
    # 行分割
    start_i = -1
    end_i = -1
    min_val = 1
    rowPairs = []
    for i in range(len_x):
        if (not data[i].all() and start_i < 0):
            start_i = i
        elif not data[i].all():
            end_i = i
        elif (data[i].all() and start_i >=0):
            if end_i - start_i > min_val:
                rowPairs.append((start_i, end_i))
            start_i, end_i = -1, -1
    print(rowPairs)

    # 列分割为单字
    start_j = -1
    end_j = -1
    blank = 0
    min_val_blank = 2
    min_val_word = 5
    number = 1
    for start, end in rowPairs:
        for j in range(len_y):
            if not data[start:end, j].all() and start_j < 0:
                start_j = j
                blank = 0
            elif not data[start:end, j].all():
                end_j = j
                blank = 0
            elif data[start:end, j].all() and start_j >= 0:
                if blank < min_val_blank:
                    blank += 1
                    # print(blank)
                # else:
                #     end_j = j
                else: 
                    if end_j - start_j >= min_val_word:
                        tmp = data[start:end, start_j:end_j]
                        # im2save = cv2.resize(tmp, (dsize, dsize)) 
                        im2save = tmp
                        cv2.imwrite(out_path + '%d.png' % number, im2save)
                        number += 1
                    start_j, end_j = -1, -1
                    blank = 0

# 用于纵向书写文字
def split_y(data, len_x, len_y, out_path):
    # 将图片分割为多列
    start_i = -1
    end_i = -1
    min_val = 1
    colPairs = []
    for i in range(len_y):
        if (not data[:, i].all() and start_i < 0):
            start_i = i
        elif not data[:, i].all():
            end_i = i
        elif (data[:, i].all() and start_i >=0):
            if end_i - start_i > min_val:
                colPairs.append((start_i, end_i))
            start_i, end_i = -1, -1
    if colPairs == []:
        colPairs = [(len_x, len_y)]
    colPairs.reverse()      # 反转，使得按照从右至左的顺序进行识别
    print(colPairs)

    # 将每一列分割为单字
    start_j = -1
    end_j = -1
    blank = 0
    min_val_blank = 10
    min_val_word = 5
    number = 1
    for start, end in colPairs:
        for j in range(len_x):
            if j != len_x-1:
                if not data[j, start:end].all() and start_j < 0:
                    start_j = j
                    blank = 0
                elif not data[j, start:end].all():
                    end_j = j
                    blank = 0
                elif data[j, start:end].all() and start_j >= 0:
                    if blank < min_val_blank:
                        blank += 1
                        # print(blank)
                    # else:
                    #     end_j = j
                    else:
                        if end_j - start_j >= min_val_word:
                            tmp = data[start_j:end_j, start:end]
                            # im2save = cv2.resize(tmp, (dsize, dsize))
                            im2save = tmp
                            cv2.imwrite(out_path + '%d.png' % number, im2save)
                            number += 1
                        start_j, end_j = -1, -1
                        blank = 0
            else:
                # 保证在最后一个字贴近边缘时也能输出
                if j-start_j >= min_val_word and end_j != -1:
                    im2save = data[start_j:end_j, start:end]
                    cv2.imwrite(out_path + '%d.png' % number, im2save)



split('y')