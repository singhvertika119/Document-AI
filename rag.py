import os
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError(
        "Please set the GOOGLE_API_KEY environment variable first.")

# Gemini LLM 
llm = GoogleGenAI(model="gemini-2.5-flash", api_key=GOOGLE_API_KEY)


# HuggingFace Embeddings
embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2")


Settings.llm = llm
Settings.embed_model = embed_model

# Load documents
documents = SimpleDirectoryReader("docs").load_data()

# Build a vector index
index = VectorStoreIndex.from_documents(documents)

# Create a query engine
query_engine = index.as_query_engine()


def rag_query(question: str) -> dict:

    response = query_engine.query(question)
    return {
        "question": question,
        "answer": response.response
    }
