import subprocess
import json
import os
from math import ceil

def get_media_duration(file_path):
    """Get the duration of a media file using ffprobe."""
    cmd = [
        'ffprobe', 
        '-v', 'error', 
        '-select_streams', 'a:0', 
        '-show_entries', 'format=duration', 
        '-of', 'json', 
        file_path
    ]
    
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        data = json.loads(output)
        return float(data['format']['duration'])
    except:
        # If there's no audio stream, try getting the video duration
        cmd = [
            'ffprobe', 
            '-v', 'error', 
            '-select_streams', 'v:0', 
            '-show_entries', 'format=duration', 
            '-of', 'json', 
            file_path
        ]
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        data = json.loads(output)
        return float(data['format']['duration'])

def merge_video_audio(video_path, audio_path, output_path):
    """
    Merge a video with an audio file using the following synchronization logic:
    - Adjust video speed to match audio when possible (max 2x speed)
    - Freeze last frame if audio is longer than video
    - Add silent audio if video is longer than audio
    
    Args:
        video_path (str): Path to the video file
        audio_path (str): Path to the audio file
        output_path (str): Path for the output file
    """
    video_duration = get_media_duration(video_path)
    audio_duration = get_media_duration(audio_path)
    
    print(f"Video duration: {video_duration} seconds")
    print(f"Audio duration: {audio_duration} seconds")
    
    # Create a temporary directory for intermediate files
    temp_dir = "temp_merge"
    os.makedirs(temp_dir, exist_ok=True)
    
    # Case 1: Video and audio are roughly the same length (within 0.5 seconds)
    if abs(video_duration - audio_duration) < 0.5:
        print("Case 1: Video and audio are about the same length. Simple merge.")
        cmd = [
            'ffmpeg', '-y',
            '-i', video_path,
            '-i', audio_path,
            '-map', '0:v',
            '-map', '1:a',
            '-c:v', 'copy',
            '-shortest',
            output_path
        ]
        subprocess.run(cmd)
    
    # Case 2: Audio is shorter than video
    elif audio_duration < video_duration:
        print("Case 2: Audio is shorter than video. Adding silent audio.")
        # Create silent audio for the remaining duration
        silence_duration = ceil(video_duration - audio_duration)
        silence_file = os.path.join(temp_dir, "silence.mp3")
        
        cmd = [
            'ffmpeg', '-y',
            '-f', 'lavfi',
            '-i', f'anullsrc=r=44100:cl=stereo:d={silence_duration}',
            silence_file
        ]
        subprocess.run(cmd)
        
        # Concatenate original audio with silence
        concat_audio = os.path.join(temp_dir, "extended_audio.mp3")
        concat_list = os.path.join(temp_dir, "concat_list.txt")
        
        with open(concat_list, 'w') as f:
            f.write(f"file '{os.path.abspath(audio_path)}'\n")
            f.write(f"file '{os.path.abspath(silence_file)}'\n")
        
        cmd = [
            'ffmpeg', '-y',
            '-f', 'concat',
            '-safe', '0',
            '-i', concat_list,
            '-c', 'copy',
            concat_audio
        ]
        subprocess.run(cmd)
        
        # Merge video with extended audio
        cmd = [
            'ffmpeg', '-y',
            '-i', video_path,
            '-i', concat_audio,
            '-map', '0:v',
            '-map', '1:a',
            '-c:v', 'copy',
            output_path
        ]
        subprocess.run(cmd)
    
    # Case 3: Audio is longer than video but can be matched by speed adjustment (up to 2x)
    elif video_duration * 2 >= audio_duration:
        print("Case 3: Adjusting video speed to match audio duration.")
        speed_factor = video_duration / audio_duration
        adjusted_video = os.path.join(temp_dir, "adjusted_video.mp4")
        
        # Adjust video speed
        cmd = [
            'ffmpeg', '-y',
            '-i', video_path,
            '-filter:v', f'setpts={speed_factor}*PTS',
            '-an',
            adjusted_video
        ]
        subprocess.run(cmd)
        
        # Merge adjusted video with audio
        cmd = [
            'ffmpeg', '-y',
            '-i', adjusted_video,
            '-i', audio_path,
            '-map', '0:v',
            '-map', '1:a',
            '-c:v', 'copy',
            output_path
        ]
        subprocess.run(cmd)
    
    # Case 4: Audio is much longer than video (more than 2x)
    else:
        print("Case 4: Audio is much longer than video. Freezing last frame.")
        
        # Extract the last frame from the video
        last_frame = os.path.join(temp_dir, "last_frame.png")
        cmd = [
            'ffmpeg', '-y',
            '-sseof', '-1',
            '-i', video_path,
            '-update', '1',
            '-q:v', '1',
            last_frame
        ]
        subprocess.run(cmd)
        
        # Get the remaining duration needed
        freeze_duration = audio_duration - video_duration
        
        # Create a video of the frozen last frame
        frozen_video = os.path.join(temp_dir, "frozen.mp4")
        cmd = [
            'ffmpeg', '-y',
            '-loop', '1',
            '-i', last_frame,
            '-t', str(freeze_duration),
            '-vf', 'fps=30',
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            frozen_video
        ]
        subprocess.run(cmd)
        
        # Concatenate original video with frozen frame video
        concat_list = os.path.join(temp_dir, "video_concat.txt")
        with open(concat_list, 'w') as f:
            f.write(f"file '{os.path.abspath(video_path)}'\n")
            f.write(f"file '{os.path.abspath(frozen_video)}'\n")
        
        extended_video = os.path.join(temp_dir, "extended_video.mp4")
        cmd = [
            'ffmpeg', '-y',
            '-f', 'concat',
            '-safe', '0',
            '-i', concat_list,
            '-c', 'copy',
            extended_video
        ]
        subprocess.run(cmd)
        
        # Merge extended video with audio
        cmd = [
            'ffmpeg', '-y',
            '-i', extended_video,
            '-i', audio_path,
            '-map', '0:v',
            '-map', '1:a',
            '-c:v', 'copy',
            output_path
        ]
        subprocess.run(cmd)
    
    print(f"Merge complete! Output saved to: {output_path}")
    
    # Clean up temporary files
    import shutil
    shutil.rmtree(temp_dir)

if __name__ == "__main__":
    # Example usage
    merge_video_audio("1.mp4", "1.mp3", "output.mp4")