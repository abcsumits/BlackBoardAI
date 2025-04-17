from openAIapi import openapi
from dialogue_writer import script
from titlendecription import title,description
from youtube_uploader import upload_video
from delete_file import delete_file
def start(input_prompt,uid=""):
    print(input_prompt,uid)
    story=openapi('strictly answer to this query in a way that youtube video can be created using it:'+input_prompt)
    script(story,input_prompt,uid)
    link=upload_video(description(story),title(story),uid)
    delete_file('combined_video'+uid+'.mp4')
    return link
