import ffmpeg
import os
import math
import subprocess
import json
from tqdm import tqdm
import time

def get_media_duration(file_path):
    """Get the duration of a media file using ffprobe."""
    try:
        result = subprocess.run(
            [
                'ffprobe', 
                '-v', 'error', 
                '-show_entries', 'format=duration', 
                '-of', 'json', 
                file_path
            ],
            capture_output=True,
            text=True
        )
        data = json.loads(result.stdout)
        return float(data['format']['duration'])
    except Exception as e:
        raise Exception(f"Error getting duration for {file_path}: {str(e)}")

def run_ffmpeg_with_progress(args, desc="Processing", total_duration=None):
    """Run ffmpeg command with tqdm progress bar."""
    process = subprocess.Popen(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )
    
    # Set up progress bar
    pbar = tqdm(total=100, desc=desc)
    
    # Initialize progress tracking
    progress = 0
    start_time = time.time()
    
    # Process ffmpeg output
    for line in process.stderr:
        # Look for time progress in ffmpeg output
        if "time=" in line and total_duration:
            try:
                # Extract time
                time_str = line.split("time=")[1].split()[0]
                # Convert to seconds
                h, m, s = time_str.split(':')
                current_time = int(h) * 3600 + int(m) * 60 + float(s)
                # Calculate percentage
                new_progress = min(int((current_time / total_duration) * 100), 100)
                
                # Update progress bar only when there's an actual change
                if new_progress > progress:
                    pbar.update(new_progress - progress)
                    progress = new_progress
            except:
                pass
    
    # Close the progress bar
    pbar.close()
    
    # Wait for process to complete
    process.wait()
    
    # Check if process completed successfully
    if process.returncode != 0:
        raise Exception(f"FFmpeg process failed with return code {process.returncode}")

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
    # Get video and audio duration
    video_duration = get_media_duration(video_path)
    audio_duration = get_media_duration(audio_path)
    
    print(f"Video duration: {video_duration:.2f}s, Audio duration: {audio_duration:.2f}s")
    
    # Create temp directory if it doesn't exist
    temp_dir = os.path.join(os.path.dirname(output_path), 'temp')
    os.makedirs(temp_dir, exist_ok=True)
    
    # Case 1: Audio and video durations are nearly the same (within 0.5 second)
    if abs(video_duration - audio_duration) < 0.5:
        print("Simple merge: Audio and video durations are nearly the same")
        cmd = [
            'ffmpeg', '-y', '-v', 'error',
            '-i', video_path,
            '-i', audio_path,
            '-map', '0:v', '-map', '1:a',
            '-c:v', 'copy', '-c:a', 'aac',
            output_path
        ]
        run_ffmpeg_with_progress(cmd, "Merging video and audio", video_duration)
    
    # Case 2: Audio is shorter than video - speed up video if possible, otherwise add silence
    elif audio_duration < video_duration:
        speed_ratio = video_duration / audio_duration
        
        if speed_ratio <= 2.0:  # Can adjust speed (max 2x)
            print(f"Speeding up video by factor of {speed_ratio:.2f} to match audio")
            filter_complex = f"[0:v]setpts={1/speed_ratio}*PTS[v]"
            cmd = [
                'ffmpeg', '-y', '-v', 'error',
                '-i', video_path,
                '-i', audio_path,
                '-filter_complex', filter_complex,
                '-map', '[v]', '-map', '1:a',
                '-c:v', 'libx264', '-c:a', 'aac',
                output_path
            ]
            run_ffmpeg_with_progress(cmd, "Speeding up video and merging", audio_duration)
        
        else:  # Video is much longer than audio
            print("Extending audio with silence to match video length")
            # Create silence of needed duration
            silence_duration = video_duration - audio_duration
            temp_silence = os.path.join(temp_dir, 'temp_silence.aac')
            
            # Create silent audio
            cmd = [
                'ffmpeg', '-y', '-v', 'error',
                '-f', 'lavfi', '-i', f'anullsrc=r=48000:cl=mono',
                '-t', str(silence_duration),
                '-c:a', 'aac',
                temp_silence
            ]
            run_ffmpeg_with_progress(cmd, "Creating silent audio", silence_duration)
            
            # Concatenate original audio with silence
            temp_extended_audio = os.path.join(temp_dir, 'temp_extended_audio.aac')
            concat_list = os.path.join(temp_dir, 'concat_list.txt')
            
            with open(concat_list, 'w') as f:
                f.write(f"file '{os.path.abspath(audio_path)}'\nfile '{os.path.abspath(temp_silence)}'")
            
            cmd = [
                'ffmpeg', '-y', '-v', 'error',
                '-f', 'concat', '-safe', '0',
                '-i', concat_list,
                '-c', 'copy',
                temp_extended_audio
            ]
            run_ffmpeg_with_progress(cmd, "Concatenating audio", audio_duration + silence_duration)
            
            # Merge video with extended audio
            cmd = [
                'ffmpeg', '-y', '-v', 'error',
                '-i', video_path,
                '-i', temp_extended_audio,
                '-map', '0:v', '-map', '1:a',
                '-c:v', 'copy', '-c:a', 'copy',
                output_path
            ]
            run_ffmpeg_with_progress(cmd, "Merging with extended audio", video_duration)
            
            # Clean up temporary files
            for temp_file in [temp_silence, temp_extended_audio, concat_list]:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
    
    # Case 3: Audio is longer than video - slow down video if possible, otherwise freeze
    else:
        speed_ratio = video_duration / audio_duration
        
        if speed_ratio >= 0.5:  # Can slow down (min 0.5x speed)
            print(f"Slowing down video by factor of {speed_ratio:.2f} to match audio")
            filter_complex = f"[0:v]setpts={1/speed_ratio}*PTS[v]"
            cmd = [
                'ffmpeg', '-y', '-v', 'error',
                '-i', video_path,
                '-i', audio_path,
                '-filter_complex', filter_complex,
                '-map', '[v]', '-map', '1:a',
                '-c:v', 'libx264', '-c:a', 'aac',
                output_path
            ]
            run_ffmpeg_with_progress(cmd, "Slowing down video and merging", audio_duration)
            
        else:  # Need to freeze the last frame
            print("Freezing last frame to match audio duration")
            # Extract the last frame of the video
            last_frame_time = video_duration - 0.05  # Slightly before the end to ensure we get a frame
            last_frame_path = os.path.join(temp_dir, 'last_frame.png')
            
            cmd = [
                'ffmpeg', '-y', '-v', 'error',
                '-ss', str(last_frame_time),
                '-i', video_path,
                '-vframes', '1',
                last_frame_path
            ]
            run_ffmpeg_with_progress(cmd, "Extracting last frame", 1)
            
            # Create a video of the frozen last frame with the needed duration
            freeze_duration = audio_duration - video_duration
            freeze_video_path = os.path.join(temp_dir, 'freeze.mp4')
            
            cmd = [
                'ffmpeg', '-y', '-v', 'error',
                '-loop', '1',
                '-i', last_frame_path,
                '-t', str(freeze_duration),
                '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
                '-video_track_timescale', '90000',  # Ensure compatible timescale
                freeze_video_path
            ]
            run_ffmpeg_with_progress(cmd, "Creating freeze frame video", freeze_duration)
            
            # Concatenate original video with freeze frame video
            concat_list_path = os.path.join(temp_dir, 'video_concat.txt')
            with open(concat_list_path, 'w') as f:
                f.write(f"file '{os.path.abspath(video_path)}'\nfile '{os.path.abspath(freeze_video_path)}'")
            
            extended_video_path = os.path.join(temp_dir, 'extended_video.mp4')
            cmd = [
                'ffmpeg', '-y', '-v', 'error',
                '-f', 'concat', '-safe', '0',
                '-i', concat_list_path,
                '-c', 'copy',
                extended_video_path
            ]
            run_ffmpeg_with_progress(cmd, "Concatenating videos", video_duration + freeze_duration)
            
            # Merge extended video with audio
            cmd = [
                'ffmpeg', '-y', '-v', 'error',
                '-i', extended_video_path,
                '-i', audio_path,
                '-map', '0:v', '-map', '1:a',
                '-c:v', 'copy', '-c:a', 'aac',
                output_path
            ]
            run_ffmpeg_with_progress(cmd, "Merging with audio", audio_duration)
            
            # Clean up temporary files
            for temp_file in [last_frame_path, freeze_video_path, concat_list_path, extended_video_path]:
                if os.path.exists(temp_file):
                    os.remove(temp_file)

# Example usage
if __name__ == "__main__":
    merge_video_audio("1.mp4", "1.mp3", "output.mp4")