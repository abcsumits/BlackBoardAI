from dialogue_prompt import d_prompt
from openAIapi import openapi
from manim_writer import write_manim
from video_editor import create_video
from speech import texttospeech
import json
import re
import threading
from code_writer import writer
from add_audio import generate_audio
def script(story,prompt,uid,regenerate=False,width=1920, height=1080):
    frames=openapi(d_prompt(story))
    frames = re.sub(r'^```(?:\w+)?\n', '', frames).strip()
    frames = re.sub(r'^json(?:\w+)?\n', '', frames).strip()
    if frames.endswith("```"):
        frames = frames[:-3].strip()
    
    try:
        
        frames = json.loads(frames)
        
        for i in range(1,len(frames)+1):
            if "segment"+str(i) not in frames:
                script(story,prompt,uid,regenerate)
                return
            else:
                if len(frames["segment"+str(i)])!=2:
                    script(story,prompt,uid,regenerate)
                    return
        
    except Exception as e:
        script(story+" your last response raised this execption make sure not to repeat this mistake again"+str(e),prompt,uid,regenerate)
        return
    print("passed dialouges",len(frames))
    writer(json.dumps(frames),'dialogue.txt')
    threads=[]
    for i in range(1,len(frames)+1):
        threads.append(threading.Thread(target=write_manim, args=(frames["segment"+str(i)][0]+'this are sub visuals of the following prompt:'+prompt,str(i),frames["segment"+str(i)][1],uid,width, height)))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    if regenerate==False:
        generate_audio(frames,uid)
        create_video(len(frames),uid)
        
    