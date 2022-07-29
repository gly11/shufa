from vit_keras import vit, utils
#需要tensorflow , tensorflow_addons, numpy

image_size = 384
classes = utils.get_imagenet_classes()
model = vit.vit_b16(
    image_size=image_size,
    activation='sigmoid',
    pretrained=True,
    include_top=True,
    pretrained_top=True
)
url = '' #此处填写图片文件地址
image = utils.read(url, image_size)
X = vit.preprocess_inputs(image).reshape(1, image_size, image_size, 3)
y = model.predict(X)
print(classes[y[0].argmax()])