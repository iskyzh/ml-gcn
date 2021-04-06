import tensorflow as tf
from layers import GraphConv, GlobalMeanPool
from data import PASTE_SIZE, ELEMENT_SELECTED


def build_model():
    # https://arxiv.org/pdf/1812.00265.pdf
    in_features = tf.keras.layers.Input(shape=(PASTE_SIZE, ELEMENT_SELECTED))
    in_matrix = tf.keras.layers.Input(shape=(PASTE_SIZE, PASTE_SIZE))
    conv = GraphConv(128, activation='relu')([in_features, in_matrix])
    conv = tf.keras.layers.BatchNormalization()(conv)
    conv = GraphConv(256, activation='relu')([conv, in_matrix])
    conv = tf.keras.layers.BatchNormalization()(conv)
    conv = GraphConv(512, activation='relu')([conv, in_matrix])
    conv = tf.keras.layers.BatchNormalization()(conv)
    sum_pool = GlobalMeanPool()(conv)
    output = tf.keras.layers.Dense(128)(sum_pool)
    output = tf.keras.layers.Dropout(0.25)(output)
    output = tf.keras.layers.Dense(2, activation='softmax')(output)

    model = tf.keras.Model(inputs=[in_features, in_matrix], outputs=output)

    model.compile(loss=tf.keras.losses.BinaryCrossentropy(),
                  optimizer=tf.keras.optimizers.Adam(0.001),
                  metrics=[tf.keras.metrics.AUC(),
                           'accuracy'])
    return model


if __name__ == '__main__':
    model = build_model()
    print("tf.__version__=", tf.__version__)
    print(model.summary())
