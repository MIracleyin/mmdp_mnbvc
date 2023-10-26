# mutilmodal doc processing
该项目为 MNBVC 计划的一部分，旨在提供一个复杂 PDF 规则解析，调用特定 PDF 解析规则的工具。该工具核心抽象了一系列 rules 作为各类不同 PDF 分类方案，并后处理解析数据为需要的格式。

## Setup
```shell

conda create -n mmdp python=3.8
conda activate mmdp

git clone https://github.com/MIracleyin/mmda_mnbvc.git
cd mmda_mnbvc
git switch to_some_branch
pip install -e '.[dev,some_dependencies]'

git clone https://github.com/MIracleyin/mmdp_mnbvc.git
cd mmdp_mnbvc
pip install .

```

## 流程




