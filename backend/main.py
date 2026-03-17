from typing import List, Literal

from fastapi import FastAPI
from pydantic import BaseModel
from ollama_client import prompt_ollama

app = FastAPI()


class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.post("/chat")
async def chat(request: ChatRequest):
    messages = [message.model_dump() for message in request.messages]
    response = prompt_ollama(messages)
    return {"response": response.model_dump()}