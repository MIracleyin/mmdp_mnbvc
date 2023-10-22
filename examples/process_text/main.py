from datetime import datetime
from time import time
from mmda.recipes import ProcessTextRecipe
from mmda.types import Document
from mmdp.utils import Simhash
import jsonlines
from pathlib import Path
import argparse
import hashlib
import pikepdf
from loguru import logger

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--log_dir",
        type=str,
        default="./logs",
        help="The directory containing the log files",
    )
    parser.add_argument(
        "--pdfs_dir",
        type=str,
        # default='/path/to/100kpdf',
        default='/Users/yin/projects/mnbvc/100kpdf',
        help="The directory containing the PDF files",
    )
    parser.add_argument(
        "--mnbvc_format",
        action='store_true',
        help="output json as mnbvc generate format",
    )

    parser.add_argument(
        "--jsonl_path",
        type=str,
        default='./parse.jsonl',
        help="The result file path",
    )
    return parser.parse_args()

def convert_to_generate(doc: Document, pdf_file: Path, threshold: 0.5):
    '''
    referecne: 
    '''
    # 定义json结构
    file_json = {'文件名': str(pdf_file.absolute()),
                 '是否待查文件': False,
                 '是否重复文件': False,
                 '文件大小': pdf_file.stat().st_size,
                 'simhash': 0,
                 '最长段落长度': 0,
                 '段落数': 0,
                 '去重段落数': 0,
                 '低质量段落数': 0,
                 '段落': []}
    
    # 定义用于去重的set
    hashs = set()

    texts = []
    for line_number, line in enumerate(doc.rows):
        # 计算最长段落长度
        file_json['最长段落长度'] = max(file_json['最长段落长度'], len(line.text))
        # 删除空行
        if len(line.text) == 0:
            continue
        # 计算每一行的md5值
        md5 = hashlib.md5(line.text.encode()).hexdigest()
        # 将每一行内容添加到 json 中
        file_json['段落'].append({'行号': line_number,
                                '是否重复': md5 in hashs,
                                '是否跨文件重复': False,
                                'md5': md5,
                                '内容': line.text
                                })
        if md5 not in hashs:
            texts.append(line.text)
    
        # 将md5值添加到set中，用于去重
        hashs.add(md5)
    
    if len(hashs) == 0:
        return None
    
    # 计算段落数和去重段落数
    file_json['段落数'] = len(file_json['段落'])
    file_json['去重段落数'] = len(hashs)
    # 计算simhash
    file_json['simhash'] = Simhash(texts).value
    # 判断是否是待查文件
    if (file_json['去重段落数'] / file_json['段落数']) < threshold:
        file_json['是否待查文件'] = True
    return file_json
        
def process(args):
    readable, faild = 0, 0
    pdfs_path = Path(args.pdfs_dir)
    jsonl_path = Path(args.jsonl_path)
    recipe = ProcessTextRecipe(svm_word_predictor_path="./svm_word_predictor.tar.gz") # for word merge
    with jsonlines.open(jsonl_path, 'w') as w:
        for pdf_file in pdfs_path.rglob("*.pdf"):
            try:
                t1 = time()
                pdf = pikepdf.Pdf.open(pdf_file)
                producer = pdf.docinfo.get("/Producer") # rules
                if "ProcessText Group" in str(producer): # rules
                    doc: Document = recipe.from_path(pdf_file)
                    if args.mnbvc_format:
                        doc_json = convert_to_generate(doc, pdf_file, threshold=0.5)
                    else:
                        doc_json = doc.to_json(with_images=True)
                    w.write(doc_json)
                else:
                    continue
                readable += 1
                logger.info(f"Parse {pdf_file} using {time() - t1}")

            except Exception as e:
                logger.error(f"Error while load PDF {pdf_file}: {e}")
                faild += 1
    
    return readable, faild

def main():
    args = parse_arguments()

    # 获取时间戳
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # 配置logger
    logger.remove(handler_id=None) # don't log in console
    logger.add(f"{args.log_dir}/pdf_convert_{timestamp}.log", rotation="500 MB") 
    
    r, f = process(args)
    logger.info(f"{args.pdf_dir}: all {r}, error {f}")

if __name__ == "__main__":
    main()