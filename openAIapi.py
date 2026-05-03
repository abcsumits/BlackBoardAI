from google import genai
import os
import random
import time
from google.genai import types
from dotenv import load_dotenv
load_dotenv()
from google import genai
from google.genai import types
import os
import random
import time
from dotenv import load_dotenv

load_dotenv()

def openapi(prompt):
    try:
        print('inside llm ')
        time.sleep(random.randint(1,3))
        client = genai.Client(api_key=os.getenv("API_KEY"+str(random.randint(1,22))))
        response = client.models.generate_content(
            model="gemini-3-flash-preview", contents=prompt,
        config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(
                    # Options in 2026: 'high', 'medium', 'low'
                    # 'high' is best for competitive programming and architecture logic.
                    thinking_level="high" ))
               
           
        
        )
        print(response)
        if response.text:
            return response.text
        else:
            
            return openapi(prompt)
            
    except Exception as e:
        print('API error arahi hai',e)
        time.sleep(random.randint(1,10))
        return openapi(prompt)