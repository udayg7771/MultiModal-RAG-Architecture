import os
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

pc.create_index(
    name="enterprise-mm-rag",
    dimension=384,   # IMPORTANT: MiniLM = 384
    metric="cosine",
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"   # change if your region is different
    )
)

print("Index created successfully.")