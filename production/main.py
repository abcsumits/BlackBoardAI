import uuid
from ai import AI
from writer import Writer
import os

input_prompt = os.getenv("PROMPT")
uid = str(uuid.uuid4())
print("Starting video generation...")
ai = AI(uid)
writer = Writer(ai, input_prompt, uid)
writer.create_video()
