import ffmpeg
import os

def merge_video_with_audio(video_path, audio_path, output_path):
    """
    Merge a video with an audio file while adjusting the video speed to match the audio duration.
    
    Args:
        video_path (str): Path to the video file
        audio_path (str): Path to the audio file
        output_path (str): Path for the output file
    """
    # Get video information
    video_info = ffmpeg.probe(video_path)
    video_duration = float(video_info['format']['duration'])
    
    # Get audio information
    audio_info = ffmpeg.probe(audio_path)
    audio_duration = float(audio_info['format']['duration'])
    
    # Calculate speed factor
    # If audio is longer, video needs to slow down (factor < 1)
    # If audio is shorter, video needs to speed up (factor > 1)
    speed_factor = video_duration / audio_duration
    
    print(f"Video duration: {video_duration} seconds")
    print(f"Audio duration: {audio_duration} seconds")
    print(f"Speed factor: {speed_factor}")
    
    # Prepare the input video stream with adjusted speed
    input_video = ffmpeg.input(video_path)
    
    # Adjust video speed using the setpts filter
    # setpts=PTS*factor slows down when factor>1, speeds up when factor<1
    adjusted_video = input_video.video.filter('setpts', f'{1/speed_factor}*PTS')
    
    # Input audio stream
    input_audio = ffmpeg.input(audio_path).audio
    
    # Combine the adjusted video with the original audio
    # Note: Removed the codec='copy' parameter since we're filtering the video
    output = ffmpeg.output(adjusted_video, input_audio, output_path)
    
    # Run the FFmpeg command with overwrite flag
    ffmpeg.run(output, overwrite_output=True)
    
    print(f"Successfully merged video and audio to: {output_path}")

if __name__ == "__main__":
    # Example usage
    merge_video_with_audio("1.mp4", "1.mp3", "output_synced.mp4")