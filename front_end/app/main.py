import sys, os
# sys.path.append(os.path.abspath(os.path.join('../scripts')))
import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import CohereEmbeddings
from langchain_community.vectorstores import FAISS

from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CohereRerank
from langchain_community.llms import Cohere
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import Docx2txtLoader
import getpass
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
import openai
openai_key=openai.api_key = os.environ['OPENAI_API_KEY']

# os.environ["COHERE_API_KEY"] = getpass.getpass("Cohere API Key:")


# from scripts.RAG_utils import load_document, load_documents_from_folder


import getpass
import os


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
        # logger.info("Document loaded successfully")
        return documents
    except Exception as e:
        # logger.error("Error loading document: %s", e)
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
            # try:
            documents = load_document(file_path)  # Use your provided function
            all_documents.extend(documents)
            # except Exception as e:
            #     # logger.error("Error loading document %s: %s", file_path, e)

    return all_documents

folder_path = "/home/elias/Documents/10 Academy/WEEK 11/LegalAI-RAG-Contract-Advisor/data/Evaluation Sets/contract"  # Replace with your folder path
all_documents = load_documents_from_folder(folder_path)


text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
split_texts = text_splitter.split_documents(all_documents)

vector_store=FAISS.from_documents(split_texts, OpenAIEmbeddings())
retriever = vector_store.as_retriever(
    search_kwargs={"k": 5}
)

compressor = CohereRerank()
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor, base_retriever=retriever
)

qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=compression_retriever)

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




