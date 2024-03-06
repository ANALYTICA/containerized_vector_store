from typing import Union
from fastapi import FastAPI
from llama import load_model, get_retriever, raq_question
from pydantic import BaseModel

app = FastAPI()
model = load_model()
retriever = get_retriever()

@app.get("/")
def read_root():
    return {"This": "is a test"}

class Message(BaseModel):
    text: str

@app.put("/chat/response")
async def respond(message: Message):
    results = raq_question(message.text, model, retriever)
    return results