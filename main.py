import argparse
import uuid
from ai import AI
from writer import Writer

# Set up argument parser
parser = argparse.ArgumentParser(description="Generate video script from prompt")
parser.add_argument('--input_prompt', type=str, required=True, help='Prompt for video content')

args = parser.parse_args()
input_prompt = args.input_prompt
uid = str(uuid.uuid4())

print("Starting video generation...")
ai = AI(uid)
writer = Writer(ai, input_prompt, uid)
writer.create_video()
