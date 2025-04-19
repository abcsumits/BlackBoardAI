import argparse
import uuid
from ai import AI
from screen_writer import write_video_script

# Set up argument parser
parser = argparse.ArgumentParser(description="Generate video script from prompt")
parser.add_argument('--input_prompt', type=str, required=True, help='Prompt for video content')

args = parser.parse_args()
input_prompt = args.input_prompt
uid = str(uuid.uuid4())

print("Starting video generation...")
ai = AI(uid)
story = ai.send_prompt(f'strictly answer to this query in a way that youtube video can be created using it: {input_prompt}')
write_video_script(story, input_prompt, uid, ai)