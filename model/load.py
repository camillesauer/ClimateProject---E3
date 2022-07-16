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
sys.path.append(os.path.abspath("./app/"))
from app.models import Img


def init():
    json_file = open('./model/cnn.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model_json = model_from_json(loaded_model_json)
    #load weights into new model
    loaded_model_json.load_weights("./model/cnn.h5")
    print("Loaded Model from disk")

    #compile and evaluate loaded model
    loaded_model_json.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
    return loaded_model_json


def preprocessing_test(path):
    x = Image.open(path)
    x = np.resize(x,(1,75,75,3))
    x = np.array(x)
    x = (x - x.mean())/255.
    return x


def predict(path):
    x = preprocessing_test(path)
    model=init()
    out = model.predict(x)[0][0]
    return round(out),  out