
import os
from langchain.embeddings.openai import OpenAIEmbeddings


from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
import openai
openai_api_key=openai.api_key = os.environ['OPENAI_API_KEY']

def select_embeddings_model(LLM_service="OpenAI"):
    if LLM_service == "OpenAI":
        openai_api_key = os.environ.get("OPENAI_API_KEY")
        embeddings = OpenAIEmbeddings(
            model='text-embedding-ada-002',
            api_key=openai_api_key
        )

    if LLM_service == "Google":
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=google_api_key
        )
    if LLM_service == "HuggingFace":
        embeddings = HuggingFaceInferenceAPIEmbeddings(    
            api_key=HF_key, 
            model_name="thenlper/gte-large"
        )
         
    return embeddings