#提取目录下所有图片,更改尺寸后保存到另一目录
from PIL import Image
import os.path
import glob
def convertjpg(pngfile,outdir,width=128,height=128):
    img=Image.open(pngfile)
    try:
        new_img=img.resize((width,height),Image.BILINEAR)   
        new_img.save(os.path.join(outdir,os.path.basename(pngfile)))
    except Exception as e:
        print(e)
for pngfile in glob.glob("D:\\test\\*.png"): #图片目录
    convertjpg(pngfile,"D:\\")        #保持目录