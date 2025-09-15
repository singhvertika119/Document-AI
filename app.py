import os
import re 
import streamlit as st
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings

# --------------------------
# Setup Gemini + Embeddings
# --------------------------

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("Please set the GOOGLE_API_KEY environment variable first.")
    st.stop()

# Configure LLM + Embeddings
llm = Gemini(model="models/gemini-1.5-flash", api_key=GOOGLE_API_KEY)
embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

Settings.llm = llm
Settings.embed_model = embed_model

# --------------------------
# Streamlit UI
# --------------------------

st.set_page_config(page_title="AI Research Assistant", page_icon="🤖", layout="wide")

st.title("📘 AI Research Assistant")
st.markdown("Ask questions about your own documents using **RAG + Gemini**")

# Sidebar for document loading
st.sidebar.header("📂 Documents")
if st.sidebar.button("Load Documents"):
    with st.spinner("Loading and indexing documents..."):
        try:
            documents = SimpleDirectoryReader("docs").load_data()
            index = VectorStoreIndex.from_documents(documents)
            st.session_state["query_engine"] = index.as_query_engine()
            st.success("Documents loaded successfully!")
        except Exception as e:
            st.error(f"Error loading documents: {e}")

# Query input
if "query_engine" in st.session_state:
    query = st.text_input("🔎 Ask a question about your documents:")
    if st.button("Get Answer"):
        if query.strip() == "":
            st.warning("Please enter a question.")
        else:
            with st.spinner("Thinking..."):
                response = st.session_state["query_engine"].query(query)
                st.subheader("✅ Answer:")
                st.write(response.response)
else:
    st.info("➡️ Load documents first from the sidebar to start querying.")
