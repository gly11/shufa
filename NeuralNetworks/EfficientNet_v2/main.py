import tensorflow as tf
import keras.applications as ka
import keras.layers as tfl

IMG_SIZE = (192, 192)
preprocess_input = ka.efficientnet_v2.preprocess_input
neuron_numbers = 1


def mymodel(image_shape=IMG_SIZE):
    input_shape = image_shape + (3,)

    base_model = ka.efficientnet_v2.EfficientNetV2M(input_shape=input_shape,
                                                    include_top=False,
                                                    weights='imagenet')
    base_model.trainable = False
    inputs = tf.keras.Input(shape=input_shape)
    x = preprocess_input(inputs)
    x = base_model(x, training=False)

    # now build new layers
    x = tfl.GlobalAveragePooling2D()(x)
    x = tfl.Dropout(0.2)(x)
    outputs = tfl.Dense(neuron_numbers)(x)  # neuron_numbers: hyper-parameter
    # outputs = x
    model = tf.keras.Model(inputs, outputs)

    return model


def show_summary():
    input_shape = IMG_SIZE + (3,)
    base_model = ka.efficientnet_v2.EfficientNetV2M(input_shape=input_shape,
                                                    include_top=False,
                                                    weights='imagenet')
    base_model.summary()


def main():
    model = mymodel(IMG_SIZE)
    model.summary()
    # base_learning_rate = 0.001
    # model.compile(optimizer=tf.keras.optimizers.Adam(lr=base_learning_rate),
    #                loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
    #                metrics=['accuracy'])
    # initial_epochs = 5
    # history = model.fit(train_dataset, validation_data=validation_dataset, epochs=initial_epochs)


if __name__ == '__main__':
    main()
