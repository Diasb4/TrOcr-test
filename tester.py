from pdf_extractor import extract_target_page

pdf_file = "storage/uploads/sample2.pdf"
phrase = "Sharing"

png_file, lines = extract_target_page(pdf_file, phrase)
print("Matched page:", png_file)
print("Lines after phrase:")
for line in lines:
    print(line)
