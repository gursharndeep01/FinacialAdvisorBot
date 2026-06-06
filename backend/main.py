from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import chat
from memory import clear_memory
from rag import build_index
from rag import get_db


app= FastAPI(tittle="Financial Advisor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    session_id: str="default"
    
class SessionRequest(BaseModel):
    session_id: str


@app.on_event("startup")
async def startup_event():
    import os
    if not os.path.exists("../faiss_index/index.faiss"):
        print("Building FAISS index...")
        build_index()
    print("Preloading FAISS index...")
    get_db()
    print("Ready!")
    
@app.get("/")
def root():
    return {"status": "Financial Advisor API is running"}
@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    try:
        response = chat(request.message, request.session_id)
        return {"response": response,
                "session_id": request.session_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/clear")
def clear_session(request: SessionRequest):
    result = clear_memory(request.session_id)
    return {"cleared": result}
@app.post("/rebuild_index")
def rebuild_index():
    try:
        build_index()
        return {"status": "Index rebuilt successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))