import streamlit as st
import os

from retrieval.orchestrator import orchestrate
from llm.gemini_engine import generate_answer
from ingestion.ingest import ingest
from utils.doc_utils import generate_doc_id
from utils.file_tracker import has_file_changed, update_file_hash


PDF_PATH = "data/sample.pdf"

st.set_page_config(page_title="Enterprise Multimodal RAG", layout="wide")

st.title("🧠 Enterprise Multimodal RAG")
st.markdown("---")


# ---------- FILE UPLOAD ----------
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file:
    os.makedirs("data", exist_ok=True)

    with open(PDF_PATH, "wb") as f:
        f.write(uploaded_file.getbuffer())

    if has_file_changed(PDF_PATH):
        with st.spinner("PDF changed. Re-ingesting..."):
            ingest(PDF_PATH)
            update_file_hash(PDF_PATH)
        st.success("Re-ingestion complete.")


# ---------- QUESTION INPUT ----------
query = st.text_input("Ask a question")

if st.button("Submit"):

    if not query:
        st.warning("Please enter a question.")
    else:
        with st.spinner("Retrieving answer..."):

            # ✅ Pass doc_id (PDF_PATH) into orchestrator
            doc_id = generate_doc_id(PDF_PATH)
            result = orchestrate(query, doc_id)

            st.write("**Detected Query Type:**", result["query_type"])

            answer = generate_answer(query, result["context"])

            st.markdown("### Answer")
            st.write(answer)