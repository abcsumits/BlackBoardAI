import ffmpeg

def get_duration(filename):
    """Get duration of media file in seconds."""
    probe = ffmpeg.probe(filename)
    return float(probe['format']['duration'])

# Paths to files
video_path = "1.mp4"
audio_path = "1.mp3"
output_path = "output.mp4"

# Get durations
video_duration = get_duration(video_path)
audio_duration = get_duration(audio_path)

# Calculate speed factor
speed_factor = video_duration / audio_duration

# Generate FFmpeg filter expressions
setpts_filter = f"{1/speed_factor}*PTS"  # Adjust PTS to change speed

# Build FFmpeg pipeline
(
    ffmpeg
    .input(video_path)
    .filter('setpts', setpts_filter)
    .output(audio_path, output_path, vcodec='libx264', acodec='aac', shortest=None)
    .run()
)