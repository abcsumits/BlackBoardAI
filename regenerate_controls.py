from manim_writer import write_manim
import json

# Replace 'data.txt' with the actual path to your file
file_path = 'dialogue.txt'

try:
    # Open the file in read mode
    with open(file_path, 'r', encoding='utf-8') as file:
        # json.load() parses the file content and converts it directly into a dictionary
        my_dictionary = json.load(file)

    

except FileNotFoundError:
    print(f"Error: The file {file_path} was not found.")
except json.JSONDecodeError:
    print("Error: The file does not contain valid JSON format.")
dialuge=my_dictionary

import threading
from video_editor import create_video
from add_audio import generate_audio
uuid=""

def regenerate_frame(frame:list,reel=False):
    if reel:
        height=1920
        width=1080
    else:
        width=1920
        height=1080
    threads=[]
    for i in frame:
        threads.append(threading.Thread(target=write_manim, args=(dialuge["segment"+str(i)][0],str(i),dialuge["segment"+str(i)][1],uuid,width,height)))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
from youtube_uploader import upload_video
def upload():
    try:
        generate_audio(dialuge,uuid)
        create_video(len(dialuge),uuid)
    except Exception as e:
        print(e)
    
    file=open("description.txt","r")

    des=file.read()
    file.close()
    file=open("title.txt","r")
    title=file.read()   
    file.close()
    try:
        upload_video(des,title,uuid)
    except Exception as e:
        print(e)
