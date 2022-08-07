import tensorflow as tf
import keras
import os
import build_dataset
import local_utils

preprocess_input = keras.applications.resnet_rs.preprocess_input
IMG_SIZE = build_dataset.IMG_SIZE
neuron_numbers = len(build_dataset.label_names)
channels_dict = {'rgb': (3,), 'rgba': (4,), 'grayscale': (1,)}
model_name = "ResNetRS50"


def mymodel(image_shape=IMG_SIZE):
    input_shape = image_shape + channels_dict[build_dataset.color_mode]
    base_model = keras.applications.resnet_rs.ResNetRS50(input_shape=input_shape,
                                                         include_top=False,
                                                         weights='imagenet')
    base_model.trainable = False  # 冻结所有层
    # 冻结部分层
    # frozen_layer_number = 250
    # for layer in base_model.layers[:frozen_layer_number + 1]:
    #     layer.trainable = False
    inputs = tf.keras.Input(shape=input_shape)  # 创建输入层
    x = preprocess_input(inputs)
    x = base_model(x, training=False)

    # build new layers
    x = keras.layers.GlobalAveragePooling2D()(x)
    x = keras.layers.Dropout(0.2)(x)
    outputs = keras.layers.Dense(neuron_numbers, activation='softmax')(x)  # neuron_numbers: hyper-parameter
    # outputs = x
    model = tf.keras.Model(inputs, outputs)
    return model


def main():
    model2 = mymodel(IMG_SIZE)
    # model2.summary()
    base_learning_rate = 0.001
    model2.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=base_learning_rate),
                   loss='categorical_crossentropy',
                   metrics=['accuracy'])
    initial_epochs = 20
    train_dataset = build_dataset.train_dataset
    validation_dataset = build_dataset.validation_dataset

    checkpoint_path = f"{model_name}/cp.ckpt"
    checkpoint_dir = os.path.dirname(checkpoint_path)

    # Create a callback that saves the model's weights
    cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                     verbose=1,
                                                     save_weights_only=True,
                                                     # save_freq=5 * build_dataset.BATCH_SIZE
                                                     )

    history = model2.fit(train_dataset, validation_data=validation_dataset,
                         epochs=initial_epochs, callbacks=[cp_callback])
    # print(history.history)
    local_utils.plot(history, model_name, epoch=initial_epochs, lr=base_learning_rate)


if __name__ == '__main__':
    main()
