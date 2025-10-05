import os
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("Please set the GOOGLE_API_KEY environment variable first.")

# Configure Gemini LLM (for responses)
llm = GoogleGenAI(model="gemini-2.5-flash", api_key=GOOGLE_API_KEY)


# Configure HuggingFace Embeddings
embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Apply globally so LlamaIndex uses them everywhere
Settings.llm = llm
Settings.embed_model = embed_model

# Load documents 
documents = SimpleDirectoryReader("docs").load_data()

# Build a vector index 
index = VectorStoreIndex.from_documents(documents)

# Create a query engine
query_engine = index.as_query_engine()

query = "Summarize the resume(6).pdf in 3 key points."
response = query_engine.query(query)

print("Query:", query)
print("Answer:", response.response)
