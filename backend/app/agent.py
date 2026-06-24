import os

from dotenv import load_dotenv
from langchain_xai import ChatXAI
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
)

class Agent:
    def __init__(self):
        self.llm = None
        self.prelude()

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
            HumanMessage(
                content="Explain LangChain simply."
            ),
        ]

    def reply(self, prompt):
        self.messages.append(HumanMessage(prompt))
        response = self.llm.invoke(self.messages) 
        return response.content
