import os
from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv()

def get_index():
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    return pc.Index("enterprise-mm-rag")