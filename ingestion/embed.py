from sentence_transformers import SentenceTransformer

# Single unified embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_text(texts):
    return model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True
    ).tolist()