from moviepy.editor import VideoFileClip, AudioFileClip,AudioClip, concatenate_videoclips, concatenate_audioclips, vfx,CompositeAudioClip
from delete_file import delete_file
from moviepy.audio.fx.all import audio_loop
def combine_audio(num):
    video_path = num + ".mp4"
    audio_path = num + ".mp3"
    output_path = 'combined' + num + ".mp4"
    
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)
    
    video=video.fx(vfx.speedx, video.duration/audio.duration)
    if audio.duration > video.duration:
        freeze_duration = audio.duration - video.duration
        last_frame = video.to_ImageClip(duration=freeze_duration)
        extended_video = concatenate_videoclips([video, last_frame])
    else:
        extended_video = video
    if audio.duration < extended_video.duration:
        silence_duration = extended_video.duration - audio.duration
        
        silent_audio = AudioClip(lambda t: 0, duration=silence_duration, fps=audio.fps)
        audio = concatenate_audioclips([audio, silent_audio])
    # Set the audio to the video
    final_video = extended_video.set_audio(audio)
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
    
    # Return the output file path so it can be loaded later
    return output_path
def create_video(Total_frames,uid):
    print("video editor me atka hua hai")
    video_files = []

    for i in range(1, Total_frames+1):
        try:
            video_files.append(VideoFileClip("combined"+str(i)+uid+".mp4"))
        except Exception as e:
            print("This frame is missing",i)
    
    final_video = concatenate_videoclips(video_files, method="compose")

    
    final_video.write_videofile("combined_video"+uid+".mp4", codec="libx264", audio_codec="aac")
    for i in range(1,Total_frames+1):
        delete_file("combined"+str(i)+uid+".mp4")
