import sys
import os
import openai
import getpass

# Load environment variables (replace with your actual keys)
openai.api_key = os.environ["OPENAI_API_KEY"]
# os.environ["COHERE_API_KEY"] = getpass.getpass("Cohere API Key:")

from langchain_community.document_loaders import TextLoader, Docx2txtLoader
from langchain_community.embeddings import CohereEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Cohere
from langchain.retrievers import ContextualCompressionRetriever
from langchain_cohere import CohereRerank
from langchain.chains import RetrievalQA
from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

def pretty_print_docs(docs):
    print(
        f"\n{'-' * 100}\n".join(
            [f"Document {i+1}:\n\n" + d.page_content for i, d in enumerate(docs)]
        )
    )

def load_document(document_path):
    """
    Loads a document from the specified path using Docx2txtLoader.

    Args:
        document_path (str): Path to the document file.

    Returns:
        list: List of document text fragments.
    """

    try:
        loader = Docx2txtLoader(document_path)
        documents = loader.load()
        return documents
    except Exception as e:
        raise

def load_documents_from_folder(folder_path):
    """
    Loads all .docx files from a folder, combining their text fragments.

    Args:
        folder_path (str): Path to the folder containing the documents.

    Returns:
        list: List of all combined text fragments from the documents.
    """

    all_documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".docx"):
            file_path = os.path.join(folder_path, filename)
            documents = load_document(file_path)
            all_documents.extend(documents)
    return all_documents

# Replace with your document folder path
folder_path = "/home/elias/Documents/10 Academy/WEEK 11/LegalAI-RAG-Contract-Advisor/data/Evaluation Sets/contract"  # Replace with your folder path

all_documents = load_documents_from_folder(folder_path)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
split_texts = text_splitter.split_documents(all_documents)

vector_store = FAISS.from_documents(split_texts, OpenAIEmbeddings())
retriever = vector_store.as_retriever(search_kwargs={"k": 5})

compressor = CohereRerank(model="rerank-english-v3.0")
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor, base_retriever=retriever
)

qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=compression_retriever)

def answer_query(query):
    """Answers a given query using the trained QA system."""

    try:
        response = qa.invoke(query)
        return response["result"].strip()

    except Exception as e:  # Handle potential errors gracefully
        return f"An error occurred: {e}"

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Update with your frontend URL
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

class Query(BaseModel):
    query: str

@app.post("/answer")
async def answer(query: Query):
    """Receives a query from the frontend and returns the answer."""
    response = answer_query(query.query)
    return {"answer": response}