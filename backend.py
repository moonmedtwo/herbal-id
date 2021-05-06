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

if __name__ == '__main__':
    model = tensorflow.keras.models.load_model('train_model.h5', compile = False)

    with open('class_to_num.json', 'r') as f:
        class_to_num = json.load(f)
        num_to_class = { val : key for (key,val) in class_to_num.items()}
    

    X = utils.image_path_to_array('test_data/bachphuclinh_50.jpg')
    mobilenet_features = utils.get_features(MobileNet, mobilenet_preprocessor, IMG_SIZE, X)
    y_pred = model.predict(mobilenet_features)
    
    print(y_pred)
    print(f'predict: {num_to_class[np.argmax(y_pred)]}')
