import tensorflow
import utils
import time
import json
import numpy as np

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import load_img

from tensorflow.keras.applications.mobilenet import MobileNet, preprocess_input
mobilenet_preprocessor = preprocess_input

IMG_SIZE = (224,224,3)

model = 0
num_to_class = 0

def trained_network_init():
    global model, num_to_class

    model = tensorflow.keras.models.load_model('train_model.h5', compile = False)

    with open('class_to_num.json', 'r') as f:
        class_to_num = json.load(f)
        num_to_class = { val : key for (key,val) in class_to_num.items()}\


def predict(X_path):
    global model,num_to_class

    X = utils.image_path_to_array(X_path)
    mobilenet_features = utils.get_features(MobileNet, mobilenet_preprocessor, IMG_SIZE, X)
    y_pred = model.predict(mobilenet_features)
    
    return y_pred