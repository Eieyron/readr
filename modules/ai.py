import cv2
import logging
import os
import pickle

import numpy as np
import tensorflow.compat.v1 as tf
import keras as ks

from collections import Counter

# suppress all logging from tensorflow
logging.getLogger('tensorflow').disabled = True
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


def load_model_vars():
    return pickle.load(open(os.path.join('.', 'models', 'vars.pkl'), 'rb'))


# n <- number of models to be loaded.
# more accurate but slower if higher
# max of 10.
def load_models(n=1, show=False):
    model_files = sorted([file for file in os.listdir('./models') if file.endswith('.h5')])[0:n]
    models = []

    for model_file in model_files:

        print(model_file)

        model = ks.models.load_model('./models/{}'.format(model_file))
        models.append(model)

    if show:
        for i in range(n):
            print("Model #{} loaded from file: {}".format(i, model_files[i]))
            models[i].summary()

    return models


# preprocess input character to fit into model input
# character <- img to be preprocessed
def preprocess_character(character):
    try:
        # invert
        character = cv2.bitwise_not(character)

        # normalize pixel values
        character = character / 255

        # reshape to fit model input shape
        character = np.expand_dims(character, axis=0)
        character = np.expand_dims(character, axis=3)
        character.reshape((1, 28, 28, 1))
    except ValueError:
        return None
    except TypeError:
        return None

    return character
# returns:
# character <- preprocessed character
# None <- if it cannot for some reason reshape the character


# predict input character with input models
# models <- the models to read the character with
# character <- img to be recognized
def read_character(models, character):
    character = preprocess_character(character)

    if character is not None:
        predictions = []
        predicted_values = []

        for model in models:
            # generate predictions
            prediction = model.predict(character)

            # get the best prediction
            predicted_value = str(np.argmax(prediction))

            # append
            predictions.append(prediction)
            predicted_values.append(predicted_value)

        predicted_character = Counter(predicted_values).most_common(1)[0][0]

        return predictions, predicted_values, predicted_character
    else:
        return None, None, ""
# returns:
# predictions <- predictions generated by the model
# predicted_values <- the most probable classification of the character by model
# predicted_character <- the character most voted by the models
# note:
# returns an empty string if preprocess_character returned None.
