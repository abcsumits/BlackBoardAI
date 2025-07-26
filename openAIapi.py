from google import genai
import os
import random
import time
from google.genai import types
from dotenv import load_dotenv
load_dotenv()
def openapi(prompt):
    try:
        print('inside llm ')
        client = genai.Client(api_key=os.getenv("API_KEY"+str(random.randint(1,21))))
        response = client.models.generate_content(
            model="gemini-2.5-pro", contents=prompt,
            config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=24576)
    ))
        print(response)
        if response.text:
            return response.text
        else:
            
            return openapi(prompt)
    except Exception as e:
        print('API error arahi hai',e)
        time.sleep(40)
        return openapi(prompt)
