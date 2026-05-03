from svg_prompt import svg_prompt
from code_writer import writer
from openAIapi import openapi
from svgtopng import svg_to_png
from image_to_video import image_to_video

def svg_video(task,frame_no,text,uid,width=1920, height=1080,image={}):
    frame_no+=uid
    file_name=frame_no+'.svg'
    prompt=svg_prompt(task,text,f"{width} X {height}",image)
    code_str=openapi(prompt)
    if code_str.startswith('```'):
        code_str = code_str[3:].strip()
    if code_str.startswith('svg') or code_str.startswith('xml'):
        code_str = code_str[3:].strip()
    if code_str.startswith('"'):
        code_str = code_str[1:].strip()
    if code_str.endswith("```"):
        code_str = code_str[:-3].strip()
    if code_str.endswith('"'):
        code_str = code_str[:-1].strip()
    try :
        writer(code_str,file_name)
        svg_to_png(file_name,frame_no+'.png',width,height)
        
        image_to_video(frame_no+'.png',frame_no+'.mp4',4)
        
        

    except Exception as e:
        
        svg_video(task,frame_no,text,uid,width,height,image)
    