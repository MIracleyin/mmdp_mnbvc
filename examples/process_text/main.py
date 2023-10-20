from time import time
from mmda.recipes import ProcessTextRecipe
import jsonlines
from pathlib import Path
import argparse

import pikepdf

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--pdfs_dir",
        type=str,
        default='./data',
        help="The directory containing the PDF files",
    )
    parser.add_argument(
        "--jsonl_path",
        type=str,
        default='./output/pdf_meta_info.jsonl',
        help="The result file path",
    )
    return parser.parse_args()

def main():
    args = parse_arguments()
    pdfs_path = Path(args.pdfs_dir)
    jsonl_path = Path(args.jsonl_path)
    readable, faild = 0, 0
    recipe = ProcessTextRecipe(svm_word_predictor_path="./svm_word_predictor.tar.gz")
    with jsonlines.open(jsonl_path, 'w') as w:
        for pdf_file in pdfs_path.rglob("*.pdf"):
            try:
                t1 = time()
                pdf = pikepdf.Pdf.open(pdf_file)
                producer = pdf.docinfo.get("/Producer")
                if "ProcessText Group" in str(producer):
                    doc = recipe.from_path(pdf_file)
                    doc_json = doc.to_json()
                    w.write(doc_json)
                    print(pdf_file)
                else:
                    continue
                readable += 1
                print(f"parse time{time() - t1}")

            except Exception as e:
                # logger.error(f"Error while load PDF {pdf_file}: {e}")
                faild += 1

if __name__ == "__main__":
    main()