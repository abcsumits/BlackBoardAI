import os
from dotenv import load_dotenv
from google.api_core.exceptions import NotFound, Conflict
from google.cloud import storage

def ensure_bucket_exists(bucket_name, location="US"):
    """
    Checks if a GCS bucket exists, and creates it if not.
    """
    client = storage.Client()
    try:
        client.get_bucket(bucket_name)
        print(f"✅ Bucket '{bucket_name}' already exists.")
    except NotFound:
        print(f"⚠️ Bucket '{bucket_name}' not found. Creating...")
        bucket = client.bucket(bucket_name)
        bucket.location = location
        try:
            client.create_bucket(bucket)
            print(f"✅ Created bucket '{bucket_name}' in location '{location}'.")
        except Conflict:
            print(f"❌ Failed to create bucket. Bucket name '{bucket_name}' may already be in use globally.")
            raise

def upload_video_to_gcs(bucket_name, source_file_path, destination_blob_name):
    """
    Uploads a file to a Google Cloud Storage bucket.
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_path)
    print(f"✅ Uploaded '{source_file_path}' to 'gs://{bucket_name}/{destination_blob_name}'")

def main():
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

if __name__ == "__main__":
    main()