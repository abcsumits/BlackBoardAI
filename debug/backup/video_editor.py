from moviepy.editor import (
    VideoFileClip, AudioFileClip, AudioClip,
    concatenate_videoclips, concatenate_audioclips,
    vfx, CompositeAudioClip
)
from common import delete_file
from moviepy.audio.fx.all import audio_loop
import os
import re

os.makedirs("output", exist_ok=True)

def combine_audio(video_path, audio_path, output_path):
    """
    Combines the given video and audio into a single video file, syncing their durations.
    If audio is longer, the last video frame is frozen to match. If audio is shorter, silence is added.
    """

    try:
        print(f"[INFO] Loading video from {video_path}")
        video = VideoFileClip(video_path)
        
        print(f"[INFO] Loading audio from {audio_path}")
        audio = AudioFileClip(audio_path)

        # Adjust video speed if needed
        video = video.fx(vfx.speedx, video.duration / audio.duration)

        # Extend video to match longer audio
        if audio.duration > video.duration:
            print("[INFO] Audio is longer than video, extending video with last frame.")
            freeze_duration = audio.duration - video.duration
            last_frame = video.to_ImageClip(duration=freeze_duration)
            extended_video = concatenate_videoclips([video, last_frame])
        else:
            extended_video = video

        # Add silence to match video duration if needed
        if audio.duration < extended_video.duration:
            print("[INFO] Audio is shorter than video, appending silence.")
            silence_duration = extended_video.duration - audio.duration
            silent_audio = AudioClip(lambda t: 0, duration=silence_duration, fps=audio.fps)
            audio = concatenate_audioclips([audio, silent_audio])

        # Combine video and final audio
        final_video = extended_video.set_audio(audio)
        print(f"[INFO] Writing combined video to {output_path}")
        final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

        return output_path

    except Exception as e:
        regex = r"(\w*)\.mp3"
        print(f"[ERROR] Failed to combine audio and video for frame {re.search(regex, video_path).group(1)}: {e}")
        return None


def concatenate_frames(total_frames, uid):
    """
    Concatenates all individual video clips into one final video.
    """
    print("[INFO] Starting final video creation...")
    video_files = []

    for i in range(1, total_frames + 1):
        combined_path = f"./temp/combined/{i}_{uid}.mp4"
        try:
            print(f"[INFO] Loading video clip {combined_path}")
            clip = VideoFileClip(combined_path)
            video_files.append(clip)
        except Exception as e:
            print(f"[WARNING] Skipping missing or invalid video: {combined_path} ({e})")

    if not video_files:
        print("[ERROR] No valid video clips found. Cannot create final video.")
        return

    try:
        final_output = f"./output/{uid}.mp4"
        print(f"[INFO] Concatenating {len(video_files)} clips into final video...")
        final_video = concatenate_videoclips(video_files, method="compose")
        
        print(f"[INFO] Writing final video to {final_output}")
        final_video.write_videofile(final_output, codec="libx264", audio_codec="aac")

        # Optionally delete intermediate files
        # for i in range(1, total_frames + 1):
        #     delete_file(f"combined{i}{uid}.mp4")

    except Exception as e:
        print(f"[ERROR] Failed to create final video: {e}")