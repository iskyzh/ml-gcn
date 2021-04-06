import pytest
from data import *
import tensorflow as tf
tf.enable_eager_execution()


# def test_load_train():
#     _, train_data = load_onehots("train")
#     _, train_labels = load_labels("train")

#     ds, _, _ = build_train_data(train_data, train_labels)

#     train_labels = transform_labels(train_labels)

#     prob = verify_dataset(ds)

#     assert 0.4 <= prob <= 0.6

#     assert len(list(ds.take(3000))) == 3000

# def test_load_test():
#     _, test_data = load_onehots("validation")
#     _, test_labels = load_labels("validation")

#     ds, _, _ = build_test_data(test_data, test_labels)

#     test_labels = transform_labels(test_labels)

#     prob = verify_dataset(ds)

#     assert 0.4 <= prob <= 0.6


def test_smiles_process():
    test_smile = "CNC1=C2N=CN([C@@H]3O[C@H](CO)C(O)[C@H]3O)C2=NC=N1"
    vert, mat = preprocess_smiles_network(test_smile)
    print(vert, mat)
    assert vert.shape == (PASTE_SIZE, ELEMENT_SELECTED)
    assert mat.shape == (PASTE_SIZE, PASTE_SIZE)
