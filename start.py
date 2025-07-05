from openAIapi import openapi
from dialogue_writer import script
from titlendecription import title,description
from youtube_uploader import upload_video
from delete_file import delete_file
import threading
import time
def start(input_prompt,uid=""):
    print(input_prompt,uid)
    story=openapi('strictly answer to this query in a way that youtube video (channel name is blackboardAI) can be created using it:'+input_prompt)
    script(story,input_prompt,uid)
    des=description(story)
    tit=title(story)
    link=upload_video(des,tit,uid)
    time.sleep(60)
    delete_file('combined_video'+uid+'.mp4')
    return link
