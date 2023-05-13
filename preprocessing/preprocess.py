# 调用lconvert, retruct, filter文件，完成预处理
import lconvert
import restruct

root_dir = '../data/img'
lconvert.lconvert(root_dir, odir="../data/img_out")
restruct.restruct(root_dir='../data/img_out')
