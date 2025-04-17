from manim_prompt import m_prompt 
from code_writer import writer
from speech import texttospeech
from video_editor import combine_audio
import subprocess
import json
import re
from delete_file import delete_file , move_file
from openAIapi import openapi
def write_manim(task,frame_no,text,uid,error='',cnt=2):
    if cnt==0:
        return
    print("code no.",frame_no)
    frame_no+=uid
    file_name=frame_no+'.py'
    code_str=openapi(m_prompt(task,text,error))
    code_str = re.sub(r'^```(?:\w+)?\n', '', code_str).strip()
    code_str = re.sub(r'^python(?:\w+)?\n', '', code_str).strip()
    code_str = re.sub(r'^manim(?:\w+)?\n', '', code_str).strip()
    if code_str.endswith("```"):
        code_str = code_str[:-3].strip()
    print('some cleaning=============================',code_str)
    try:
        writer(code_str,file_name)
        subprocess.run('manim -qh '+file_name+' Frame', shell=True, text=True, capture_output=True,timeout=600 )
        delete_file(file_name)
        print("created filex"+file_name)
        if move_file('./media/videos/'+frame_no+'/1080p60/'+'Frame'+'.mp4','./'+frame_no+'.mp4'):
            delete_file('./media/videos/'+frame_no)
            write_manim(task,frame_no,text,"",'''Strictly fix theError: Your last  code generated multiple video , only single video will get processed '''+'''Your last Code : '''+code_str,cnt-1)
        else:
            texttospeech(text,frame_no+".mp3")
            combine_audio(frame_no)
            delete_file(frame_no+'.mp4')
            delete_file(frame_no+'.mp3')
            delete_file('./media/videos/'+frame_no)
            return True

    except subprocess.CalledProcessError as e:
        delete_file(file_name)
        delete_file('./media/videos/'+frame_no)
        write_manim(task,frame_no,text,"",'''Your last CODE  generated ERROR , DONOT REPEAT SAME MISTAKE AGAIN{Error: '''+e.stderr+"}"+"Strictly make the code error less",cnt-1)
        return
    except Exception as e:
        delete_file(file_name)
        delete_file('./media/videos/'+frame_no)
        write_manim(task,frame_no,text,"",'''Your last CODE  generated ERROR , DONOT REPEAT SAME MISTAKE AGAIN{Error: '''+str(e)+"}",cnt-1)
        return