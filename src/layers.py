import tensorflow as tf
import numpy as np
from tensorflow.keras import activations, initializers, regularizers, constraints
from tensorflow.keras import backend as K
from tensorflow.keras.layers import Layer, Dense

# Rewrite version of https://github.com/danielegrattarola/spektral/blob/master/spektral/layers/pooling/global_pool.py


class GlobalPooling(Layer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.supports_masking = True
        self.batch_pooling_op = None

    def call(self, inputs):
        return self.batch_pooling_op(inputs, axis=-2, keepdims=False)

    def compute_output_shape(self, input_shape):
        return input_shape[:-2] + input_shape[-1:]

    def get_config(self):
        return super().get_config()


class GlobalSumPool(GlobalPooling):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.batch_pooling_op = tf.reduce_sum


class GlobalMeanPool(GlobalPooling):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.batch_pooling_op = tf.reduce_mean

# Rewrite version of https://github.com/danielegrattarola/spektral/blob/master/spektral/layers/convolutional/graph_conv.py


class GraphConv(Layer):
    def __init__(self,
                 features,
                 activation=None,
                 kernel_initializer='glorot_uniform',
                 bias_initializer='zeros',
                 **kwargs):

        super().__init__(**kwargs)
        self.features = features
        self.activation = activations.get(activation)
        self.kernel_initializer = initializers.get('glorot_uniform')
        self.bias_initializer = initializers.get('zeros')
        self.supports_masking = False

    def build(self, input_shape):
        assert len(input_shape) >= 2
        input_dim = input_shape[0][-1]
        self.kernel = self.add_weight(shape=(input_dim, self.features),
                                      initializer=self.kernel_initializer,
                                      name='kernel')

        self.bias = self.add_weight(shape=(self.features,),
                                    initializer=self.bias_initializer,
                                    name='bias')

        self.built = True

    def call(self, inputs):
        features = inputs[0]
        matrix = inputs[1]

        output = tf.matmul(features, self.kernel)
        output = tf.matmul(matrix, output)
        output = K.bias_add(output, self.bias)

        if self.activation is not None:
            output = self.activation(output)

        return output

    def compute_output_shape(self, input_shape):
        features_shape = input_shape[0]
        output_shape = features_shape[:-1] + (self.features,)
        return output_shape

    def get_config(self):
        config = {
            'features': self.features,
            'activation': activations.serialize(self.activation),
            'kernel_initializer': initializers.serialize(self.kernel_initializer),
            'bias_initializer': initializers.serialize(self.bias_initializer),
        }
        base_config = super().get_config()
        return dict(list(base_config.items()) + list(config.items()))
