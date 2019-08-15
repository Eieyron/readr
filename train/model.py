# requires tensorflow==2.0.0a0
# pip install tensorflow==2.0.0a0

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from tensorflow import keras

import os
import pickle

import numpy as np
import tensorflow as tf

tf.keras.backend.set_image_data_format('channels_last')


# function to normalize input data
def norm_input(x): return (x - mean_px) / std_px


def create_model():
    model = keras.models.Sequential()
    model.add(keras.layers.Lambda(norm_input, input_shape=(28, 28, 1), output_shape=(28, 28, 1)))
    model.add(keras.layers.Conv2D(32, (3, 3)))
    model.add(keras.layers.LeakyReLU())
    model.add(keras.layers.BatchNormalization(axis=-1))
    model.add(keras.layers.Conv2D(32, (3, 3)))
    model.add(keras.layers.LeakyReLU())
    model.add(keras.layers.MaxPooling2D())
    model.add(keras.layers.BatchNormalization(axis=-1))
    model.add(keras.layers.Conv2D(64, (3, 3)))
    model.add(keras.layers.LeakyReLU())
    model.add(keras.layers.BatchNormalization(axis=-1))
    model.add(keras.layers.Conv2D(64, (3, 3)))
    model.add(keras.layers.LeakyReLU())
    model.add(keras.layers.MaxPooling2D())
    model.add(keras.layers.Flatten())
    model.add(keras.layers.BatchNormalization())
    model.add(keras.layers.Dense(512))
    model.add(keras.layers.LeakyReLU())
    model.add(keras.layers.BatchNormalization())
    model.add(keras.layers.Dropout(0.3))
    model.add(keras.layers.Dense(10, activation='softmax'))

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    return model


def fit_model(m, i):
    m.fit_generator(batches, steps_per_epoch=steps_per_epoch, epochs=1,
                    validation_data=test_batches, validation_steps=validation_steps)
    m.optimizer.lr = 0.1
    m.save('./models/w_m' + str(i) + '_e1.h5')
    m.fit_generator(batches, steps_per_epoch=steps_per_epoch, epochs=4,
                    validation_data=test_batches, validation_steps=validation_steps)
    m.optimizer.lr = 0.01
    m.save('./models/w_m' + str(i) + '_e5.h5')
    m.fit_generator(batches, steps_per_epoch=steps_per_epoch, epochs=12,
                    validation_data=test_batches, validation_steps=validation_steps)
    m.optimizer.lr = 0.001
    m.save('./models/w_m' + str(i) + '_e17.h5')
    m.fit_generator(batches, steps_per_epoch=steps_per_epoch, epochs=18,
                    validation_data=test_batches, validation_steps=validation_steps)
    m.save('./models/w_m' + str(i) + '_e35.h5')
    return m


def format_dataset(file_dev='./dev.pkl'):
    if os.path.isfile(file_dev):
        print("Found existing file: " + file_dev)
        mean_px, std_px = pickle.load(open(file_dev, 'rb'))
        print("Loaded existing file: " + file_dev)
    else:
        print("Found no existing file: " + file_dev)
        print("Creating new file")

        (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

        # store labels on test set for visualization
        test_labels = y_test

        # x_train.shape

        # vgg expects channels - here we have just one
        x_train = x_train.reshape(x_train.shape[0], 28, 28, 1)
        x_test = x_test.reshape(x_test.shape[0], 28, 28, 1)
        # x_train.shape

        # convert to float
        x_train = x_train.astype(np.float32)
        x_test = x_test.astype(np.float32)

        # normalize
        x_train /= 255
        x_test /= 255

        # y_train.shape

        # labels should be onehot encoded
        y_train = keras.utils.to_categorical(y_train, 10)
        y_test = keras.utils.to_categorical(y_test, 10)

        # calculate mean and standard deviation
        mean_px = x_train.mean().astype(np.float32)
        std_px = x_train.std().astype(np.float32)

        dev = mean_px, std_px
        pickle.dump(dev, open(file_dev, "wb"))
        print("Created new file: " + file_dev)

    return mean_px, std_px


if __name__ == '__main__':
    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

    # store labels on test set for visualization
    test_labels = y_test

    # x_train.shape

    # vgg expects channels - here we have just one
    x_train = x_train.reshape(x_train.shape[0], 28, 28, 1)
    x_test = x_test.reshape(x_test.shape[0], 28, 28, 1)
    # x_train.shape

    # convert to float
    x_train = x_train.astype(np.float32)
    x_test = x_test.astype(np.float32)

    # normalize
    x_train /= 255
    x_test /= 255

    # y_train.shape

    # labels should be onehot encoded
    y_train = keras.utils.to_categorical(y_train, 10)
    y_test = keras.utils.to_categorical(y_test, 10)

    # calculate mean and standard deviation
    mean_px = x_train.mean().astype(np.float32)
    std_px = x_train.std().astype(np.float32)

    # augment data
    batch_size = 512

    gen = keras.preprocessing.image.ImageDataGenerator(
        rotation_range=12,
        width_shift_range=0.1,
        shear_range=0.3,
        height_shift_range=0.1,
        zoom_range=0.1,
        data_format='channels_last')

    batches = gen.flow(x_train, y_train, batch_size=batch_size)
    test_batches = gen.flow(x_test, y_test, batch_size=batch_size)
    steps_per_epoch = int(np.ceil(batches.n / batch_size))
    validation_steps = int(np.ceil(test_batches.n / batch_size))

    # train and save
    models = []
    for i in range(0, 10):
        print("Training model {}".format(i))
        m = fit_model(create_model(), i)
        print("Done training model {}".format(i))
        m.save('model_'+str(i)+'.h5')
        models.append(m)

    notif = "Done training all 10!"

    # load models
    models = [keras.models.load_model('./models/w_m'+str(i)+'_eF.h5') for i in range(10)]
    print("Models successfully loaded!")

    # if you wish to go even further..
    for i in range(10):
        print("Loading model {}".format(i))
        m = keras.models.load_model('./models/w_m' + str(i) + '_eF.h5')
        print("Done loading model {}".format(i))

        print("Training model {}".format(i))
        m.optimizer.lr = 0.0001
        m.fit_generator(batches, steps_per_epoch=steps_per_epoch, epochs=4,
                        validation_data=test_batches, validation_steps=validation_steps)

        print("Done training model {}".format(i))

        m.save('./models/w_m' + str(i) + '_eF2.h5')

        print("Saved model {}".format(i))

    # evaluate the models (optional)
    print("Evaluating models")
    eval_batch_size = 512

    # evaluate every model
    evals = np.array([m.evaluate(x_test,y_test, batch_size=eval_batch_size) for m in models])

    # calculate mean from evaluations
    evals.mean(axis=0)

    for i, m in enumerate(models):
        m.save('./models/w_m' + str(i) + '_eF.h5')

    print("Done!")
