import tensorflow as tf
import keras
import sys
import local_utils
import load_data
strategy = load_data.strategy
print('Number of devices: {}'.format(strategy.num_replicas_in_sync))
sys.path.insert(0, sys.path[0] + "/../")

preprocess_input = keras.applications.efficientnet_v2.preprocess_input
IMG_SIZE = tuple(load_data.IMG_SIZE)
neuron_numbers = load_data.class_num
channels_dict = {'rgb': (3,), 'rgba': (4,), 'grayscale': (1,)}
model_name = "EfficientNetV2S"


def mymodel(image_shape=IMG_SIZE):
    model = tf.keras.models.load_model(f'./{model_name}/weights-02-0.68--0.001.hdf5')
    point = -35
    for layer in model.layers[:point]:
        layer.trainable = False
    for layer in model.layers[point:]:
        layer.trainable = True
    return model


def main():
    with strategy.scope():
        model2 = mymodel()
    model2.summary()

    base_learning_rate = 1e-3
    initial_epochs = 3
    train_dataset, validation_dataset = load_data.train_ds, load_data.val_ds
    model2.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=base_learning_rate),
                   loss='categorical_crossentropy',
                   metrics=['accuracy'])
    filepath = model_name + "/" + "weights-{epoch:02d}-{val_accuracy:.2f}"+f"-{base_learning_rate}.hdf5"
    checkpoint = keras.callbacks.ModelCheckpoint(filepath, monitor='val_accuracy', verbose=1,
                                                 save_best_only=True, mode='max', save_weights_only=False)

    reduce_lr = keras.callbacks.ReduceLROnPlateau(monitor='val_accuracy', factor=0.2, patience=1, mode='auto',
                                                  verbose=1, min_lr=0.0001)

    early_stop = keras.callbacks.EarlyStopping(monitor='val_accuracy', patience=2, verbose=1, mode='auto')
    history = model2.fit(train_dataset, validation_data=validation_dataset,
                         epochs=initial_epochs,
                         callbacks=[checkpoint, reduce_lr, early_stop])
    model2.save('{}/model.h5'.format(model_name))
    local_utils.plot(history, model_name, epoch=initial_epochs, lr=base_learning_rate)


if __name__ == '__main__':
    main()
