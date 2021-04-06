# Machine Learning Course Project

## Introduction

通过 GCN 对 SMILES 表示的化学分子毒性进行预测。更多信息请参见[课程 Kaggle](https://www.kaggle.com/c/cs410-2020-fall-ai-project-1/)。

本项目通过一套 Cloud ML Infra 管理上百个机器学习模型，实现了 "implement once, run anywhere"。
仓库里包含了整个 infra 的相关脚本和代码。

`report.pdf` 是本项目的实验报告。

## Getting Started

在使用这套工具前，你需要安装必要的工具。

```bash
brew install minio/stable/mc
conda install tqdm tensorflow-gpu=1.15 keras=2.2.4 numpy pandas
pip install minio
```

## Run an Experiment

在项目根目录下，使用 `run.sh` 执行指令。

```bash
./run.sh python ./src/train.py
```

如果程序出错，数据不会被上传到对象存储。你可以手动上传。

```bash
./save.sh
```

可以通过 `list.sh` 列出所有实验。

```bash
./list.sh
```

可以通过 `recover.sh` 将某一次实验恢复到本地。

```bash
./recover.sh 20201111_221731_alexchi_31db906-dirty
```

可以使用 `clean.sh` 将缓存的实验数据清除。

```bash
./clean.sh
```

在实验过程中可能生成大量的数据。使用样例程序，仅 30 轮训练就能产生 1GB 数据。可以考虑：
* 每 10 轮 checkpoint 一次。
* 仅仅 checkpoint 最后一轮
* ...

## File Management

在预处理、训练过程中的所有文件都存放在交大对象储存上。你可以安装 minio 来查看对象云上的数据。
在项目目录中，也有对 minio API 的封装。

训练的结果和 log 应当全部存放在 `run_dir()` 函数返回的位置中。

请注意，下面的语句中含有 key 等隐私数据。请不要上传到各种公开平台上。

```bash
mc alias set sjtu-skyzh https://s3.jcloud.sjtu.edu.cn:443 [ACCESS KEY REDACTED] [SECRET KEY REDACTED]
mc ls sjtu-skyzh
```

对象存储的 `[BUCKET NAME REDACTED]/` bucket 存放本次训练过程中的所有文件。
