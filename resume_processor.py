import os
import asyncio
from dotenv import load_dotenv

# ✅ Gemini SDK
import google.generativeai as genai

# Loaders & splitters
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader
)

from langchain.text_splitter import RecursiveCharacterTextSplitter

# Vector store
from langchain_community.vectorstores import Chroma

# Retriever
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.base import AttributeInfo

# ✅ Embeddings (LOCAL — stable)
from langchain_community.embeddings import HuggingFaceEmbeddings


# ==================== Event Loop Fix ====================
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())


# ==================== Keys ====================
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
if not GOOGLE_API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY is missing. Check your .env file.")


# ✅ Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)


# ==================== Models ====================

# ✅ Gemini LLM (NEW WAY)

model = genai.GenerativeModel("gemini-3.5-flash")# ✅ Local embeddings (no API issues)
embedding = HuggingFaceEmbeddings()


# ==================== Functions ====================

def load_resume(file_path):
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith(".docx"):
        loader = Docx2txtLoader(file_path)
    elif file_path.endswith(".txt"):
        loader = TextLoader(file_path, encoding="utf-8")
    else:
        raise ValueError("Unsupported file format.")
    return loader.load()


def split_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    return splitter.split_documents(docs)


def store_to_vectorstore(chunks, persist_directory="chroma_store"):
    texts = [chunk.page_content for chunk in chunks]
    metadatas = [{"source": f"resume_chunk_{i}"} for i in range(len(texts))]

    vectordb = Chroma.from_texts(
        texts=texts,
        embedding=embedding,
        metadatas=metadatas,
        persist_directory=persist_directory
    )

    return vectordb


def run_self_query(query, persist_directory="chroma_store"):
    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding
    )

    metadata_field_info = [
        AttributeInfo(
            name="source",
            description="Where the chunk is from",
            type="string"
        )
    ]

    # ✅ NOTE: SelfQueryRetriever still needs LLM — replace with simple approach later
    retriever = SelfQueryRetriever.from_llm(
        llm=None,
        vectorstore=vectorstore,
        document_contents="Resume chunks",
        metadata_field_info=metadata_field_info
    )

    return retriever.get_relevant_documents(query)


def analyze_resume(chunks, job_description):
    # ✅ Combine all chunks into one analysis (reduces API calls)
    resume_text = "\n\n".join([chunk.page_content for chunk in chunks])
    
    prompt = f"""
Analyze this complete resume against the job description and provide:

1. Suitability Score (out of 100)
2. Skills Matched
3. Experience Relevance
4. Education Evaluation
5. Strengths
6. Weaknesses
7. Final Recommendation

Job Description:
{job_description}

Complete Resume:
{resume_text}
"""

    # ✅ Single API call instead of one per chunk
    response = model.generate_content(prompt)

    if hasattr(response, "text"):
        return response.text
    else:
        return "No response generated"