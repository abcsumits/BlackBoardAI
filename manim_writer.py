from manim_prompt import m_prompt 
from debug_prompt import debug_prompt
from code_writer import writer
from speech import texttospeech
from video_editor import combine_audio
import subprocess
import json
import re
from delete_file import delete_file , move_file
from openAIapi import openapi
from svg_video import svg_video
def write_manim(task,frame_no,text,uid,error='',cnt=3,code=''):
    if cnt==0:
        svg_video(task,frame_no,text,uid)
        return
    print("code no.",frame_no)
    frame_no+=uid
    file_name=frame_no+'.py'
    if error=='' or cnt==1:
        code_str=openapi(m_prompt(task,text))
    
    else:
        code_str=openapi(debug_prompt(code,error))
    if code_str.startswith('```'):
        code_str = code_str[3:].strip()
    if code_str.startswith('python'):
        code_str = code_str[6:].strip()
    if code_str.startswith('manim'):
        code_str = code_str[5:].strip()
    if code_str.startswith('"'):
        code_str = code_str[1:].strip()
    if code_str.endswith("```"):
        code_str = code_str[:-3].strip()
    
    if code_str.endswith('"'):
        code_str = code_str[:-1].strip()
    print('some cleaning=============================',code_str)
    try:
        writer(code_str,file_name)
        print("runing subprocess")
        subprocess.run('manim -qh '+file_name+' Frame', shell=True, text=True, capture_output=True,timeout=100 )
        delete_file(file_name)
        print("created filex"+file_name)
        if move_file('./media/videos/'+frame_no+'/1080p60/'+'Frame'+'.mp4','./'+frame_no+'.mp4'):
            delete_file('./media/videos/'+frame_no)
            write_manim(task,frame_no,text,"","This code doesn't generated the video",cnt-1,code_str)
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
        write_manim(task,frame_no,text,"",e,cnt-1,code_str)
        return
    except Exception as e:
        delete_file(file_name)
        delete_file('./media/videos/'+frame_no)
        write_manim(task,frame_no,text,"",e,cnt-1,code_str)
        return