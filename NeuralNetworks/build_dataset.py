import tensorflow as tf
from keras.utils import image_dataset_from_directory
from glob import glob
import utils
import os

# import matplotlib.pyplot as plt


AUTOTUNE = tf.data.experimental.AUTOTUNE
BATCH_SIZE = 32
X = 128
IMG_SIZE = (X, X)
root = utils.get_project_path()
data_root = f"{root}/data/img_selected_30/"
dataset_name = data_root.split("/")[-2]
label_names = sorted(os.path.split(path)[-1] for path in glob(f"{data_root}*"))
label_to_index = dict((name, index) for index, name in enumerate(label_names))
color_mode = 'rgb'


# 构建用于训练的数据集
def build_train_val(path=data_root):
    train_dataset = image_dataset_from_directory(path,
                                                 shuffle=True,
                                                 batch_size=BATCH_SIZE,
                                                 image_size=IMG_SIZE,
                                                 validation_split=0.2,
                                                 subset='training',
                                                 seed=42,
                                                 label_mode='categorical',
                                                 class_names=label_names,
                                                 color_mode=color_mode)
    validation_dataset = image_dataset_from_directory(data_root,
                                                      shuffle=True,
                                                      batch_size=BATCH_SIZE,
                                                      image_size=IMG_SIZE,
                                                      validation_split=0.2,
                                                      subset='validation',
                                                      seed=42,
                                                      label_mode='categorical',
                                                      class_names=label_names,
                                                      color_mode=color_mode)
    # class_names = train_dataset.class_names
    # print(class_names)
    train_dataset = train_dataset.prefetch(buffer_size=AUTOTUNE)
    validation_dataset = validation_dataset.prefetch(buffer_size=AUTOTUNE)
    # print(validation_dataset)
    return train_dataset, validation_dataset


# 构建用于预测的数据集
def build_pred(path=data_root):
    data2pred = image_dataset_from_directory(path, shuffle=False,
                                                      batch_size=BATCH_SIZE,
                                                      image_size=IMG_SIZE,
                                                      color_mode=color_mode)
    return data2pred