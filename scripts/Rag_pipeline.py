import os
import json
from dotenv import load_dotenv, find_dotenv
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader, Docx2txtLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma, FAISS
from langchain_community.vectorstores import FaissVectorStore

# Configuration and loading
_ = load_dotenv(find_dotenv())
openai_api_key = os.environ['OPENAI_API_KEY']
document_path = "../data/Evaluation Sets/Robinson Advisory.docx"
loader = Docx2txtLoader(document_path)
texts = loader.load()

# Text splitting and embeddings
text_splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=50)
texts = text_splitter.split_documents(texts)
embeddings = OpenAIEmbeddings(model='text-embedding-ada-002', api_key=openai_api_key)

# Vector store and retriever
vector_store = FaissVectorStore.from_documents(texts, embeddings)
retriever = vector_store.as_retriever(search_kwargs={"k": 1})

# Question-answering system
qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=retriever)

def answer_query(query):
    """Answers a given query using the trained QA system."""
    # Use retriever and QA system to generate response
    relevant_docs = retriever.get_relevant_documents(query)
    response = qa.run(query, context=relevant_docs)
    
    # Format and return the response
    formatted_response = format_response(relevant_docs, response)
    return formatted_response

def format_response(relevant_docs, response):
    """Optionally formats the response with retrieved document snippets."""
    # Customize formatting based on your preferences (e.g., include snippets if desired)
    if snippets_desired:
        formatted_response = "Found relevant documents:\n"
        for doc in relevant_docs:
            formatted_response += f"- {doc['page_content'][:50]}...\n"
        formatted_response += f"\nAnswer: {response}"
    else:
        formatted_response = response
    return formatted_response

if __name__ == "__main__":
    # Main input loop
    while True:
        query = input("Ask me a question about the document: ")
        if query.lower() == "quit":
            break
        response = answer_query(query)
        print(response)

