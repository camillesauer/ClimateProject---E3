import tensorflow as tf
from keras.models import model_from_json, load_model
import tensorflow.keras.backend as K
import numpy as np
from imageio import imread, imsave
from PIL import Image
import re
import sys
import os
sys.path.append(os.path.abspath("/home/apprenant/PycharmProjects/ClimateProject---E3/app/"))
from app.models import Img


def init():
    json_file = open('/home/apprenant/PycharmProjects/ClimateProject---E3/model/model_tuner.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model_json = model_from_json(loaded_model_json)
    #load weights into new model
    loaded_model_json.load_weights("/home/apprenant/PycharmProjects/ClimateProject---E3/model/model_tuner.h5")
    print("Loaded Model from disk")

    #compile and evaluate loaded model
    loaded_model_json.compile(loss='sparse_categorical_crossentropy',optimizer='adam',metrics=['accuracy'])
    return loaded_model_json


def predict(path):
    x = imread(path)
    x = np.resize(x,(1,75,75,3))
    model = init()
    out = model.predict(x)
    print(out)
    response = np.argmax(out,axis=1)
    print(response)
    return [response[0], out[0][0]]

