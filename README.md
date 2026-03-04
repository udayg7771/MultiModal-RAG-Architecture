# Enterprise Multimodal RAG System

An enterprise-style **Multimodal Retrieval-Augmented Generation (RAG)** system that enables semantic querying across **text and image-based documents**.

The system ingests PDF documents, extracts textual and visual content, embeds them into a shared semantic space, and retrieves the most relevant multimodal context using **vector similarity search**. Retrieved context is then passed to a **large language model (LLM)** for grounded reasoning and response generation.

This architecture demonstrates how modern **GenAI-powered document intelligence systems** are built using vector databases, embedding models, multimodal processing pipelines, and LLM orchestration.

---

# Project Overview

Traditional search systems rely on keyword matching and fail to understand semantic meaning.  
Retrieval-Augmented Generation (RAG) solves this by combining:

- **Vector embeddings**
- **Semantic similarity search**
- **Large Language Models**

This project extends RAG into a **multimodal pipeline**, enabling reasoning over both **text and images extracted from documents**.

The system:

1. Parses PDF documents
2. Extracts text and images
3. Generates captions for images using vision-language models
4. Embeds all information into vector representations
5. Stores vectors in Pinecone
6. Retrieves relevant context using cosine similarity
7. Feeds retrieved context into Gemini for grounded answers

---

The architecture separates the pipeline into **three core stages**:

### 1. Ingestion Layer
Responsible for parsing documents and generating structured information.

Tasks performed:
- PDF parsing
- Image extraction
- Caption generation
- OCR enrichment
- Content chunking

### 2. Vector Indexing Layer
Responsible for converting content into embeddings and storing them.

Tasks performed:
- Embedding generation
- Vector indexing
- Metadata storage
- Document-level isolation using SHA-256 hashing

### 3. Retrieval + Reasoning Layer
Responsible for answering user queries.

Tasks performed:
- Query embedding
- Cosine similarity search
- Context assembly
- Multimodal reasoning using Gemini

---

# Tech Stack

| Technology | Purpose |
|-----------|--------|
| **Python** | Core system implementation |
| **Streamlit** | Interactive UI for document querying |
| **Pinecone (vector database)** | Stores and retrieves semantic embeddings |
| **Sentence Transformers (MiniLM)** | Generates 384-dimensional semantic embeddings |
| **Transformers + Torch** | Runs BLIP model for image caption generation |
| **PyMuPDF** | Parses PDF documents and extracts images |
| **Pytesseract** | Extracts text embedded inside images |
| **Pillow** | Image preprocessing for captioning and LLM input |
| **Google Gemini** | Multimodal reasoning and response generation |

---

# Key Features

### Multimodal RAG
Supports semantic reasoning across **both text and images**.

### Cross-Modal Embedding Alignment
Image captions and OCR text are embedded into the same vector space as document text.

### Deterministic Document Isolation
Documents are assigned **SHA-256 hashes** to prevent cross-document retrieval contamination.

### Semantic Vector Search
Retrieval is performed using **cosine similarity over vector embeddings** stored in Pinecone.

### Query-Type Aware Retrieval
Queries are classified into:
- Textual
- Numeric
- Visual

The system prioritizes the most relevant modality during retrieval.

### Grounded LLM Responses
Only retrieved document context is sent to Gemini to prevent hallucination.

---

# Installation

1. Clone the repository
2. Install dependencies
3. Create a .env file in the root directory.
   ```bash
   PINECONE_API_KEY=your_pinecone_key
   GEMINI_API_KEY=your_gemini_key
5. Create your own Pinecone index (first time only)
6. Run the Streamlit interface

