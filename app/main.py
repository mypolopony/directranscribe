from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from app.transcriber import transcribe_bytes

app = FastAPI()

@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    audio_bytes = await file.read()
    text = transcribe_bytes(audio_bytes)
    return JSONResponse(content={"transcript": text})