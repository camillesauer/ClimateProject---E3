import tensorflow as tf
from keras.models import model_from_json, load_model
import tensorflow.keras.backend as K
from keras.models import model_from_yaml
import numpy as np
from imageio import imread, imsave
from PIL import Image
import re
import pandas
import sys
import os
sys.path.append(os.path.abspath("/home/apprenant/PycharmProjects/ClimateProject---E3/app/"))
from app.models import Img


def init():
    json_file = open('/home/apprenant/PycharmProjects/ClimateProject---E3/model/cnn.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model_json = model_from_json(loaded_model_json)
    #load weights into new model
    loaded_model_json.load_weights("/home/apprenant/PycharmProjects/ClimateProject---E3/model/cnn.h5")
    print("Loaded Model from disk")

    #compile and evaluate loaded model
    loaded_model_json.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
    return loaded_model_json

def predict(path):
    x = imread(path)
    x = np.resize(x,(1,75,75,3))
    model=init()
    out = model.predict(x)[0][0]
    out = round(out)
    prediction = model.predict(x)[0][0]
    return out,  prediction