from typing import List, Literal
from uuid import uuid4
from qdrant_client.http.models import PointStruct

from document_processor import extract_text, chunk_text
from ollama_client import get_embedding, prompt_ollama
from qdrant_setup import ensure_collection, upsert_points
from fastapi import FastAPI, File, UploadFile, HTTPException
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

@app.post("/documents/upload")
async def add_documents(file: UploadFile = File(...)):
    content = await file.read()

    try:
        text = extract_text(file.filename, content)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    if not text.strip():
        raise HTTPException(status_code=400, detail="No extractable text found")

    chunks = chunk_text(text)
    vectors = get_embedding(chunks)
    ensure_collection(len(vectors[0]))

    document_id = str(uuid4())
    points = []

    for index, (chunk, vector) in enumerate(zip(chunks, vectors)):
        points.append(
            PointStruct(
                id=f"{document_id}-{index}",
                vector=vector,
                payload={
                    "document_id": document_id,
                    "filename": file.filename,
                    "chunk_index": index,
                    "text": chunk,
                    "mime_type": file.content_type,
                },
            )
        )

    upsert_points(points)

    return {
        "document_id": document_id,
        "filename": file.filename,
        "chunks_indexed": len(points),
    }