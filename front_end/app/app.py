import streamlit as st
import os
import json
from dotenv import load_dotenv, find_dotenv
from langchain.chains import RetrievalQA
from langchain.document_loaders import Docx2txtLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter


# Configuration and loading
load_dotenv(find_dotenv())  # Load environment variables from .env file

# Document-specific configurations
document_path = "/home/elias/Documents/10 Academy/WEEK 11/LegalAI-RAG-Contract-Advisor/data/Evaluation Sets/Robinson Advisory.docx"  
loader = Docx2txtLoader(document_path)
texts = loader.load()

# Text splitting and embeddings
text_splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=50)
texts = text_splitter.split_documents(texts)
embeddings = OpenAIEmbeddings(
    model="text-embedding-ada-002", api_key=os.environ["OPENAI_API_KEY"]
)

# Vector store and retriever
vector_store = vector_store = FAISS.from_documents(texts, embeddings)
retriever = vector_store.as_retriever(search_kwargs={"k": 1})

# Question-answering system
qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=retriever)

def answer_query(query):
    """Answers a given query using the trained QA system."""

    try:
        # relevant_docs = retriever.get_relevant_documents(query)
        response = qa.run(query)
        formatted_response = format_response(response)
        return formatted_response

    except Exception as e:  # Handle potential errors gracefully
        return f"An error occurred: {e}"

def format_response(response):
    """Formats the response with relevant document snippets or other information."""

    # Customize formatting based on your preferences (e.g., include snippets)
    return f"Answer: {response}"

def main():
# Navigation bar with white background
   
    
    st.set_page_config(page_title="LegalAI-RAG-Contract-Advisor")

    # Display the HTML template
    # st.markdown(html_temp, unsafe_allow_html=True)
    st.title("Ask me a question about the document:")
    
    query = st.text_input("", placeholder="Type your question here...")
    
    if query:
        response = answer_query(query)
        st.write(response)

if __name__ == "__main__":
    main()
