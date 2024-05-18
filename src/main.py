from fastapi import FastAPI, File, UploadFile, HTTPException

from src import service

app = FastAPI()


@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are allowed.")
    return service.upload_pdf(file)


@app.post("/ask/")
async def ask_question(question: str):
    """ Ask a question to AI """
    return service.ask(question)
