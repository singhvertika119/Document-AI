from fastapi import FastAPI
from pydantic import BaseModel
from rag import rag_query

app = FastAPI(title="RAG API",
              description="FastAPI wrapper for RAG + Gemini", version="1.0")


class QueryRequest(BaseModel):
    question: str


@app.post("/ask/")
def ask_question(req: QueryRequest):
    return rag_query(req.question)
