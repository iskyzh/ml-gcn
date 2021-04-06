from predict import predict
from model import build_model
from train import train
from storage import run_dir
import tensorflow as tf
tf.enable_eager_execution()


CHECKPOINT_PATH = run_dir() / "checkpoints"

p = CHECKPOINT_PATH.glob('**/*')
files = [str(x) for x in p if x.is_file()]
files = sorted(files, key=lambda x: float(x.split('-')[-1][:-3]))

RUN_ID = (run_dir() / "DATA_RUNID").read_text().strip()

for idx, model_path in enumerate(reversed(files)):
    if idx >= 3:
        break
    auc = float(model_path.split('-')[-1][:-3])
    epoch = int(model_path.split('-')[-2].split('/')[-1])
    path = f"result-{RUN_ID}-{epoch}.csv"

    print("using model %s, AUC=%.6f, epoch=%d, save to %s" %
          (model_path, auc, epoch, path))

    model = build_model()
    model.load_weights(model_path)
    result = predict(model)
    result.to_csv(run_dir() / path, index=False)
