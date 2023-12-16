from datetime import datetime
from time import time
import jsonlines
from pathlib import Path
import argparse
import hashlib
import pikepdf
import fitz as mupdf
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
        default="100kpdf",
        help="The directory containing the pdf files",
    )
    return parser.parse_args()

def grep(args):
    readable, faild = 0, 0
    pdfs_path = Path(args.pdfs_dir)
    for pdf_path in pdfs_path.rglob("*.pdf"):
        try:
            pdf = mupdf.open(pdf_path)
            producer = pdf.metadata.get("producer")
            # pdf = pikepdf.Pdf.open(pdf_path)
            # producer = pdf.docinfo.get("/Producer")
            img_count = 0
            for page in pdf:
                img_count += len(page.get_images())

            if "ProcessText Group" in str(producer) and img_count == 0:
                print(pdf_path) # todo: better way?
            else:
                continue
            readable += 1
        except Exception as e:
            logger.error(f"Error while load PDF {pdf_path}: {e}")
            faild += 1
        
    return readable, faild



def main():
    args = parse_arguments()

    # 获取时间戳
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # 配置logger
    logger.remove(handler_id=None) # don't log in console
    logger.add(f"{args.log_dir}/pdf_grep_{timestamp}.log", rotation="500 MB") 
    
    r, f = grep(args)
    logger.info(f"{args.pdfs_dir}: all {r}, error {f}")

if __name__ == "__main__":
    main()