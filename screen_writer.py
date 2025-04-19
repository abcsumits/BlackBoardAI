from prompt import dialogue_prompt
from ai import AI
from manim_writer import write_manim
from video_editor import concatenate_frames
from speech import texttospeech
import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

MAX_WORKERS = 5

def write_video_script(story, prompt, uid, ai: AI):
    frames = ai.send_prompt(dialogue_prompt(story))
    print("INFO: Response received from AI for segments")
    frames = re.sub(r'^```(?:\w+)?\n', '', frames).strip()
    frames = re.sub(r'^json(?:\w+)?\n', '', frames).strip()
    if frames.endswith("```"):
        frames = frames[:-3].strip()
    
    try:
        frames = json.loads(frames)
        
        for i in range(1, len(frames) + 1):
            if "segment" + str(i) not in frames:
                write_video_script(story, prompt, uid, ai)
                return
            else:
                if len(frames["segment" + str(i)]) != 2:
                    write_video_script(story, prompt, uid, ai)
                    return
        
    except Exception as e:
        write_video_script(story + " your last response raised this exception make sure not to repeat this mistake again: " + str(e), prompt, uid, ai)
        return
    
    print("INFO: Number of segments received from AI:", len(frames))

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = []
        for i in range(1, len(frames) + 1):
            text = frames["segment" + str(i)][0] + ' this are sub visuals of the following prompt: ' + prompt
            image_prompt = frames["segment" + str(i)][1]
            futures.append(executor.submit(write_manim, ai, text, str(i), image_prompt, uid))
        
        for future in as_completed(futures):
            future.result()  # Wait for all to complete (and catch any exceptions)

    print("INFO: All segments processed successfully")
    print("INFO: Moving to video creation")
    concatenate_frames(len(frames), uid)