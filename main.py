import uuid
from ai import AI
from writer import Writer
import os
from dotenv import load_dotenv
load_dotenv()

input_prompt = os.getenv("PROMPT")
# uid = str(uuid.uuid4())
uid = '57618eb4-2497-4abb-a2c4-908e7f89569d'
print("Starting video generation...")
ai = AI(uid)
writer = Writer(ai, input_prompt, uid)
writer.create_video()
