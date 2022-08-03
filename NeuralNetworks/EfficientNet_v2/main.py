import tensorflow as tf
import keras.losses as kl
import keras.layers as tfl
import keras.applications as ka
import NeuralNetworks.build_dataset as build_dataset


preprocess_input = ka.efficientnet_v2.preprocess_input
IMG_SIZE = build_dataset.IMG_SIZE
neuron_numbers = len(build_dataset.label_names)


def mymodel(image_shape=IMG_SIZE):
    input_shape = image_shape + (3,)
    base_model = ka.efficientnet_v2.EfficientNetV2M(input_shape=input_shape,
                                          include_top=False,
                                          weights='imagenet')
    base_model.trainable = False  # freeze the base model by making it non trainable
    inputs = tf.keras.Input(shape=input_shape)  # 创建输入层
    x = preprocess_input(inputs)
    x = base_model(x, training=False)

    # build new layers
    x = tfl.GlobalAveragePooling2D()(x)
    x = tfl.Dropout(0.2)(x)
    outputs = tfl.Dense(neuron_numbers, activation='softmax')(x)  # neuron_numbers: hyper-parameter
    # outputs = x
    model = tf.keras.Model(inputs, outputs)
    return model


def main():
    model2 = mymodel(IMG_SIZE)
    # model2.summary()
    base_learning_rate = 0.001
    model2.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=base_learning_rate),
                   loss=kl.CategoricalCrossentropy(),
                   metrics=['accuracy'])
    initial_epochs = 5
    train_dataset = build_dataset.train_dataset
    validation_dataset = build_dataset.validation_dataset
    history = model2.fit(train_dataset, validation_data=validation_dataset, epochs=initial_epochs, steps_per_epoch=100)
    print(history)


if __name__ == '__main__':
    main()
