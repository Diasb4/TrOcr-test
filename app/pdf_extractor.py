
import re
from pathlib import Path
import easyocr
from pdf2image import convert_from_path
import os


# Normalization

def normalize(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-zа-я0-9 ]", "", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


# PDF -> images

def pdf_to_images(pdf_path: str, out_dir="pages", dpi=220):
    os.makedirs(out_dir, exist_ok=True)
    pages = convert_from_path(pdf_path, dpi=dpi)
    png_files = []

    for i, page in enumerate(pages):
        png_path = Path(out_dir) / f"page_{i + 1}.png"
        page.save(png_path, "PNG")
        png_files.append(png_path)

    return png_files


# Extract target page and text below phrase

def extract_target_page(pdf_path: str, phrase: str, out_dir="pages", dpi=220):
    phrase_norm = normalize(phrase)
    reader = easyocr.Reader(["en"])
    png_files = pdf_to_images(pdf_path, out_dir, dpi)

    results = []

    for png_file in png_files:
        # Get OCR as a single string
        text_chunks = reader.readtext(str(png_file), detail=0, paragraph=True)
        full_text = " ".join([normalize(t) for t in text_chunks if t.strip()])

        # Split text at the first occurrence of the phrase
        parts = full_text.split(phrase_norm, 1)
        if len(parts) > 1:
            text_below_phrase = parts[1].strip()
        else:
            text_below_phrase = ""  # phrase not found

        results.append({
            "page": str(png_file),
            # "full_text": full_text,
            "text_below_phrase": text_below_phrase
        })

    return results
