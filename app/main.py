import boto3
import uuid 
from fastapi import FastAPI, APIRouter, Request, File, UploadFile, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Annotated


app= FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
s3 = boto3.client('s3')
bucket_name = 'wehelp-taipei-spot'

class FileRequest(BaseModel):
    fileName: str
    fileType: str

@app.get("/", include_in_schema=False)
async def index():
	return FileResponse("app/static/index.html", media_type="text/html")

@app.post("/api/messages")
async def post_message_data(file: UploadFile = File(...),  text: str = Form(...)):
	uid = uuid.uuid4()
	file_name = str(file.filename) + str(uid)
	contents = await file.read()

	try:
		response = await s3.put_object(Bucket=bucket_name, Key=file_name, Body=contents)
		return JSONResponse(content={"ok": "true"})
	except Exception as e:
		return JSONResponse(content={"message": f"Failed to upload file: {str(e)}"}, status_code=500)