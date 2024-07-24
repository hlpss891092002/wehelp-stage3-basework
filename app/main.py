import boto3
import uuid 
import os
import requests
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, APIRouter, Request, File, UploadFile, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from pydantic import BaseModel
from typing import Annotated
from app.model.message_method import insert_message, get_all_message

logger = logging.getLogger(__name__)
Format = ' %(asctime)s - %(message)s'
logging.basicConfig(filename='app.log', encoding='utf-8', level=logging.INFO, format=Format)

class LogRequestMiddleware(BaseHTTPMiddleware):
		async def dispatch(self, request:Request, call_next):
				logger.info(f"IP : {request.client.host}, method : {request.method},  to URL: {request.url.path}'")
				response = await call_next(request)
				return response

app= FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
load_dotenv()

access_key_id = os.getenv("ACCESS_KEY_ID")
Secret_access_key = os.getenv("SECRECT_ACCESS_KEY")
aws_region = "ap-northeast-2"
s3 = boto3.client("s3", aws_access_key_id=access_key_id, aws_secret_access_key=Secret_access_key, region_name=aws_region)
bucket_name = "wehelp-taipei-spot"
CLOUDFRONT_DOMAIN = "d3iwepe7jlx8fj.cloudfront.net"

class FileRequest(BaseModel):
    fileName: str
    fileType: str

@app.get("/", include_in_schema=False)
async def index():
	return FileResponse("app/static/index.html", media_type="text/html")

@app.post("/api/messages")
async def post_message_data(file: UploadFile = File(...),  text: str = Form(...)):
	uid = uuid.uuid4()
	file_name = str(uid) +  str(file.filename)
	file_type = file.headers["content-type"]
	contents = await file.read()
	try:
		headers = {
			"content-Type":"multipart/form-data"
		}
		# save pig to S3
		upload_url = s3.generate_presigned_url("put_object", Params={"Bucket": bucket_name, "Key":file_name},ExpiresIn=60)
		response = requests.put(upload_url, data=contents, headers = headers)
		
		#get cdn_url
		cloudfront_utl = CLOUDFRONT_DOMAIN + '/' + file_name
		print(cloudfront_utl)
		
		#save to DB
		data = insert_message(text, cloudfront_utl)
		return JSONResponse(content={"ok": True, "data": data}, status_code=200)
	except Exception as e:
		print(f"{e}")
		return str(e)

@app.get("/api/messages")
async def return_messages():
	try:
		raw_data = get_all_message()
		data_for_return = []
		for data in raw_data:
			id, message, image_cdn_url = data.values()
			data_dict = {}
			data_dict["id"] = id
			data_dict["text"] = message
			data_dict["image_cdn_url"] = image_cdn_url
			data_for_return.append(data_dict)
		data_count = len(data_for_return)
		return JSONResponse(content={"total":data_count,"data": data_for_return}, status_code=200)
	except Exception as e:
		print(f"{e}")
		return str(e)

	
