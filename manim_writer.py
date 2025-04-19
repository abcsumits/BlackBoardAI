from prompt import manim_code_prompt 
from common import write_file,  delete_file, move_file
from speech import texttospeech
from video_editor import combine_audio
import subprocess
import json
import re
import os
from ai import AI

# Ensure directories exist
os.makedirs("temp/videos", exist_ok=True)
os.makedirs("temp/audios", exist_ok=True)
os.makedirs("temp/combined", exist_ok=True)

def write_manim(ai: AI, task, frame_no, text, uid, error='', cnt = 2):
    if cnt == 0:
        return
    print("INFO: Generating code for frame", frame_no)
    frame_no = f"{frame_no}_{uid}"
    file_name=f"./temp/{frame_no}.py"
    code_str=ai.send_prompt(manim_code_prompt(task,text,error))
    print("INFO: Response received from AI for code generation")
    print("INFO: Cleaning code")
    code_str = re.sub(r'^```(?:\w+)?\n', '', code_str).strip()
    code_str = re.sub(r'^python(?:\w+)?\n', '', code_str).strip()
    code_str = re.sub(r'^manim(?:\w+)?\n', '', code_str).strip()
    if code_str.endswith("```"):
        code_str = code_str[:-3].strip()
    print("INFO: Code cleaned. Moving to file creation")
    try:
        print(f"INFO: Writing the generated code to {file_name}")
        write_file(code_str, file_name)
        print("INFO: Executing the manim code in the file", file_name)
        # Execute the manim command
        subprocess.run('manim -qh '+file_name+' Frame', shell=True, text=True, capture_output=True,timeout=600 )
        delete_file(file_name)
        print("INFO: Manim code executed successfully")
        if not move_file('./media/videos/'+frame_no+'/1080p60/'+'Frame'+'.mp4', './temp/videos/'+frame_no+'.mp4'):
            print("WARNING: Multiple videos generated, only one needs to be processed. Deleting the extra video files")
            delete_file('./media/videos/'+frame_no)
            print("INFO: Sending for regenerating the manim code")
            write_manim(task,frame_no,text,"",'''Strictly fix theError: Your last  code generated multiple video , only single video will get processed '''+'''Your last Code : '''+code_str,cnt-1)
        else:
            print("SUCCESS: Manim code executed successfully in a single video")
            texttospeech(text,f"temp/audios/{frame_no}.mp3")
            print("INFO: Audio generated successfully")
            print("INFO: Combining audio and video")
            combine_audio(f'./temp/videos/{frame_no}.mp4', './temp/audios/'+frame_no+'.mp3', './temp/combined/'+frame_no+'.mp4')
            print("INFO: Audio and video combined successfully")
            # print("INFO: Deleting the extra video files")
            # delete_file('./temp/videos/'+frame_no+'.mp4')
            # delete_file('./temp/audios/'+frame_no+'.mp3')
            # delete_file('./media/videos/'+frame_no)
            return True

    except subprocess.CalledProcessError as e:
        print("ERROR: Manim code execution failed")
        print("INFO: Error message:", e.stderr)
        print("INFO: Sending for regenerating the manim code")
        delete_file(file_name)
        delete_file('./media/videos/'+frame_no)
        write_manim(ai, task,frame_no,text,"",'''Your last CODE  generated ERROR , DONOT REPEAT SAME MISTAKE AGAIN{Error: '''+e.stderr+"}"+"Strictly make the code error less",cnt-1)
        return
    except Exception as e:
        print("ERROR: Manim code execution failed")
        print("INFO: Error message:", str(e))
        print("INFO: Sending for regenerating the manim code")
        print("INFO: Deleting the extra video files")
        delete_file(file_name)
        delete_file('./media/videos/'+frame_no)
        write_manim(ai, task,frame_no,text,"",'''Your last CODE  generated ERROR , DONOT REPEAT SAME MISTAKE AGAIN{Error: '''+str(e)+"}",cnt-1)
        return