import tensorflow as tf
import numpy as np
from data import build_data_from_dataset
from model import build_model
import os
import math
from storage import run_dir

CHECKPOINT_PATH = run_dir() / "checkpoints"
CHECKPOINT_PATH.mkdir(parents=True, exist_ok=True)

CHECKPOINT_PATH = str(CHECKPOINT_PATH) + "/{epoch:02d}-{val_auc:.6f}.h5"
TB_PATH = str(run_dir() / "tensorboard")


def train(model):
    BATCH_SIZE = 64
    TRAIN_SIZE = 1000  # 8171
    train_dataset = build_data_from_dataset('train', BATCH_SIZE)
    test_dataset = build_data_from_dataset('validation', BATCH_SIZE)

    resampled_steps_per_epoch = math.ceil(8171 / BATCH_SIZE)

    resampled_test_steps_per_epoch = math.ceil(273 / BATCH_SIZE * 9)

    early_stopping = tf.keras.callbacks.EarlyStopping(
        monitor='val_acc',
        verbose=1,
        patience=10,
        mode='max')

    cp_callback = tf.keras.callbacks.ModelCheckpoint(
        monitor='val_acc',
        filepath=CHECKPOINT_PATH,
        mode='max',
        # save_best_only=True,
        save_weights_only=True,
        verbose=1)

    csv_callback = tf.keras.callbacks.CSVLogger(
        str(run_dir() / "train.log"), append=True)

    # tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=TB_PATH)

    model.fit(train_dataset,
              epochs=300,
              steps_per_epoch=resampled_steps_per_epoch,
              callbacks=[cp_callback, early_stopping, csv_callback],
              validation_steps=resampled_test_steps_per_epoch,
              validation_data=test_dataset)


def get_model_summary(model):
    summary_str = []
    model.summary(print_fn=lambda x: summary_str.append(x))
    return "\n".join(summary_str)


if __name__ == '__main__':
    model = build_model()
    (run_dir() / "DATA_MODEL_SUMMARY").write_text(get_model_summary(model))
    print(model.summary())
    train(model)
