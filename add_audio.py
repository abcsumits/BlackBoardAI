from video_editor import combine_audio
from speech import texttospeech
from delete_file import delete_file
def generate_audio(frames,uid):
    print(len(frames))
    for i in range(1,len(frames)+1):
            frame_no=str(i)+uid
            text=frames["segment"+str(i)][1]
            texttospeech(text,frame_no+".mp3")
            temp=combine_audio(frame_no)
            if not temp:
                return False
            delete_file(frame_no+'.mp4')
            delete_file(frame_no+'.mp3')
    return True
    #create_video(len(frames),uid)