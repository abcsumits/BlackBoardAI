from svg_prompt import svg_prompt
from code_writer import writer
from openAIapi import openapi
from svgtopng import svg_to_png
from image_to_video import image_to_video
from speech import texttospeech
from video_editor import combine_audio
from delete_file import delete_file
from video_editor import get_duration
def svg_video(task,frame_no,text,uid):
    frame_no+=uid
    file_name=frame_no+'.svg'
    prompt=svg_prompt(task,text)
    code_str=openapi(prompt)
    if code_str.startswith('```'):
        code_str = code_str[3:].strip()
    if code_str.startswith('svg'):
        code_str = code_str[3:].strip()
    if code_str.startswith('"'):
        code_str = code_str[1:].strip()
    if code_str.endswith("```"):
        code_str = code_str[:-3].strip()
    if code_str.endswith('"'):
        code_str = code_str[:-1].strip()
    try :
        writer(code_str,file_name)
        svg_to_png(file_name,frame_no+'.png')
        texttospeech(text,frame_no+".mp3")
        image_to_video(frame_no+'.png',frame_no+'.mp4',get_duration(frame_no+'.mp3')+1)
        combine_audio(frame_no)
        delete_file(frame_no+'.mp4')
        delete_file(frame_no+'.mp3')

    except Exception as e:
        svg_video(task,frame_no,text,uid="")
    