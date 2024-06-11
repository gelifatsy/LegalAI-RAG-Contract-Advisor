from langchain_community.chat_models import ChatOpenAI

import os
from langchain.embeddings.openai import OpenAIEmbeddings


from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
import openai
openai_api_key=openai.api_key = os.environ['OPENAI_API_KEY']



def instantiate_LLM(LLM_provider,api_key,temperature=0.5,top_p=0.95,model_name=None):
    """Instantiate LLM in Langchain.
    Parameters:
        LLM_provider (str): the LLM provider; in ["OpenAI","Google","HuggingFace"]
        model_name (str): in ["gpt-3.5-turbo", "gpt-3.5-turbo-0125", "gpt-4-turbo-preview", 
            "gemini-pro", "mistralai/Mistral-7B-Instruct-v0.2"].            
        api_key (str): google_api_key or openai_api_key or huggingfacehub_api_token 
        temperature (float): Range: 0.0 - 1.0; default = 0.5
        top_p (float): : Range: 0.0 - 1.0; default = 1.
    """
    if LLM_provider == "OpenAI":
        llm = ChatOpenAI(
            api_key=api_key,
            model=model_name, # in ["gpt-3.5-turbo", "gpt-3.5-turbo-0125", "gpt-4-turbo-preview"]
            temperature=temperature,
            model_kwargs={
                "top_p": top_p
            }
        )
    if LLM_provider == "Google":
        llm = ChatGoogleGenerativeAI(
            google_api_key=api_key,
            model=model_name, # "gemini-pro"
            temperature=temperature,
            top_p=top_p,
            convert_system_message_to_human=True
        )
    if LLM_provider == "HuggingFace":
        llm = HuggingFaceHub(
            repo_id=model_name, # "mistralai/Mistral-7B-Instruct-v0.2"
            huggingfacehub_api_token=api_key,
            model_kwargs={
                "temperature":temperature,
                "top_p": top_p,
                "do_sample": True,
                "max_new_tokens":1024
            },
        )
    return llm


from langchain.memory import ConversationSummaryBufferMemory,ConversationBufferMemory

def create_memory(model_name='gpt-3.5-turbo',memory_max_token=None):
    """Creates a ConversationSummaryBufferMemory for gpt-3.5-turbo.
    Creates a ConversationBufferMemory for the other models."""
    
    if model_name=="gpt-3.5-turbo":
        if memory_max_token is None:
            memory_max_token = 1024 # max_tokens for 'gpt-3.5-turbo' = 4096
        memory = ConversationSummaryBufferMemory(
            max_token_limit=memory_max_token,
            llm=ChatOpenAI(model_name="gpt-3.5-turbo",openai_api_key=openai_api_key,temperature=0.1),
            return_messages=True,
            memory_key='chat_history',
            output_key="answer",
            input_key="question"
        )
    else:
        memory = ConversationBufferMemory(
            return_messages=True,
            memory_key='chat_history',
            output_key="answer",
            input_key="question",
        )  
    return memory