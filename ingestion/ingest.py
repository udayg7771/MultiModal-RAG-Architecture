from ingestion.extract import extract_pdf
from ingestion.embed import embed_text
from ingestion.analyze import enrich_image
from pinecone_store import get_index
from utils.doc_utils import generate_doc_id  # ✅ use shared utility


def ingest(pdf_path):
    index = get_index()

    # 🔥 Generate deterministic document ID
    doc_id = generate_doc_id(pdf_path)

    text_chunks, images = extract_pdf(pdf_path)
    vectors = []

    print(f"Generated doc_id: {doc_id}")
    print("Embedding text...")

    for chunk in text_chunks:
        embedding = embed_text([chunk["content"]])[0]

        vectors.append({
            "id": chunk["id"],
            "values": embedding,
            "metadata": {
                "type": "text",
                "content": chunk["content"],
                "page": chunk["page"],
                "doc_id": doc_id
            }
        })

    print("Embedding images...")

    for image in images:
        enriched_text = enrich_image(image["path"])
        embedding = embed_text([enriched_text])[0]

        vectors.append({
            "id": image["id"],
            "values": embedding,
            "metadata": {
                "type": "image",
                "path": image["path"],
                "caption": enriched_text,  # ✅ required for Gemini grounding
                "page": image["page"],
                "doc_id": doc_id
            }
        })

    print("Upserting to Pinecone...")
    index.upsert(vectors=vectors)

    print("Ingestion complete with SHA-256 doc_id filtering.")


if __name__ == "__main__":
    ingest("data/sample.pdf")