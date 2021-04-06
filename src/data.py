import pandas as pd
import numpy as np
import tensorflow as tf
from tqdm import tqdm
from storage import get_object
from pysmiles import read_smiles
import networkx as nx
import logging
logging.getLogger('pysmiles').setLevel(logging.CRITICAL)

tf.enable_eager_execution()


def load_smiles(path):
    smiles = pd.read_csv(get_object(f"{path}/names_smiles.txt"))
    return smiles


def load_labels(path, label_path):
    if label_path:
        labels = pd.read_csv(get_object(f"{path}/{label_path}"))
    else:
        labels = pd.read_csv(get_object(f"{path}/names_labels.txt"))
    return labels


def build_data(path, label_path):
    smiles = load_smiles(path)
    labels = load_labels(path, label_path)
    joint_data = smiles.merge(labels, on=['Chemical'])
    # joint_data['SMILES'].str.decode("utf-8")
    # print(joint_data)
    return joint_data


def to_numpy_array(frame):
    smiles = np.array(frame['SMILES'])
    labels = np.array(frame['Label']).astype(np.int8)
    return smiles, labels


def split_by_label(data, labels):
    result = [[], []]
    assert(len(data) == len(labels))
    for datum, label in zip(data, labels):
        result[label].append(datum)
    return result[0], result[1]


PASTE_SIZE = 132
ALL_ELEMS = ['Ag', 'Al', 'As', 'Au', 'B', 'Ba', 'Be', 'Bi', 'Br', 'C', 'Ca', 'Cd', 'Cl', 'Co', 'Cr', 'Cu', 'Dy', 'F', 'Fe', 'Ge', 'H', 'Hg', 'I', 'In',
             'K', 'Li', 'Mg', 'Mn', 'Mo', 'N', 'Na', 'Nd', 'Ni', 'O', 'P', 'Pb', 'Pd', 'Pt', 'S', 'Sb', 'Se', 'Si', 'Sn', 'Sr', 'Ti', 'Tl', 'V', 'Yb', 'Zn', 'Zr']
ELEMS_RANGE = len(ALL_ELEMS)
HCOUNT_RANGE = 6
CHARGE_RANGE = 6
ELEMENT_SELECTED = ELEMS_RANGE + HCOUNT_RANGE + CHARGE_RANGE


def normalize(mx):
    rowsum = np.array(mx.sum(1))
    r_inv = np.power(rowsum, -1).flatten()
    r_inv[np.isinf(r_inv)] = 0.
    r_mat_inv = np.diag(r_inv)
    mx = r_mat_inv.dot(mx)
    return mx


def preprocess_smiles_network(smile):
    # get adj matrix
    if not isinstance(smile, str):
        smile = smile.decode('utf-8')

    mol = read_smiles(smile)
    mat = nx.to_numpy_matrix(mol)
    mat = mat + np.multiply(mat.T, mat.T > mat) - np.multiply(mat, mat.T > mat)
    mat = normalize(mat + np.eye(mat.shape[0]))

    elements = np.array([vert for (idx, vert) in mol.nodes(data='element')])
    verts_1 = np.array([elements == e for e in ALL_ELEMS])

    hcounts = np.array([vert for (idx, vert) in mol.nodes(data='hcount')])
    verts_2 = np.array([hcounts == h for h in range(HCOUNT_RANGE)])

    charges = np.array([vert for (idx, vert) in mol.nodes(data='charge')])
    verts_3 = np.array([np.abs(charges) == c for c in range(CHARGE_RANGE)])

    mat_shape = mat.shape[0]
    mat_shape = min(mat_shape, PASTE_SIZE)

    final_mat = np.zeros((PASTE_SIZE, PASTE_SIZE))
    final_mat[:mat_shape, :mat_shape] = mat[:mat_shape, :mat_shape]

    final_verts = np.zeros((ELEMENT_SELECTED, PASTE_SIZE))
    final_verts[:ELEMS_RANGE, :mat_shape] = verts_1[:, :mat_shape]
    final_verts[ELEMS_RANGE:ELEMS_RANGE+HCOUNT_RANGE,
                :mat_shape] = verts_2[:, :mat_shape]
    final_verts[ELEMS_RANGE+HCOUNT_RANGE:,
                :mat_shape] = verts_3[:, :mat_shape]

    return final_verts.T, final_mat


def preprocess_label(label):
    if label == 0:
        return np.array([1, 0])
    if label == 1:
        return np.array([0, 1])
    raise ""


def to_tensor_slice(data):
    data = tf.data.Dataset.from_tensor_slices(data)
    return data


def process_smile(smile, label):
    feature, matrix = tf.numpy_function(preprocess_smiles_network, [
        smile], [np.double, np.double])
    feature.set_shape((PASTE_SIZE, ELEMENT_SELECTED))
    matrix.set_shape((PASTE_SIZE, PASTE_SIZE))
    return (feature, matrix), label


def process_label(_1, label):
    label = tf.numpy_function(preprocess_label, [label], np.int64)
    label.set_shape(2)
    return _1, label


def verify_dataset(dataset):
    sum = 0
    n = 0
    for _, label in dataset.take(233):
        for i in label.numpy():
            if i[1] == 1:
                sum += 1
            n += 1
    return sum / n


def build_data_from_dataset(set, batch, limit=0, oversample=True, label_path=None):
    data = build_data(set, label_path)
    if limit != 0:
        data = data[:limit]
    data = to_numpy_array(data)
    data = to_tensor_slice(data)
    data = data.map(process_smile)
    data = data.cache()
    data = data.shuffle(batch * 16)
    if oversample:
        pos = data.filter(lambda _1, x: tf.math.equal(x, 1)).repeat()
        neg = data.filter(lambda _1, x: tf.math.equal(x, 0)).repeat()
        pos = pos.map(process_label)
        neg = neg.map(process_label)
        data = tf.data.experimental.sample_from_datasets(
            [pos, neg], weights=[0.5, 0.5])
    else:
        data = data.map(process_label).repeat()
    data = data.batch(batch)
    data = data.prefetch(tf.data.experimental.AUTOTUNE)
    return data


if __name__ == '__main__':
    data = build_data_from_dataset('validation', 32)
    result = list(data.take(1))[0]
    print(result[0].shape)
    print(result[1].shape)
    # data = build_data('train')
    # x = []
    # max_size = 0
    # for smile in data['SMILES']:
    #     mol = read_smiles(smile)
    #     mat = nx.to_numpy_matrix(mol)
    #     max_size = max(max_size, mat.shape[0])
    #     x.append(np.array([vert for (idx, vert) in mol.nodes(data='element')]))
    # print(np.unique(np.concatenate(x)))
    # print(max_size)
