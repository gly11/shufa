import tensorflow as tf
import keras
# import os
# import build_dataset
import sys
import local_utils
import load_data
strategy = load_data.strategy
print('Number of devices: {}'.format(strategy.num_replicas_in_sync))
sys.path.insert(0, sys.path[0] + "/../")

preprocess_input = keras.applications.efficientnet_v2.preprocess_input
# IMG_SIZE = build_dataset.IMG_SIZE
# neuron_numbers = len(build_dataset.label_names)
IMG_SIZE = tuple(load_data.IMG_SIZE)
neuron_numbers = load_data.class_num
channels_dict = {'rgb': (3,), 'rgba': (4,), 'grayscale': (1,)}
model_name = "EfficientNetV2S"
unfrozen = -70


def mymodel(image_shape=IMG_SIZE):
    # input_shape = image_shape + channels_dict[build_dataset.color_mode]
    input_shape = image_shape + channels_dict[load_data.color_mode]
    base_model = keras.applications.efficientnet_v2.EfficientNetV2S(input_shape=input_shape,
                                                                    include_top=False,
                                                                    weights='imagenet')
    # base_model.trainable = False  # 冻结所有层
    # 冻结部分层
    # frozen_layer_number = 250
    for layer in base_model.layers[:unfrozen]:
        # 5层可训练
        layer.trainable = False
    inputs = tf.keras.Input(shape=input_shape)  # 创建输入层
    x = preprocess_input(inputs)
    x = base_model(x, training=False)

    # build new layers
    x = keras.layers.GlobalAveragePooling2D()(x)
    x = keras.layers.Dropout(0.4)(x)
    outputs = keras.layers.Dense(neuron_numbers, activation='softmax')(x)  # neuron_numbers: hyper-parameter
    # outputs = x
    model = tf.keras.Model(inputs, outputs)
    return model


def main():
    with strategy.scope():
        model2 = mymodel(IMG_SIZE)
    model2.summary()

    base_learning_rate = 1e-3
    initial_epochs = 30
    # train_dataset, validation_dataset = build_dataset.build_train_val()
    train_dataset, validation_dataset = load_data.train_ds, load_data.val_ds
    model2.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=base_learning_rate),
                   loss='categorical_crossentropy',
                   metrics=['accuracy'])

    # checkpoint_path = f"{model_name}/cp.ckpt"
    # checkpoint_dir = os.path.dirname(checkpoint_path)

    # # Create a callback that saves the model's weights
    # checkpoint = keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
    #                                              verbose=1,
    #                                              save_weights_only=True)

    # checkpoint
    filepath = model_name + "/" + "weights-{epoch:02d}-{val_accuracy:.2f}"+f"-{base_learning_rate}-{unfrozen}.hdf5"
    checkpoint = keras.callbacks.ModelCheckpoint(filepath, monitor='val_accuracy', verbose=1,
                                                 save_best_only=True, mode='max', save_weights_only=False)

    reduce_lr = keras.callbacks.ReduceLROnPlateau(monitor='val_accuracy', factor=0.2, patience=1, mode='auto',
                                                  verbose=1, min_lr=1e-5)

    early_stop = keras.callbacks.EarlyStopping(monitor='val_accuracy', patience=2, verbose=1, mode='auto')

    # TensorBoardcallback = keras.callbacks.TensorBoard(log_dir=f'./{model_name}/logs',
    #                                                   histogram_freq=1, write_graph=True, write_grads=False,
    #                                                   write_images=True, embeddings_freq=0, embeddings_layer_names=None,
    #                                                   embeddings_metadata=None, embeddings_data=None,
    #                                                   update_freq='epoch')
    # model2.load_weights(f'./{model_name}/weights-04-0.61.hdf5')
    history = model2.fit(train_dataset, validation_data=validation_dataset,
                         epochs=initial_epochs,
                         callbacks=[checkpoint, reduce_lr, early_stop])
    # print(history.history)
    model2.save('{}/model.h5'.format(model_name))
    local_utils.plot(history, model_name, epoch=initial_epochs, lr=base_learning_rate)


if __name__ == '__main__':
    main()
