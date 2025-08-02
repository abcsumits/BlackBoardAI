import os
import random
import uuid
import hashlib
from datetime import datetime
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Base path for hash-based storage
def sha256_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

class AI:
    def __init__(self, session_id: str, api_count: int = 11):
        self.session_id = session_id
        self.PROMPT_BPATH = f"./prompts/{session_id}"
        self.RESPONSE_BPATH = f"./responses/{session_id}"
        self.api_count = api_count
        os.makedirs(self.PROMPT_BPATH, exist_ok=True)
        os.makedirs(self.RESPONSE_BPATH, exist_ok=True)

    def send_prompt(self, prompt: str, depth: int = 10) -> str:
        if depth <= 0:
            print("[ERROR] Maximum recursion depth reached.")
            return ""
        try:
            hash_name = sha256_hash(prompt)
            prompt_path = os.path.join(self.PROMPT_BPATH, f"{hash_name}.txt")
            response_path = os.path.join(self.RESPONSE_BPATH, f"{hash_name}.txt")

            # Check if response already exists
            if os.path.exists(response_path):
                print(f"[INFO] Cached response exists. Reading from {response_path}")
                with open(response_path, "r", encoding="utf-8") as f:
                    return f.read()

            print("[INFO] Generating response for prompt...")

            # Save prompt
            with open(prompt_path, "w", encoding="utf-8") as f:
                f.write(prompt)
            print(f"[INFO] Prompt saved to {prompt_path}")

            # Load API key
            api_key = os.getenv("API_KEY" + str(random.randint(1, self.api_count)))
            client = genai.Client(api_key=api_key)

            # Generate response
            response = client.models.generate_content(
                model="gemini-2.5-pro", contents=prompt,
                config=genai.types.GenerateContentConfig(
                    thinking_config=genai.types.ThinkingConfig(thinking_budget=24576)
                )
            )

            # Save response
            with open(response_path, "w", encoding="utf-8") as f:
                f.write(response.text)
            print(f"[INFO] Response saved to {response_path}")

            if not response.text:
                print("[WARNING] Empty response received, retrying...")
                return self.send_prompt(prompt, depth - 1)
            return response.text

        except Exception as e:
            print(f"[ERROR] API call failed: {e}")
            print("[INFO] Retrying...")
            return self.send_prompt(prompt, depth - 1)