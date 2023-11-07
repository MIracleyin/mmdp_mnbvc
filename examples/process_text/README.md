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

## Usecase

使用 examples/process_text/grep_ProcessText.py 抓取符合规则的 pdf 文件名

```python
python examples/process_text/grep_ProcessText.py --pdfs_dir '/Path/to/pdf' > process_pdf_list
```

使用 examples/process_text/process_ProcessText.py 解析符合规则的 pdf 文件名

```python
python examples/process_text/process_ProcessText.py --pdfs_list '/Path/to/pdf_list' 

--mnbvc_format # 以 mnbvc 通用文本格式输出到 jsonl 中
```