import tensorflow as tf
import tensorflow.keras.layers as tfl
import os

img_path = ''   #数据路径
preprocess_input = tf.keras.applications.resnet_rs.preprocess_input
IMG_SIZE = (160, 160)
IMG_SHAPE = IMG_SIZE + (3,)

def mymodel(input_shape= IMG_SHAPE ):
    base_model = tf.keras.applications.resnet_rs.ResNetRS50(input_shape=input_shape,
                                        include_top=False,
                                        weights='imagenet')
    base_model.trainable = False                # freeze the base model by making it non trainable
    inputs = tf.keras.Input(shape=input_shape)  # 创建输入层
    x = preprocess_input(inputs)
    x = base_model(x, training=False)
    # build new layers
    x = tfl.GlobalAveragePooling2D()(x)
    x = tfl.Dropout(0.2)(x)

    outputs = tfl.Dense(1)(x)               # neuron_numbers: hyper-parameter

    model = tf.keras.Model(inputs, outputs)

    return model

model2 = mymodel(IMG_SHAPE)
model2.summary()

# base_learning_rate = 0.001
# model2.compile(optimizer=tf.keras.optimizers.Adam(lr=base_learning_rate),
            #   loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
            #   metrics=['accuracy'])
# initial_epochs = 5
# history = model2.fit(train_dataset, validation_data=validation_dataset, epochs=initial_epochs)
