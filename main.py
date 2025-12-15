from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

image = Image.open("./train/image9.png").convert("RGB")

processor = TrOCRProcessor.from_pretrained(
    "microsoft/trocr-large-printed",
    use_fast=False
)

model = VisionEncoderDecoderModel.from_pretrained(
    "microsoft/trocr-large-printed"
).to(device)

pixel_values = processor(images=image, return_tensors="pt").pixel_values.to(device)

with torch.no_grad():
    generated_ids = model.generate(pixel_values)

generated_text = processor.batch_decode(
    generated_ids, skip_special_tokens=True
)[0]

print(generated_text)
