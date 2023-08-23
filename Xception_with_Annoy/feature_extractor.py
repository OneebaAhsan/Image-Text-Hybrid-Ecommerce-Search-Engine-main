import logging
from keras.preprocessing import image
from keras.applications.xception import Xception, preprocess_input
from keras.models import Model
import numpy as np

import tensorflow as tf
tf.get_logger().setLevel(logging.ERROR)


class FeatureExtractor:
    def __init__(self):
        self.model = Xception(weights='imagenet', include_top=False, pooling='max')

    def extract(self, img):
        img = img.resize((299, 299))
        img = img.convert('RGB')
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        feature = self.model.predict(x)[0]
        return feature / np.linalg.norm(feature)