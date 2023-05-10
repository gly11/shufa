# import tensorflow as tf
import keras
import NeuralNetworks.build_dataset as build_dataset
import numpy as np

model_name = 'EfficientNetV2S'
model = keras.models.load_model('./NeuralNetworks/{}/model.h5'.format(model_name))
data2pred = build_dataset.build_pred(path="./split/output/")
label2index = build_dataset.label_to_index
index2label = dict(zip(label2index.values(), label2index.keys()))
pred = list(np.argmax(model.predict(data2pred), axis=1))
result = []
for i in pred:
    result.append(index2label[i])
print(result)