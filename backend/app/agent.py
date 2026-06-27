import os

from dotenv import load_dotenv
from langchain_xai import ChatXAI
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
)

from app.global_vars import *
from app.preprocess import Preprocessor

class Agent:
    def __init__(self):
        self.llm = None
        self.prelude()
        self.PP = Preprocessor()

    def prelude(self):
        load_dotenv()

        # Read API key
        XAI_API_KEY = os.getenv("XAI_API_KEY")

        if not XAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set")

        # Initialize model
        self.llm = ChatXAI(
            model="grok-4",
            temperature=0.7,
            api_key=XAI_API_KEY,
        )

        # Conversation
        self.messages = [
            SystemMessage(
                content="You are a helpful assistant."
            ),
        ]

    def reply(self, query):
        results = self.PP.vectorstore.similarity_search(
            query,
            k=20
        )
        context = "\n\n".join(
                doc.page_content
                for doc in results
        )

        prompt = f"""
Use the following context to answer the question.

Context:
{context}

Question:
{query}
"""
        response = self.llm.invoke(prompt) 
        return response.content
