import os
import random
from datetime import datetime
from dotenv import load_dotenv
from google import genai
import uuid

load_dotenv()

# Ensure directories exist
os.makedirs("prompts", exist_ok=True)
os.makedirs("responses", exist_ok=True)

import os
PROMPT_BPATH = './prompts/4a652610-3816-4d83-a53b-1a06dceb023f'
RESPONSE_BPATH = './responses/4a652610-3816-4d83-a53b-1a06dceb023f'

files = os.listdir(RESPONSE_BPATH)
files.sort()

class AI:
    def __init__(self, session_id=str(uuid.uuid4())):
        self.session_id: str = session_id
        self.count: int = 0

    def __get_next_file(self):
        try:
            file = files.pop(self.count)
        except IndexError:
            print("[INFO] No more files to process.")
            exit(1)
        return file
    
    def send_prompt1(self, prompt: str):
        filename = self.__get_next_file()
        print(f"[INFO] Using file: {filename}")
        with open(os.path.join(RESPONSE_BPATH, filename), "r", encoding="utf-8") as f:
            response = f.read()
            return response

    def send_prompt(self, prompt: str):
        try:
            print("[INFO] Generating response for prompt...")

            # Generate timestamped filenames
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            os.makedirs(f"prompts/{self.session_id}", exist_ok=True)
            os.makedirs(f"responses/{self.session_id}", exist_ok=True)
            prompt_filename = f"prompts/{self.session_id}/prompt_{timestamp}.txt"
            response_filename = f"responses/{self.session_id}/response_{timestamp}.txt"

            # Save prompt to file
            with open(prompt_filename, "w", encoding="utf-8") as f:
                f.write(prompt)
            print(f"[INFO] Prompt saved to {prompt_filename}")

            # Pick a random API key (if multiple are defined)
            api_key = os.getenv("API_KEY" + str(random.randint(1, 11)))
            client = genai.Client(api_key=api_key)

            # Make the request
            response = client.models.generate_content(
                model="gemini-2.5-pro-exp-03-25",
                contents=prompt
            )

            # Save response if available
            if response.text:
                with open(response_filename, "w", encoding="utf-8") as f:
                    f.write(response.text)
                print(f"[INFO] Response saved to {response_filename}")
                return response.text
            else:
                print("[WARNING] Empty response, retrying...")
                return self.send_prompt(prompt)

        except Exception as e:
            print(f"[ERROR] API call failed: {e}")
            print("[INFO] Retrying...")
            return self.send_prompt(prompt)