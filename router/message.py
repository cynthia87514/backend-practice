from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from model.message import MessageModel
from schema.message import MessageRender
import boto3
from typing import List
import os
from dotenv import load_dotenv

MessageRouter = APIRouter(
    prefix = "/api",
    tags = ["Message"]
)

load_dotenv()

# AWS S3 Configuration
s3_client = boto3.client(
    "s3",
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
)
BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
CLOUDFRONT_DOMAIN = os.getenv("CLOUDFRONT_DOMAIN")

@MessageRouter.post("/upload")
async def upload_message(message: str = Form(...), image: UploadFile = File(...)):
    try:
        # Upload image to S3
        s3_key = f"images/{image.filename}"
        s3_client.upload_fileobj(image.file, BUCKET_NAME, s3_key)
        
        # Generate CloudFront URL
        image_url = f"{CLOUDFRONT_DOMAIN}/{s3_key}"

        # Save message and image URL to RDS
        msg_model = MessageModel(message=message, image_url=image_url)
        await msg_model.save()

        return JSONResponse(content={"ok": True})
    except Exception as e:
        print(e)
        return JSONResponse(content={"error": True}, status_code=500)

@MessageRouter.get("/messages", response_model=List[MessageRender])
async def get_messages():
    messages = await MessageModel.get_messages()
    return messages
