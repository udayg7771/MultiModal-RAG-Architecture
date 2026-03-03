from ingestion.embed import embed_text
from pinecone_store import get_index


def retrieve(query, doc_id, top_k=6):
    index = get_index()

    query_embedding = embed_text([query])[0]

    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
        filter={
            "doc_id": {"$eq": doc_id}  # ✅ document-level filtering
        }
    )

    text_results = []
    image_results = []

    for match in results["matches"]:
        metadata = match["metadata"]
        score = match["score"]

        if metadata["type"] == "text":
            text_results.append((score, metadata["content"]))

        elif metadata["type"] == "image":
            image_results.append((score, {
                "path": metadata["path"],
                "caption": metadata.get("caption", "")
            }))

    # Sort by score
    text_results.sort(reverse=True, key=lambda x: x[0])
    image_results.sort(reverse=True, key=lambda x: x[0])

    # Determine dominant modality
    top_text_score = text_results[0][0] if text_results else 0
    top_image_score = image_results[0][0] if image_results else 0

    texts = []
    images = []

    if top_text_score > top_image_score + 0.15:
        # Text-dominant query
        texts = [text_results[0][1]]
    elif top_image_score > top_text_score:
        # Image-dominant query
        images = [image_results[0][1]]
    else:
        # Multimodal
        texts = [t[1] for t in text_results[:2]]
        images = [i[1] for i in image_results[:1]]

    return texts, images