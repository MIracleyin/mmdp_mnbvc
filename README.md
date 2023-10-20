# mutilmodal doc processing
多模态文档处理

## Setup
```shell
conda create -n mmdp python=3.8
conda activate mmdp

cd mnbvc_mmda
pip install .

git clone https://github.com/MIracleyin/mmdp_mnbvc.git
cd mnbvc_mmdp
pip install .
```

## 流程

python examples/process_text/main.py --pdfs_dir /path/to/pdfs_dir --jsonl_path /path/to/parse.jsonl



