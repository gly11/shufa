import tensorflow as tf
from keras.utils import image_dataset_from_directory
from glob import glob
import utils


# import matplotlib.pyplot as plt


AUTOTUNE = tf.data.experimental.AUTOTUNE
BATCH_SIZE = 32
IMG_SIZE = (160, 160)
root = utils.get_project_path()
data_root = f"{root}/data/img_selected/"
label_names = sorted(path.split('/')[-1] for path in glob(f"{data_root}*"))
label_to_index = dict((name, index) for index, name in enumerate(label_names))
train_dataset = image_dataset_from_directory(data_root,
                                             shuffle=True,
                                             batch_size=BATCH_SIZE,
                                             image_size=IMG_SIZE,
                                             validation_split=0.2,
                                             subset='training',
                                             seed=42,
                                             label_mode='categorical',
                                             class_names=label_names)
validation_dataset = image_dataset_from_directory(data_root,
                                                  shuffle=True,
                                                  batch_size=BATCH_SIZE,
                                                  image_size=IMG_SIZE,
                                                  validation_split=0.2,
                                                  subset='validation',
                                                  seed=42,
                                                  label_mode='categorical',
                                                  class_names=label_names)
class_names = train_dataset.class_names
# print(class_names)
train_dataset = train_dataset.prefetch(buffer_size=AUTOTUNE)
validation_dataset = validation_dataset.prefetch(buffer_size=AUTOTUNE)
# print(validation_dataset)
