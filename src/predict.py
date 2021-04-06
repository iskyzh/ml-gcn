import tensorflow as tf
from data import build_data, to_numpy_array, to_tensor_slice, process_smile, process_label
import pandas as pd
import numpy as np


def predict(model):
    data = build_data("test", label_path="output_sample.txt")
    chemical = data['Chemical']
    data = to_numpy_array(data)
    data = to_tensor_slice(data)
    data = data.map(process_smile)
    data = data.map(process_label)
    data = data.batch(32)

    result = model.predict(data)

    chemicals = []
    labels = []
    for x, y in zip(result, chemical):
        chemicals.append(y)
        labels.append(x[1])
    return pd.DataFrame(data={"Chemical": chemicals, "Label": labels})
