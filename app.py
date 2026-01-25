import streamlit as st
import requests


def load_css():
    """Injects custom CSS to style the Streamlit app."""
    css = """
    <style>
        /* --- General Styles --- */
        body {
            background-color: #0F172A; /* Dark Navy Blue */
        }
        /* Main container */
        [data-testid="stAppViewContainer"] {
            background-color: #0F172A;
        }
        /* Main text color */
        .stApp {
            color: #E2E8F0; /* Light gray */
        }

        /* --- Header --- */
        /* Title */
        h1 {
            color: #FFFFFF;
            font-size: 2.5rem;
            font-weight: 600;
        }
        /* Subtitle */
        .subtitle {
            color: #94A3B8; /* Muted gray */
            font-size: 1.1rem;
            margin-top: -10px;
        }

        /* --- Input Area --- */
        /* Input Label */
        [data-testid="stTextInput"] label {
            color: #E2E8F0;
            font-size: 1.1rem;
            font-weight: 600;
        }
        /* Text Input Box */
        [data-testid="stTextInput"] input {
            background-color: #1E293B; /* Darker input bg */
            border: 1px solid #334155;
            border-radius: 0.5rem; /* 8px */
            color: #FFFFFF;
        }
        /* Text Input placeholder */
        [data-testid="stTextInput"] input::placeholder {
            color: #64748B;
        }

        /* --- Button --- */
        [data-testid="stButton"] button {
            background-color: #0D9488; /* Teal */
            color: #FFFFFF;
            border: none;
            border-radius: 0.5rem;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            transition: background-color 0.3s ease;
        }
        [data-testid="stButton"] button:hover {
            background-color: #0F766E; /* Darker teal */
        }
        [data-testid="stButton"] button:active {
            background-color: #115E59; /* Even darker */
        }

        /* --- Answer Area --- */
        /* Answer Subheader "✅ Answer:" */
        h3 {
            color: #FFFFFF;
            font-size: 1.5rem;
            font-weight: 600;
        }
        /* Answer list item */
        .answer-item {
            color: #E2E8F0;
            font-size: 1rem;
            line-height: 1.6;
        }
        .answer-item-check {
            color: #0D9488; /* Teal checkmark */
            margin-right: 8px;
            font-weight: bold;
        }

        /* --- Other Components --- */
        /* Spinner */
        [data-testid="stSpinner"] > div {
            color: #0D9488; /* Teal spinner */
        }
        /* Error Box */
        [data-testid="stException"] {
            background-color: #3F1A1A;
            border-color: #DC2626;
            border-radius: 0.5rem;
        }
        /* Warning Box */
        [data-testid="stAlert"] {
            border-radius: 0.5rem;
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# Streamlit UI


# Set page config
st.set_page_config(
    page_title="Document AI",
    page_icon="📄",  
    layout="centered"  
)


load_css()



st.markdown("<h1>📄 Document AI</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='subtitle'>Ask questions about your own documents using RAG + Gemini (via FastAPI)</p>",
    unsafe_allow_html=True
)


query = st.text_input(
    "🔹 Ask a question about your documents:",
    placeholder="summarize the resume(6).pdf in 3 points"
)

# FastAPI backend URL
API_URL = "http://127.0.0.1:8000/ask/"

if st.button("Get Answer"):
    if query.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            try:
                response = requests.post(API_URL, json={"question": query})

                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("answer", "No answer found.")

                    
                    st.subheader("✅ Answer:") 

                    
                    if isinstance(answer, list):
                        for point in answer:
                            st.markdown(
                                f"<p class='answer-item'><span class='answer-item-check'>✔</span> {point}</p>",
                                unsafe_allow_html=True
                            )
                    elif '\n' in answer: 
                        answer_points = [p for p in answer.split('\n') if p.strip()]
                        for point in answer_points:
                            st.markdown(
                                f"<p class='answer-item'><span class='answer-item-check'>✔</span> {point}</p>",
                                unsafe_allow_html=True
                            )
                    else: 
                        st.markdown(
                            f"<p class='answer-item'><span class='answer-item-check'>✔</span> {answer}</p>",
                            unsafe_allow_html=True
                        )

                else:
                    st.error(f"API Error (Status {response.status_code}): {response.text}")

            except requests.exceptions.ConnectionError:
                st.error("Error: Could not connect to the FastAPI backend.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")