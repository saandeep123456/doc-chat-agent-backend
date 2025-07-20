from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from services.document_service import process_document
from services.query_service import answer_question, get_chat_history

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "ok", "message": "FastAPI backend is running"}
    
@app.post("/upload")
async def upload_file(file: UploadFile, user_id: str = Form(...)):
    await process_document(file, user_id)
    return {"status": "success", "filename": file.filename}

@app.post("/ask")
async def ask_question(question: str = Form(...), user_id: str = Form(...)):
    answer = await answer_question(question, user_id)
    return {"answer": answer}

@app.get("/history/{user_id}")
async def get_user_history(user_id: str):
    return {"messages": get_chat_history(user_id)}
