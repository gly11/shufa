import tensorflow as tf
# import numpy as np
import pandas as pd
import utils
import matplotlib.pyplot as plt

root = utils.get_project_path()
img_root = f"{root}/data/img_out/"
csv_path = f'{root}/data/csv_files/data.csv'
channels = 3
IMG_SIZE = [128, 128]

df = pd.read_csv(csv_path, encoding='utf-8')
index2label = dict(zip(df['No.'], df['Word']))

df['No.'] = img_root + df['No.'].astype(str) + '.png'
img_label_ds2 = tf.data.Dataset.from_tensor_slices((df['No.'], df['Word']))


def load_img(path, label):
    img = tf.io.read_file(path)
    img = tf.image.decode_png(img, channels=channels)
    img = tf.image.resize(img, IMG_SIZE)
    return img, label


def plot_img(datasets, count):
    for (i, img) in enumerate(datasets.take(count)):
        plt.subplot(2, 2, i + 1)
        plt.imshow(img)
        plt.xticks([])
        plt.yticks(([]))
    plt.show()

img_label_ds2 = img_label_ds2.map(load_img)

for (img, label) in img_label_ds2.take(4):
    print('img:', img[0, 0, 0].numpy())
    print('label', index2label[label.numpy()])
