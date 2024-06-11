import logging
from logger_config import configure_logger
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker

from langchain.vectorstores import Chroma
from langchain_community.vectorstores import FAISS
from langchain.document_loaders import Docx2txtLoader
import os


from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
import openai
openai_key=openai.api_key = os.environ['OPENAI_API_KEY']

logger = configure_logger()

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
        logger.info("Document loaded successfully")
        return documents
    except Exception as e:
        logger.error("Error loading document: %s", e)
        raise

import os

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
            try:
                documents = load_document(file_path)  # Use your provided function
                all_documents.extend(documents)
            except Exception as e:
                logger.error("Error loading document %s: %s", file_path, e)

    return all_documents




def split_document(documents, splitter_type="RecursiveCharacterTextSplitter", chunk_size=300, chunk_overlap=0):
    """
    Splits a document into text fragments using the specified splitter type.

    Args:
        documents (list): List of document text fragments.
        splitter_type (str, optional): Type of splitter to use.
                                      Options: "semantic", "character", or "recursive_character".
                                       Defaults to "recursive_character".
        chunk_size (int, optional): Size of each text fragment (for character-based splitters).
                                        Defaults to 300.
        chunk_overlap (int, optional): Amount of overlap between fragments (for character-based splitters).
                                          Defaults to 0.

    Returns:
        list: List of split text fragments.
    """

    try:
        if splitter_type == "SemanticChunker":
            text_splitter = SemanticChunker(OpenAIEmbeddings())
        elif splitter_type == "CharacterTextSplitter":
            text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        elif splitter_type == "RecursiveCharacterTextSplitter":
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        else:
            raise ValueError(f"Invalid splitter type: {splitter_type}")

        texts = text_splitter.split_documents(documents)
        logger.info("Documents split successfully")
        return texts

    except Exception as e:
        logger.error("Error splitting documents: %s", e)
        raise  # Re-raise the exception for further handling



# retrieval.py
def create_embeddings(texts):
    """
    Generates embeddings for the provided text fragments using OpenAIEmbeddings.

    Args:
        texts (list): List of text fragments.

    Returns:
        OpenAIEmbeddings: Embeddings object.
    """

    try:
        embeddings = OpenAIEmbeddings(
            model='text-embedding-ada-002',
            api_key=openai_key
        )
        logger.info("Embeddings created successfully")
        return embeddings

    except Exception as e:
        logger.error("Error creating embeddings: %s", e)
        raise  # Re-raise the exception




from langchain.vectorstores import Chroma, FAISS


def create_vector_store(documents, embeddings, vector_store=None):
    """
    Creates a vector store using the provided documents and embeddings.

    Args:
        documents (list): List of documents.
        embeddings (OpenAIEmbeddings): Embeddings object.
        vector_store (Optional[VectorStore]): An existing vector store to use.

    Returns:
        VectorStore: The created vector store.
    """

    try:
        if vector_store is None:
            # Choose the appropriate vector store based on type
            if isinstance(vector_store, FAISS):
                vector_store = FAISS.from_documents(documents, embeddings)
            elif isinstance(vector_store, Chroma):
                vector_store = Chroma.from_documents(documents, embeddings)
            else:
                # Default to FAISS if no specific type or an unsupported type is provided
                vector_store = FAISS.from_documents(documents, embeddings)
            logger.info("Vector store created successfully")
        else:
            logger.info("Using existing vector store")

        return vector_store

    except Exception as e:
        logger.error("Error creating vector store: %s", e)
        raise  # Re-raise the exception for further handling

def create_retriever(vector_store, k):
  """
  Creates a retriever from the provided vector store with the specified k value.

  Args:
      vector_store (VectorStore): The vector store to use.
      k (int): The number of nearest neighbors to retrieve.

  Returns:
      RetrievalStore: The created retriever.
  """

  try:
    retriever = vector_store.as_retriever(search_kwargs={"k": k})
    logger.info("Retriever created successfully")
    return retriever

  except Exception as e:
    logger.error("Error creating retriever: %s", e)
    raise  # Re-raise the exception for further handling

def get_relevant_documents(query, vector_store, k):
    """
    Retrieves relevant documents for a given query using the vector store.

    Args:
        query (str): The query to search for.
        vector_store (Chroma): Vector store object.
        k (int, optional): Number of top documents to retrieve. Defaults to 1.

    Returns:
        list: List of retrieved documents.
    """

    retriever = vector_store.as_retriever(search_kwargs={"k": k})
    relevant_docs = retriever.get_relevant_documents(query)
    return relevant_docs

# qa_system.py
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA

# def create_qa_system(retriever):


def create_qa_system(retriever, llm=OpenAI(), chain_type="stuff"):
  """
  Creates a RetrievalQA system using the provided retriever and LLM.

  Args:
      retriever (RetrievalStore): The retrieval store to use.
      llm (Optional[LLM]): The language model to use. Defaults to OpenAI().
      chain_type (str, optional): The type of chain to use. Defaults to "question_answering".

  Returns:
      RetrievalQA: The created RetrievalQA system.
  """

  try:
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type=chain_type, retriever=retriever)
    logger.info("QA system created successfully")
    return qa

  except Exception as e:
    logger.error("Error creating QA system: %s", e)
    raise  # Re-raise the exception for further handling
