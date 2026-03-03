# ingestion/analyze.py

from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import pytesseract
import torch

# Load once globally
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def generate_caption(image_path):
    image = Image.open(image_path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt")

    with torch.no_grad():
        out = model.generate(
            **inputs,
            max_new_tokens=40
        )

    caption = processor.decode(out[0], skip_special_tokens=True)
    return caption


def extract_ocr(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text.strip()


def enrich_image(image_path):
    caption = generate_caption(image_path)
    ocr_text = extract_ocr(image_path)

    enriched = caption
    if ocr_text:
        enriched += " " + ocr_text

    return enriched