import json
import argparse

def load_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_json_file(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)

def extract_size_info(tokens):
    size_dict = {}
    for token in tokens:
        if len(token["spans"]) == 1 and "size" in token["metadata"]:
            span = token['spans'][0]
            size_dict[span["start"]] = [
                token["metadata"]["size"],
                span['box']["left"],
                span['box']["top"],
                span['box']["width"],
                span['box']["height"]
            ]
    return size_dict

def create_paragraph(start, end, box, page, content, paragraph_id):
    return {
        'spans': [{'start': start, 'end': end, 'box': box}],
        'id': paragraph_id,
        'metadata': content
    }

def process_rows(rows, symbols, size_dict):
    paragraphs = []
    content = ""
    last_size = 0
    last_pos = 0
    paragraph_id = 0

    for row in rows:
        if len(row["spans"]) == 1:
            span = row['spans'][0]
            start, end = span["start"], span["end"]
            metadata_size = size_dict[start][0]
            current_pos = span['box']["top"] + span['box']["height"]

            if not content:
                start_point, box, page = start, span['box'], span['box']["page"]
                last_size, last_pos = metadata_size, current_pos

            if (int(metadata_size) - int(last_size) > 2) or (round(span['box']["top"], 2) - round(last_pos, 2) > 0.02):
                paragraphs.append(create_paragraph(start_point, end, box, page, content, paragraph_id))
                content, paragraph_id = "", paragraph_id + 1
                start_point, box, page = end, span['box'], span['box']["page"]
                last_size, last_pos = metadata_size, current_pos

            if round(span['box']["top"], 2) - round(last_pos, 2) <= 0.02:
                last_pos = current_pos

            content += symbols[start:end]

            if round(span['box']["width"], 2) < 0.5:
                paragraphs.append(create_paragraph(start_point, end, box, page, content, paragraph_id))
                content, paragraph_id = "", paragraph_id + 1
                start_point, box, page = end, span['box'], span['box']["page"]
                last_size, last_pos = metadata_size, current_pos

    return paragraphs

def insert_paragraph(source_path, output_path):
    data = load_json_file(source_path)
    tokens, symbols, rows = data["tokens"], data["symbols"], data["rows"]
    size_dict = extract_size_info(tokens)
    data["paragraph"] = process_rows(rows, symbols, size_dict)
    save_json_file(data, output_path)

def main():
    parser = argparse.ArgumentParser(description='Insert paragraphs into JSON.')
    parser.add_argument('--source', required=True, help='Input file path.')
    parser.add_argument('--output', required=True, help='Output file path.')
    args = parser.parse_args()
    insert_paragraph(args.source, args.output)

if __name__ == '__main__':
    main()
