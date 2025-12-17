from transformers import TrOCRProcessor, VisionEncoderDecoderModel

# Pretrained model name
model_name = "microsoft/trocr-large-printed"

# Load processor and model from Hugging Face Hub
processor = TrOCRProcessor.from_pretrained(model_name, use_fast=False)
model = VisionEncoderDecoderModel.from_pretrained(model_name)

# Save locally to models folder
processor.save_pretrained("models/trocr-large-printed")
model.save_pretrained("models/trocr-large-printed")

print("TrOCR model and processor saved locally!")
