from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.prompts import ChatPromptTemplate

import re
import traceback
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
BACKEND_DIR = BASE_DIR.parent
UPLOAD_DIR = BASE_DIR / "uploads"

load_dotenv(BACKEND_DIR / ".env")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===========================
# Global Variables
# ===========================

pdf_chunks = []


# ===========================
# Gemini LLM
# ===========================

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3,
)


# ===========================
# Prompt
# ===========================

prompt = ChatPromptTemplate.from_template(
"""
Answer the question using only the provided context.

Context:
{context}

Question:
{question}
"""
)


# ===========================
# Helper Function
# ===========================

def format_docs(docs):
    return "\n\n".join(docs)


def retrieve_context(question, k=3):
    terms = set(re.findall(r"\w+", question.lower()))

    if not terms:
        return pdf_chunks[:k]

    scored_chunks = []

    for chunk in pdf_chunks:
        chunk_terms = set(re.findall(r"\w+", chunk.lower()))
        score = len(terms & chunk_terms)
        scored_chunks.append((score, chunk))

    scored_chunks.sort(key=lambda item: item[0], reverse=True)

    best_chunks = [chunk for score, chunk in scored_chunks[:k] if score > 0]

    return best_chunks or pdf_chunks[:k]


# ===========================
# Create RAG Pipeline
# ===========================

def create_rag(pdf_path):
    global pdf_chunks

    # Load PDF
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    print("Pages:", len(documents))

    # Split Documents
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documents)
    pdf_chunks = [chunk.page_content for chunk in chunks]

    print("Chunks:", len(chunks))


# ===========================
# Upload API
# ===========================

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file was selected.")

    if file.content_type != "application/pdf" and not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Please upload a PDF file.")

    UPLOAD_DIR.mkdir(exist_ok=True)

    safe_filename = Path(file.filename).name
    pdf_path = UPLOAD_DIR / safe_filename

    content = await file.read()

    if not content:
        raise HTTPException(status_code=400, detail="The uploaded PDF is empty.")

    with open(pdf_path, "wb") as f:
        f.write(content)

    try:
        # Create new RAG for uploaded PDF
        create_rag(str(pdf_path))
    except Exception as e:
        print("UPLOAD ERROR:", e)
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"PDF was saved, but processing failed: {e}",
        ) from e


    return {
        "message": "PDF uploaded and processed successfully.",
        "filename": safe_filename,
    }


# ===========================
# Chat API
# ===========================

@app.post("/chat")
async def chat(question: str):
    if not pdf_chunks:
        raise HTTPException(status_code=400, detail="Please upload a PDF first.")

    try:
        context = format_docs(retrieve_context(question))
        response = (prompt | llm).invoke({
            "context": context,
            "question": question,
        })

        return {"answer": response.content}

    except Exception as e:
        print("ERROR:", e)
        traceback.print_exc()

        return {"answer": str(e)}
