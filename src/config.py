import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone, ServerlessSpec

from langchain.chat_models import ChatOpenAI


class Settings:
    def __init__(self):
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")


def configure_cors(app: FastAPI):
    origins = [
        "*",
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def verify_pinecone_index():
    """ Verify if the Pinecone index exists """
    try:
        pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        index_name = "document"
        if index_name not in pc.list_indexes().names():
            pc.create_index(
                name=index_name,
                dimension=1536,
                metric="euclidean",
                spec=ServerlessSpec(
                    cloud='aws',
                    region='us-east-1'
                )
            )
    except Exception as e:
        return {"error": str(e)}


def instance_pinecone():
    """ Initialize a Pinecone instance and return the index "document"""
    return Pinecone(api_key=settings.PINECONE_API_KEY).Index("document")


def instance_embeddings():
    return OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)


def instance_llm():
    return ChatOpenAI(temperature=0, openai_api_key=settings.OPENAI_API_KEY)


settings = Settings()
