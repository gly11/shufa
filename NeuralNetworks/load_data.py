import tensorflow as tf
# import numpy as np
import pandas as pd
import utils
import matplotlib.pyplot as plt
from collections import Counter

root = utils.get_project_path()
img_root = f"{root}/data/img_out/"
csv_path = f'{root}/data/csv_files'
csv_file = f"{csv_path}/data_100_removed.csv"
channels = 3
color_mode = 'rgb'

IMG_SIZE = [128, 128]
AUTOTUNE = tf.data.AUTOTUNE
BATCH_SIZE = 32

df = pd.read_csv(csv_file, encoding='utf-8')
index2label = dict(zip(df['No.'], df['Word']))
img_count = len(index2label.keys())
counter = Counter(df['Word'])  # class: Counter
class_num = len(counter.values())
label_indexing = dict(zip(counter.keys(), range(class_num)))
df['indexed_label'] = [label_indexing[w] for w in df['Word']]
df['No.'] = img_root + df['No.'].astype(str) + '.png'

one_hot = tf.one_hot(df['indexed_label'], class_num, on_value=1)
img_label_ds = tf.data.Dataset.from_tensor_slices((df['No.'], one_hot))


def load_img(path, label):
    img = tf.io.read_file(path)
    img = tf.image.decode_png(img, channels=channels)
    img = tf.image.resize(img, IMG_SIZE)
    return img, label


img_label_ds = img_label_ds.shuffle(img_count, reshuffle_each_iteration=False, seed=42)
val_size = int(img_count * 0.2)
train_ds = img_label_ds.skip(val_size)
val_ds = img_label_ds.take(val_size)

# Set `num_parallel_calls` so multiple images are loaded/processed in parallel.
train_ds = train_ds.map(load_img, num_parallel_calls=AUTOTUNE)
val_ds = val_ds.map(load_img, num_parallel_calls=AUTOTUNE)

print(f'train: {tf.data.experimental.cardinality(train_ds).numpy()}')
print(f'val: {tf.data.experimental.cardinality(val_ds).numpy()}')

# for image, label in train_ds.take(1):
#     # print(image)
#     print("Image shape: ", image.numpy().shape)
#     print("Label: ", label.numpy())


def configure_for_performance(ds):
    ds = ds.cache()
    ds = ds.shuffle(buffer_size=1000)
    ds = ds.batch(BATCH_SIZE)
    ds = ds.prefetch(buffer_size=AUTOTUNE)
    return ds


train_ds = configure_for_performance(train_ds)
val_ds = configure_for_performance(val_ds)

# image_batch, label_batch = next(iter(train_ds))
# plt.figure(figsize=(10, 10))
# for i in range(9):
#     ax = plt.subplot(3, 3, i + 1)
#     plt.imshow(image_batch[i].numpy().astype("uint16"))
#     # label = label_batch[i]
#     # plt.title(class_names[label])
#     plt.axis("off")