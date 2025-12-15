from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
import torch

<<<<<<< HEAD
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

image = Image.open("./train/image9.png").convert("RGB")

=======
imageLink = "./train/image9.png"
image = Image.open(imageLink).convert("RGB")
# processor = TrOCRProcessor.from_pretrained("microsoft/trocr-large-printed")
>>>>>>> 6a69855 (Update files on TrOCR-test-training/main)
processor = TrOCRProcessor.from_pretrained(
    "microsoft/trocr-large-printed",
    use_fast=False
)

<<<<<<< HEAD
model = VisionEncoderDecoderModel.from_pretrained(
    "microsoft/trocr-large-printed"
).to(device)

pixel_values = processor(images=image, return_tensors="pt").pixel_values.to(device)
=======
model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-large-printed")
pixel_values = processor(images=image, return_tensors="pt").pixel_values
>>>>>>> 6a69855 (Update files on TrOCR-test-training/main)

with torch.no_grad():
    generated_ids = model.generate(pixel_values)

<<<<<<< HEAD
generated_text = processor.batch_decode(
    generated_ids, skip_special_tokens=True
)[0]

print(generated_text)
=======
generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
print(generated_text)

>>>>>>> 6a69855 (Update files on TrOCR-test-training/main)
