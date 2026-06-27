from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import time

from app.agent import Agent
from app.preprocess import Preprocessor
from app.global_vars import *

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

# Setup context directory
CONTEXT_DIR.mkdir(exist_ok=True)

agent = Agent()
preprocessor = Preprocessor()

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

@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    # TODO: Handle user inputing duplicate files

    contents = await file.read()
    # Check MIME type
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    # Check extension
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="File must have a .pdf extension."
        )

    filepath = CONTEXT_DIR / file.filename
    with open(filepath, "wb") as f:
        f.write(contents)

    time.sleep(3) # For testing

    metadata = {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(contents),
    }

    # Put data PDF through injestion pipeline
    await preprocessor.injest_pdf(metadata, file.filename) 

    return metadata
