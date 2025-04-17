from google import genai
import os
import random

from dotenv import load_dotenv
load_dotenv()
def openapi(prompt):
    try:
        print('inside llm ')
        client = genai.Client(api_key=os.getenv("API_KEY"+str(random.randint(1,10))))
        response = client.models.generate_content(
            model="gemini-2.5-pro-exp-03-25", contents=prompt)
        print(response)
        if response.text:
            return response.text
        else:
            return openapi(prompt)
    except Exception as e:
        print('API error arahi hai',e)
        return openapi(prompt)
