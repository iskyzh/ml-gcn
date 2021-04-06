import tensorflow as tf

from storage import run_dir
from train import train
from model import model
from predict import predict

model = model()
train(model)
