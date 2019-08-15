import os

import numpy as np
import tensorflow as tf

from modules.ai import load_model_vars


def load_models(n=1, show=False):
    model_files = sorted([file for file in os.listdir('./models') if file.endswith('.h5')])[0:n]
    print(model_files)
    models = []
    for model_file in model_files:
        model = tf.keras.models.load_model('./models/{}'.format(model_file))
        models.append(model)

    if show:
        for i in range(n):
            print("Model #{} loaded from file: {}".format(i, model_files[i]))
            models[i].summary()

    return models


if __name__ == '__main__':
    mean_px, std_px = load_model_vars()
    print("Mean px: {}, Std px: {}".format(mean_px, std_px))

    models = load_models(10, False)

    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

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
    y_train = tf.keras.utils.to_categorical(y_train, 10)
    y_test = tf.keras.utils.to_categorical(y_test, 10)

    eval_batch_size = 512

    # evaluate every model
    evals = np.array([m.evaluate(x_test, y_test, batch_size=eval_batch_size) for m in models])
    # calculate mean from evaluations
    print("Mean: {}".format(evals.mean(axis=0)))
