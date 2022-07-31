import tensorflow as tf
import keras.layers as tfl
import keras.applications as ka

img_path = ''  # 数据路径
preprocess_input = ka.resnet_rs.preprocess_input
IMG_SIZE = (192, 192)
neuron_numbers = 1


def mymodel(image_shape=IMG_SIZE):
    input_shape = image_shape + (3,)
    base_model = ka.resnet_rs.ResNetRS101(input_shape=input_shape,
                                          include_top=False,
                                          weights='imagenet')
    base_model.trainable = False  # freeze the base model by making it non trainable
    inputs = tf.keras.Input(shape=input_shape)  # 创建输入层
    x = preprocess_input(inputs)
    x = base_model(x, training=False)

    # build new layers
    x = tfl.GlobalAveragePooling2D()(x)
    x = tfl.Dropout(0.2)(x)
    outputs = tfl.Dense(neuron_numbers)(x)  # neuron_numbers: hyper-parameter
    # outputs = x
    model = tf.keras.Model(inputs, outputs)

    return model


def main():
    model2 = mymodel(IMG_SIZE)
    model2.summary()
    # base_learning_rate = 0.001
    # model2.compile(optimizer=tf.keras.optimizers.Adam(lr=base_learning_rate),
    #                loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
    #                metrics=['accuracy'])
    # initial_epochs = 5
    # history = model2.fit(train_dataset, validation_data=validation_dataset, epochs=initial_epochs)


if __name__ == '__main__':
    main()
