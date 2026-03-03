import fitz
import os
import uuid

def extract_pdf(pdf_path, image_dir="data/images"):
    os.makedirs(image_dir, exist_ok=True)

    doc = fitz.open(pdf_path)

    text_chunks = []
    image_data = []

    for page_num, page in enumerate(doc):
        text = page.get_text().strip()

        if text:
            text_chunks.append({
            "id": str(uuid.uuid4()),
            "content": text,
            "page": page_num
        })

        images = page.get_images(full=True)

        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]

            image_filename = f"page{page_num}_img{img_index}.png"
            image_path = os.path.join(image_dir, image_filename)

            with open(image_path, "wb") as f:
                f.write(image_bytes)

            image_data.append({
                "id": str(uuid.uuid4()),
                "path": image_path,
                "page": page_num
            })

    return text_chunks, image_data