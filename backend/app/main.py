from fastapi import FastAPI
from pydantic import BaseModel
from app.agent import Agent
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="PDF Analyzer")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", # React endpoint
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = Agent()

@app.get("/")
def root():
    return {"message": "API running"}

class ChatRequest(BaseModel):
    question: str

@app.post("/chat")
def reply(req: ChatRequest):
    augmented_prompt = f"""
    Answer the following question:

    {req.question}
    """

    response_str = agent.reply(augmented_prompt)

    return {
        "answer": response_str
    }
