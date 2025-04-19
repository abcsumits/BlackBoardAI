from moviepy.editor import (
    VideoFileClip, AudioFileClip, AudioClip,
    concatenate_videoclips, concatenate_audioclips,
    vfx, CompositeAudioClip
)
from common import delete_file
from moviepy.audio.fx.all import audio_loop
import numpy as np
import os
import re

def combine_audio(num):
    video_path  = f"{num}.mp4"
    audio_path  = f"{num}.mp3"
    output_path = f"combined{num}.mp4"
    
    video = VideoFileClip(video_path, audio=False)
    audio = AudioFileClip(audio_path)
    silent_audio = AudioClip(
            make_frame=lambda t: np.zeros(audio.nchannels),
            duration=0.04,
            fps=audio.fps
        )
    audio = concatenate_audioclips([audio, silent_audio])
    # Adjust video speed to match audio duration
    print(video.duration)
    print(audio.duration)
    speed_factor = min((video.duration/audio.duration)+0.04,2)
    video = video.fx(vfx.speedx, speed_factor)
    print(video.duration)
    # Ensure duration match
    if audio.duration > video.duration:
        freeze_duration = audio.duration - video.duration+0.04
        print("freeze_duration:",freeze_duration)
        last_frame_time = max(0, video.duration - 0.04)
        print("last_frame_time:",last_frame_time)
        last_frame = video.to_ImageClip(t=last_frame_time).set_duration(freeze_duration).without_audio()
        print("last frame created successfully")
        video = concatenate_videoclips([video, last_frame], method="compose")
    print(video.duration)
    if audio.duration < video.duration:
        silence_duration = video.duration - audio.duration-0.04
        silent_audio = AudioClip(
            make_frame=lambda t: np.zeros(audio.nchannels),
            duration=silence_duration,
            fps=audio.fps
        )
        audio = concatenate_audioclips([audio, silent_audio])
    print(audio.duration,video.duration)
    final_video = video.set_audio(audio).subclip(0,  audio.duration)
    print("final video duration",final_video.duration)
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac",ffmpeg_params=["-shortest"])
    
    return output_path

combine_audio(1)