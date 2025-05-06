### LangMem FastAPI Server: Entry Point (Structured Memory Version + Auto GPT Reply)

# file: app/main.py
import os
from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List, Optional
from langmem.tool import LangMemTool
from langmem.llm_client import ask_llm

app = FastAPI()


class MemoryInput(BaseModel):
    user_id: str
    metadata: dict
    comment: str
    tags: Optional[List[str]] = []
    auto_reply: Optional[bool] = False

class QueryInput(BaseModel):
    user_id: str
    question: str
    hotel_url: Optional[str] = None
    top_k: Optional[int] = 10
    style: Optional[str] = "detailed"



@app.post("/memories/add")
def add_memory(payload: MemoryInput):
    mem_tool = LangMemTool(user_id=payload.user_id)
    # Convert structured data to GPT-readable text
    meta_parts = [f"{k.replace('_', ' ').capitalize()}: {v}" for k, v in payload.metadata.items()]
    meta_text = "\n".join(meta_parts)
    structured_text = f"{meta_text}\nComment: {payload.comment}"

    memory_data = {
        "text": structured_text,
        "metadata": payload.metadata,
        "tags": payload.tags
    }
    mem_tool.add_memory_object(memory_data)
    mem_tool.save()

    reply = None
    if payload.auto_reply:
        reply = mem_tool.generate_reply_to_comment(payload.metadata, payload.comment)

    return {"status": "added", "reply": reply}

@app.get("/memories/search")
def search_memory(
    user_id: str = Query(...),
    q: str = Query(...),
    hotel_url: Optional[str] = None,
    k: int = 5
):
    mem_tool = LangMemTool(user_id=user_id)
    results = mem_tool.store.search(q, k)

    if hotel_url:
        results = [r for r in results if r[0].get("metadata", {}).get("hotel_url") == hotel_url]

    return [
        {
            "text": m["text"],
            "metadata": m.get("metadata", {}),
            "tags": m.get("tags", []),
            "timestamp": m.get("timestamp"),
            "score": score
        }
        for m, score in results
    ]


@app.post("/summarize")
def summarize(input: QueryInput):
    mem_tool = LangMemTool(user_id=input.user_id)
    results = mem_tool.store.search(input.question, k=input.top_k)
    if input.hotel_url:
        results = [r for r in results if r[0].get("metadata", {}).get("hotel_url") == input.hotel_url]

    hotel_name = None
    for m, _ in results:
        hotel_name = m.get("metadata", {}).get("hotel_name")
        if hotel_name:
            break

    context = "\n".join([f"- {m['text']}" for m, _ in results])

    if input.style == "short":
        instruction = "Summarize the main compliments and complaints in 1–2 sentences. Avoid lists."
    else:
        instruction = "Summarize the main compliments and complaints. Use bullet points if needed."

    prompt = f"""You are an assistant analyzing guest reviews for a hotel.
    Hotel name: {hotel_name or 'Unknown'}
    
    Here are some guest comments:
    {context}
    
    {instruction}
    """

    response = ask_llm(prompt)
    return {
        "hotel": hotel_name,
        "style": input.style,
        "answer": response
    }


@app.post("/reset")
def reset(user_id: str = Query(...)):
    mem_tool = LangMemTool(user_id=user_id)
    mem_tool.store.memories.clear()
    mem_tool.store.index.reset()
    mem_tool.save()
    if os.path.exists(mem_tool.memory_file):
        os.remove(mem_tool.memory_file)
    return {"status": f"memory for user '{user_id}' has been reset"}

