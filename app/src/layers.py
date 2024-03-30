# Custom Distance Layer Module

# Dependencies
import tensorflow as tf
from tensorflow.keras.layers import Layer

class Dist(Layer):
    def __init__(self, **kwargs):
        super().__init__()
       
    # Similarity Calculation
    def call(self, input_embedding, validation_embedding):
        return tf.math.abs(input_embedding - validation_embedding)