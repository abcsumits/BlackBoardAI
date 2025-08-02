import os
import subprocess
from dotenv import dotenv_values
from google.oauth2 import service_account
from google.auth.transport.requests import Request

# === CONFIGURATION ===
SERVICE_ACCOUNT_FILE = 'jobrun_key.json'     # Path to service account key
ENV_FILE = '.env'                                  # Your .env file with vars
PROJECT_ID = 'fleet-pillar-451011-m9'                          # Your GCP project ID
REGION = 'us-central1'
JOB_NAME = 'generate-video-job'
IMAGE_URL = f'gcr.io/{PROJECT_ID}/video-generator-ai:latest'
SERVICE_ACCOUNT_EMAIL = 'runjob@{PROJECT_ID}.iam.gserviceaccount.com'

# === STEP 1: AUTHENTICATE WITH GOOGLE CLOUD ===
print("🔐 Authenticating with Google Cloud...")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SERVICE_ACCOUNT_FILE

# credentials = service_account.Credentials.from_service_account_file(
#     SERVICE_ACCOUNT_FILE,
#     scopes=["https://www.googleapis.com/auth/cloud-platform"]
# )
# credentials.refresh(Request())

# === STEP 2: LOAD ENV FILE ===
print(f"📦 Loading environment variables from {ENV_FILE}...")
env_vars = dotenv_values(ENV_FILE)  # {'KEY': 'VALUE'}

if not env_vars:
    raise ValueError(f"No environment variables found in {ENV_FILE}")

env_string = ",".join(f"{k}={v}" for k, v in env_vars.items())

# === STEP 3: CREATE THE JOB (if it doesn't exist) ===
print("⚙️ Creating Cloud Run Job...")
try:
    subprocess.run([
        "gcloud", "run", "jobs", "create", JOB_NAME,
        "--image", IMAGE_URL,
        "--region", REGION,
        "--project", PROJECT_ID,
        "--service-account", SERVICE_ACCOUNT_EMAIL,
        "--max-retries", "3",
        "--task-timeout", "3600s",
        "--memory", "16Gi",
        "--cpu", "8",
        "--set-env-vars", env_string
    ], check=True)
    print("✅ Job created.")
except subprocess.CalledProcessError as e:
    print(f"⚠️ Job may already exist. Skipping create step. ({e})")

# === STEP 4: RUN THE JOB ===
print("🚀 Running the Cloud Run Job...")
try:
    subprocess.run([
        "gcloud", "run", "jobs", "execute", JOB_NAME,
        "--region", REGION,
        "--project", PROJECT_ID,
        "--wait",
        "--update-env-vars", env_string
    ], check=True)
    print("✅ Job ran successfully.")
except subprocess.CalledProcessError as e:
    print(f"❌ Job execution failed: {e}")