from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os
from .ai import apicall



app = FastAPI()

origins = [
    "http://localhost",
    "http://20.119.81.24:3000",  # Replace with your React app's URL
]

# Add the CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

class ChatRequest(BaseModel):
    question: str

@app.post("/ask")
def ask_question(request: ChatRequest):
    answer = apicall(request.question)
    return {"answer": answer}