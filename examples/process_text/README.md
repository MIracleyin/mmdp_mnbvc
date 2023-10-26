## pure pdf convert

## 更新
使用 mmda 某个分支，防止依赖污染环境

## Setup
```shell

conda create -n mmdp python=3.8
conda activate mmdp

git clone https://github.com/MIracleyin/mmda_mnbvc.git
cd mmda_mnbvc
git switch process_text
pip install -e '.[dev,svm_word_predictor]'

git clone https://github.com/MIracleyin/mmdp_mnbvc.git
cd mmdp_mnbvc
pip install .
```

将 PDF 转化为 mnbvc generate json format

python examples/process_text/main.py --pdfs_dir /path/to/pdfs_dir --jsonl_path /path/to/parse.jsonl --mnbvc_format