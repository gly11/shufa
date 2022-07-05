from PIL import Image
import os.path
import glob
def convertjpg(jpgfile,outdir,width=128,height=128):
    img=Image.open(jpgfile)
    try:
        new_img=img.resize((width,height),Image.BILINEAR)   
        new_img.save(os.path.join(outdir,os.path.basename(jpgfile)))
    except Exception as e:
        print(e)
for jpgfile in glob.glob("E:\\img\\*.jpg"): #图片目录
    convertjpg(jpgfile,"E:\\")        #储存目录
————————————————
版权声明：本文为CSDN博主「A~朱蒙蒙」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/weixin_43122919/article/details/107465516