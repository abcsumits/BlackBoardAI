from moviepy.editor import (
    VideoFileClip, AudioFileClip, AudioClip,
    concatenate_videoclips, concatenate_audioclips,
    vfx, CompositeAudioClip
)

# Load video and audio files
video = VideoFileClip("1.mp4")
audio = AudioFileClip("1.mp3")

# Get durations
video_duration = video.duration
audio_duration = audio.duration

# Calculate speed factor to match audio length
speed_factor = video_duration / audio_duration

# Adjust video speed to match audio duration
adjusted_video = video.fx(vfx.speedx, factor=1/speed_factor)

# Set the new audio
final_video = adjusted_video.set_audio(audio)

# Export the final result
final_video.write_videofile("output.mp4", codec="libx264", audio_codec="aac")