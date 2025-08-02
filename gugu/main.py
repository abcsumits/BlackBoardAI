import argparse
import os
from ai import AI
from writer import Writer
from dotenv import load_dotenv
from gugu.upload_script import ensure_bucket_exists, upload_video_to_gcs

# Load environment variables
load_dotenv()

input_prompt = os.getenv("PROMPT")
uid = os.getenv("TASK_ID")
print(f"Prompt: {input_prompt}")
print(f"Task ID: {uid}")
if not input_prompt or not uid:
    raise ValueError("❌ Missing required environment variables: PROMPT or TASK_ID.")

print("Starting video generation...")
# ai = AI(uid)
# writer = Writer(ai, input_prompt, uid)
# writer.create_video()

# Load variables from .env
load_dotenv()

# Set credentials path
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

bucket_name = os.getenv("GCS_BUCKET_NAME")
video_path = f'./output/RESULT_{os.getenv("TASK_ID")}.mp4'
destination = f'{os.getenv("USER_ID")}/{os.getenv("TASK_ID")}.mp4'

if not all([bucket_name, video_path, destination]):
    raise ValueError("❌ Missing one or more required variables in .env file.")

ensure_bucket_exists(bucket_name)
upload_video_to_gcs(bucket_name, video_path, destination)