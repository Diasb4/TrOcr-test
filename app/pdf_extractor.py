# import os
# import re
# import json
# from pdf2image import convert_from_path
# import easyocr
# from pathlib import Path

# # -----------------------------
# # Normalization
# # -----------------------------
# def normalize(s: str) -> str:
#     s = s.lower()
#     s = re.sub(r"[^a-zа-я0-9 ]", "", s)
#     s = re.sub(r"\s+", " ", s)
#     return s.strip()

# # -----------------------------
# # Rolling Hash (Rabin-Karp)
# # -----------------------------
# def rolling_hash(text: str, pattern: str) -> bool:
#     base = 257
#     mod = 10**9 + 7

#     n = len(text)
#     m = len(pattern)

#     if m > n:
#         return False

#     ph = 0
#     th = 0
#     power = 1

#     for i in range(m):
#         ph = (ph * base + ord(pattern[i])) % mod
#         th = (th * base + ord(text[i])) % mod
#         if i < m - 1:
#             power = (power * base) % mod

#     for i in range(n - m + 1):
#         if ph == th:
#             if text[i:i + m] == pattern:
#                 return True

#         if i < n - m:
#             th = (th - ord(text[i]) * power) % mod
#             th = (th * base + ord(text[i + m])) % mod
#             th = (th + mod) % mod

#     return False

# # -----------------------------
# # PDF -> images
# # -----------------------------
# def pdf_to_images(pdf_path: str, out_dir="pages", dpi=220):
#     os.makedirs(out_dir, exist_ok=True)
#     pages = convert_from_path(pdf_path, dpi=dpi)
#     png_files = []

#     for i, page in enumerate(pages):
#         png_path = Path(out_dir) / f"page_{i + 1}.png"
#         page.save(png_path, "PNG")
#         png_files.append(png_path)

#     return png_files

# # -----------------------------
# # Extract target page and text below phrase
# # -----------------------------
# def extract_target_page(pdf_path: str, phrase: str, out_dir="pages", dpi=220):
#     phrase_norm = normalize(phrase)
#     reader = easyocr.Reader(["ru", "en"])  # lazy load could be done outside if needed
#     png_files = pdf_to_images(pdf_path, out_dir, dpi)

#     for png_file in png_files:
#         text_chunks = reader.readtext(str(png_file), detail=0, paragraph=True)
#         lines = [normalize(l) for l in text_chunks if l.strip()]

#         for idx, line in enumerate(lines):
#             if rolling_hash(line, phrase_norm):
#                 # Return page path and lines below the heading
#                 return str(png_file), lines[idx + 1 :]

#     # Phrase not found: return all text
#     all_text = []
#     for png_file in png_files:
#         text_chunks = reader.readtext(str(png_file), detail=0, paragraph=True)
#         all_text.extend([normalize(l) for l in text_chunks if l.strip()])

#     return "All text extracted", all_text

# # -----------------------------
# # Helper functions for floats/ints if needed
# # -----------------------------
# def extract_floats(lines):
#     floats = []
#     pattern = re.compile(r"\d+\.\d+|\.\d+|\d+,\d+")
#     for line in lines:
#         matches = pattern.findall(line)
#         for m in matches:
#             m = m.replace(",", ".")
#             try:
#                 floats.append(float(m))
#             except:
#                 pass
#     return floats

# def extract_ints(lines):
#     ints = []
#     pattern = re.compile(r"\b\d+\b")
#     for line in lines:
#         matches = pattern.findall(line)
#         for m in matches:
#             try:
#                 ints.append(int(m))
#             except:
#                 pass
#     return ints

# # -----------------------------
# # Full OCR of a page
# # -----------------------------
# def full_ocr(png_path: str):
#     reader = easyocr.Reader(["ru", "en"])
#     return reader.readtext(str(png_path), detail=1, paragraph=True)



import os
import re
from pathlib import Path
from pdf2image import convert_from_path
import easyocr

# -----------------------------
# Normalization
# -----------------------------
def normalize(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-zа-я0-9 ]", "", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()

# -----------------------------
# Rolling Hash (Rabin-Karp)
# -----------------------------
def rolling_hash(text: str, pattern: str) -> bool:
    base = 257
    mod = 10**9 + 7
    n, m = len(text), len(pattern)

    if m > n:
        return False

    ph = th = 0
    power = 1
    for i in range(m):
        ph = (ph * base + ord(pattern[i])) % mod
        th = (th * base + ord(text[i])) % mod
        if i < m - 1:
            power = (power * base) % mod

    for i in range(n - m + 1):
        if ph == th and text[i:i + m] == pattern:
            return True
        if i < n - m:
            th = (th - ord(text[i]) * power) % mod
            th = (th * base + ord(text[i + m])) % mod
            th = (th + mod) % mod
    return False

# -----------------------------
# PDF -> images
# -----------------------------
def pdf_to_images(pdf_path: str, out_dir="pages", dpi=220):
    os.makedirs(out_dir, exist_ok=True)
    pages = convert_from_path(pdf_path, dpi=dpi)
    png_files = []

    for i, page in enumerate(pages):
        png_path = Path(out_dir) / f"page_{i + 1}.png"
        page.save(png_path, "PNG")
        png_files.append(png_path)

    return png_files

# -----------------------------
# Extract pages and text below phrase
# -----------------------------
def extract_target_page(pdf_path: str, phrase: str, out_dir="pages", dpi=220):
    phrase_norm = normalize(phrase)
    reader = easyocr.Reader(["en"])
    png_files = pdf_to_images(pdf_path, out_dir, dpi)

    results = []

    for png_file in png_files:
        text_chunks = reader.readtext(str(png_file), detail=0, paragraph=True)
        lines = [normalize(l) for l in text_chunks if l.strip()]
        text_below_phrase = []

        for idx, line in enumerate(lines):
            if rolling_hash(line, phrase_norm):
                text_below_phrase = lines[idx + 1 :]
                break

        results.append({
            "page": str(png_file),
            "full_text": lines,
            "text_below_phrase": text_below_phrase
        })

    return results
