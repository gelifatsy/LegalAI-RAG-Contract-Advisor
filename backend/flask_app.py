from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from dataclasses import dataclass
import os
import sys
import getpass
import openai
from langchain_community.document_loaders import TextLoader, Docx2txtLoader
from langchain_community.embeddings import CohereEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Cohere
from langchain.retrievers import ContextualCompressionRetriever
from langchain_cohere import CohereRerank
from langchain.chains import RetrievalQA
from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])

@dataclass
class Query:
    query: str

def pretty_print_docs(docs):
    print(
        f"\n{'-' * 100}\n".join(
            [f"Document {i+1}:\n\n" + d.page_content for i, d in enumerate(docs)]
        )
    )

def load_document(document_path):
    try:
        loader = Docx2txtLoader(document_path)
        documents = loader.load()
        return documents
    except Exception as e:
        raise

def load_documents_from_folder(folder_path):
    all_documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".docx"):
            file_path = os.path.join(folder_path, filename)
            documents = load_document(file_path)
            all_documents.extend(documents)
    return all_documents

folder_path = "/home/elias/Documents/10 Academy/WEEK 11/LegalAI-RAG-Contract-Advisor/data/Evaluation Sets/contract"

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
    try:
        response = qa.invoke(query)
        return response["result"].strip()
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/answer', methods=['POST'])
@cross_origin(origins=["http://localhost:5173"])
def answer():
    query = Query(**request.get_json())
    response = answer_query(query.query)
    return jsonify({'answer': response})

if __name__ == '__main__':
    app.run(debug=True)