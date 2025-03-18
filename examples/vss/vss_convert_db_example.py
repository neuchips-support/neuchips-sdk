import argparse
import neuvss as vss
import numpy as np
import os
import torch
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
from typing import Any, List
from unstructured.partition.pdf import partition_pdf

RAW_TEXT_CACHE_FILE = "raw_text.pt"
CORPUS_EMB_CACHE_FILE = "corpus_emb.pt"
VSS_DB_CACHE_FILE = "vss_db.bin"
WEIGHT_SCALE = 0.0374

def extract_raw_text(raw_elements: List[Any]) -> List[Any]:
    text_elements = []
    table_elements = []
    for element in raw_elements:
        if "unstructured.documents.elements.Table" in str(type(element)):
            table_elements.append(str(element))
        elif "unstructured.documents.elements.CompositeElement" in str(type(element)):
            text_elements.append(str(element))
    return text_elements + table_elements

def convert_pdf_to_db_bin(pdf_file, cache_dir):
    if not os.path.isfile(pdf_file):
        raise RuntimeError(f"The pdf file {pdf_file} does not exist.")

    raw_elements = partition_pdf(
        filename=pdf_file,
        extract_images_in_pdf=False,
        infer_table_structure=True,
        chunking_strategy="by_title",
        max_characters=400,
        new_after_n_chars=380,
        combine_text_under_n_chars=200)
    raw_text = extract_raw_text(raw_elements)

    emb_model = SentenceTransformer("WhereIsAI/UAE-Large-V1")
    encoded_raw_text = emb_model.encode(raw_text, convert_to_tensor=True)
    corpus_emb = torch.clamp(torch.round(encoded_raw_text / WEIGHT_SCALE), -127, 127).to(torch.int8)

    db_row_size = corpus_emb.shape[1]

    os.makedirs(cache_dir, exist_ok=True)
    torch.save(raw_text, os.path.join(cache_dir, RAW_TEXT_CACHE_FILE))
    torch.save(corpus_emb, os.path.join(cache_dir, CORPUS_EMB_CACHE_FILE))
    corpus_emb.numpy().tofile(os.path.join(cache_dir, VSS_DB_CACHE_FILE))

    return db_row_size

def convert_db_bin_to_weight_bin(db_bin_file, db_row_size, weight_dir):
    if not vss.PyNeuVssCalculator.convert_db(db_row_size, db_bin_file, weight_dir):
        raise RuntimeError(f"Failed to convert VSS db to weight files.")

def main():
    parser = argparse.ArgumentParser(description="An example for converting a pdf file to db cache and VSS weights.")
    parser.add_argument("--pdf_file", type=str, required=True, help="A pdf file that is the db source.")
    parser.add_argument("--cache_dir", type=str, required=True, help="The directory of db cache files.")
    parser.add_argument("--weight_dir", type=str, required=True, help="The directory of VSS weight files.")
    args = parser.parse_args()

    db_row_size = convert_pdf_to_db_bin(args.pdf_file, args.cache_dir)
    db_bin_file = os.path.join(args.cache_dir, VSS_DB_CACHE_FILE)
    convert_db_bin_to_weight_bin(db_bin_file, db_row_size, args.weight_dir)

    print(f"Convert pdf {args.pdf_file} to the VSS weight files in dir {args.weight_dir} OK.\n")

if __name__ == '__main__':
    main()
