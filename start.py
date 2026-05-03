from openAIapi import openapi
from dialogue_writer import script
from titlendecription import title,description
from youtube_uploader import upload_video
from delete_file import delete_file
import threading
import time
from code_writer import writer
from add_audio import generate_audio
def start(input_prompt,uid="",reel=False,regenerate=False):
    if reel==True:
        story=openapi('strictly answer to this query in a way that reel (should be short crisp about less than 2 mintues) can be created using it:'+input_prompt)
        des=description(story)
        tit=title(story)
        writer(des,"description.txt")
        writer(tit,"title.txt")
        script(story+" do not make more than 20 segments make sure script is less than of 2.5 mins, strictly it is for reels and shorts ",input_prompt,uid,regenerate,1080,1920)
        if regenerate==True:
            return
        link=upload_video(des,tit,uid)
        
        return link

        
    else:
        print(input_prompt,uid)
        story=openapi('strictly answer to this query in a way that youtube video (channel name is blackboardAI) can be created using it:'+input_prompt)
        des=description(story)
        tit=title(story)
        link=None
        writer(des,"description.txt")
        writer(tit,"title.txt")
        script(story,input_prompt,uid,regenerate)
        if regenerate==False:
            link=upload_video(des,tit,uid)
            time.sleep(60)

        return link
