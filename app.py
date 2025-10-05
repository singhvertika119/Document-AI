import streamlit as st
import requests

# --------------------------
# Streamlit UI
# --------------------------

st.set_page_config(page_title="AI Research Assistant", page_icon="🤖", layout="wide")

st.title("📘 Document AI")
st.markdown("Ask questions about your own documents using **RAG + Gemini (via FastAPI)**")

API_URL = "http://127.0.0.1:8000/ask/"  # FastAPI backend

query = st.text_input("🔎 Ask a question about your documents:")

if st.button("Get Answer"):
    if query.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            try:
                response = requests.post(API_URL, json={"question": query})
                if response.status_code == 200:
                    data = response.json()
                    st.subheader("✅ Answer:")
                    st.write(data["answer"])
                else:
                    st.error(f"API Error: {response.text}")
            except Exception as e:
                st.error(f"Error connecting to API: {e}")
