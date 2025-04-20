from common import delete_file
import numpy as np
from moviepy.config import get_setting
import subprocess
import ffmpeg
import os
import math
import time

# Create directories if they don't exist
os.makedirs("output", exist_ok=True)
os.makedirs("temp/ffmpeg", exist_ok=True)

def combine_audio(video_path, audio_path, output_path):
    """Combine video and audio with smart speed adjustment and handling duration mismatches."""
    start_time = time.time()
    uuid = os.path.splitext(os.path.basename(video_path))[0]
    print(f"[INFO] Processing file: {uuid}")
    
    def get_duration(path):
        try:
            duration = float(ffmpeg.probe(path)['format']['duration'])
            return duration
        except Exception as e:
            raise ValueError(f"Could not get duration for {path}: {str(e)}")

    try:
        video_duration = get_duration(video_path)
        audio_duration = get_duration(audio_path)
        print(f"[INFO] Video duration: {video_duration:.2f}s, Audio duration: {audio_duration:.2f}s")
    except ValueError as e:
        print(f"[ERROR] {str(e)}")
        return None

    # Calculate speed factor with safe clamping
    speed_factor = video_duration / audio_duration if audio_duration != 0 else 1.0
    speed_factor = max(min(speed_factor, 2.0), 0.7)
    new_video_duration = video_duration / speed_factor
    print(f"[INFO] Speed adjustment factor: {speed_factor:.2f}x")

    input_video = ffmpeg.input(video_path)
    video_stream = input_video.video.filter('setpts', f'{1/speed_factor}*PTS')
    
    temp_files = []
    
    try:
        # Suppress FFmpeg output for cleaner logs
        ffmpeg_kwargs = {
            'quiet': True,
            'overwrite_output': True
        }
        
        # Case 1: Audio longer than adjusted video (freeze frame)
        if audio_duration > new_video_duration:
            freeze_duration = round(audio_duration - new_video_duration, 3)
            print(f"[INFO] Audio is longer by {freeze_duration:.2f}s - adding freeze frame")
            
            if freeze_duration < 0.1:
                print("[INFO] Difference too small, performing direct merge")
                ffmpeg.output(
                    video_stream,
                    ffmpeg.input(audio_path).audio,
                    output_path,
                    acodec='aac',
                    vcodec='libx264'
                ).run(**ffmpeg_kwargs)
                return output_path

            adjusted_video_path = f'./temp/ffmpeg/temp_adjusted_{uuid}.mp4'
            print(f"[INFO] Creating adjusted speed video")
            ffmpeg.output(video_stream, adjusted_video_path, vcodec='libx264').run(**ffmpeg_kwargs)
            temp_files.append(adjusted_video_path)

            last_frame_path = f'./temp/ffmpeg/temp_last_frame_{uuid}.png'
            frame_time = max(0, round(new_video_duration - 0.05, 2))
            try:
                print(f"[INFO] Extracting last frame for freeze")
                ffmpeg.input(adjusted_video_path, ss=frame_time).output(
                    last_frame_path, vframes=1
                ).run(**ffmpeg_kwargs)
            except:
                print(f"[INFO] Falling back to first frame")
                ffmpeg.input(adjusted_video_path, ss=0).output(
                    last_frame_path, vframes=1
                ).run(**ffmpeg_kwargs)
            temp_files.append(last_frame_path)

            freeze_path = f'./temp/ffmpeg/temp_freeze_{uuid}.mp4'
            print(f"[INFO] Creating freeze frame video of {freeze_duration:.2f}s")
            ffmpeg.input(last_frame_path, loop=1, t=round(freeze_duration, 2)).output(
                freeze_path, c='libx264', pix_fmt='yuv420p'
            ).run(**ffmpeg_kwargs)
            temp_files.append(freeze_path)

            final_video_path = f'./temp/ffmpeg/temp_final_video_{uuid}.mp4'
            concat_list = f'./temp/ffmpeg/temp_concat_{uuid}.txt'
            with open(concat_list, 'w') as f:
                f.write(f"file '{os.path.abspath(adjusted_video_path)}'\nfile '{os.path.abspath(freeze_path)}'")
            
            print(f"[INFO] Concatenating video segments")
            ffmpeg.input(concat_list, format='concat', safe=0).output(
                final_video_path, c='copy'
            ).run(**ffmpeg_kwargs)
            temp_files.extend([concat_list, final_video_path])

            print(f"[INFO] Adding audio track")
            ffmpeg.input(final_video_path).output(
                ffmpeg.input(audio_path).audio,
                output_path,
                acodec='aac',
                vcodec='copy'
            ).run(**ffmpeg_kwargs)

        # Case 2: Audio shorter than adjusted video (add silence)
        elif audio_duration < new_video_duration:
            silence_duration = round(new_video_duration - audio_duration, 3)
            print(f"[INFO] Audio is shorter by {silence_duration:.2f}s - adding silence")
            
            if silence_duration < 0.1:
                print("[INFO] Difference too small, performing direct merge")
                ffmpeg.output(
                    video_stream,
                    ffmpeg.input(audio_path).audio,
                    output_path,
                    acodec='aac',
                    vcodec='libx264'
                ).run(**ffmpeg_kwargs)
                return output_path

            # Get original audio parameters
            audio_info = ffmpeg.probe(audio_path)
            audio_stream = next((s for s in audio_info['streams'] if s['codec_type'] == 'audio'), None)
            if not audio_stream:
                raise ValueError("No audio stream found in input file")

            sample_rate = audio_stream.get('sample_rate', '44100')
            channels = audio_stream.get('channels', 2)

            # Generate silence in MP3 format
            silence_path = f'./temp/ffmpeg/temp_silence_{uuid}.mp3'
            print(f"[INFO] Generating {silence_duration:.2f}s of silence")
            ffmpeg.input(
                'anullsrc',
                f='lavfi',
                t=round(silence_duration, 2)
            ).output(
                silence_path,
                acodec='libmp3lame',
                ar=sample_rate,
                ac=channels
            ).run(**ffmpeg_kwargs)
            temp_files.append(silence_path)

            # Concatenate audio files
            extended_audio_path = f'./temp/ffmpeg/temp_extended_{uuid}.mp3'
            audio_concat_list = f'./temp/ffmpeg/temp_audio_concat_{uuid}.txt'
            with open(audio_concat_list, 'w') as f:
                f.write(f"file '{os.path.abspath(audio_path)}'\nfile '{os.path.abspath(silence_path)}'")
            
            print(f"[INFO] Concatenating audio with silence")
            ffmpeg.input(
                audio_concat_list,
                format='concat',
                safe=0
            ).output(
                extended_audio_path,
                c='copy'
            ).run(**ffmpeg_kwargs)
            temp_files.extend([audio_concat_list, extended_audio_path])

            # Merge with adjusted video
            adjusted_video_path = f'./temp/ffmpeg/temp_adjusted_{uuid}.mp4'
            print(f"[INFO] Creating adjusted speed video")
            ffmpeg.output(video_stream, adjusted_video_path, vcodec='libx264').run(**ffmpeg_kwargs)
            temp_files.append(adjusted_video_path)

            print(f"[INFO] Merging with extended audio")
            ffmpeg.input(adjusted_video_path).output(
                ffmpeg.input(extended_audio_path).audio,
                output_path,
                acodec='aac',
                vcodec='copy'
            ).run(**ffmpeg_kwargs)

        # Case 3: Exact match
        else:
            print(f"[INFO] Audio and video durations match - direct merge")
            ffmpeg.output(
                video_stream,
                ffmpeg.input(audio_path).audio,
                output_path,
                acodec='aac',
                vcodec='libx264'
            ).run(**ffmpeg_kwargs)

    except Exception as e:
        print(f"[ERROR] Processing {uuid}: {str(e)}")
        return None
    finally:
        # Clean up temp files
        print(f"[INFO] Cleaning up {len(temp_files)} temporary files")
        for f in temp_files:
            try:
                if os.path.exists(f):
                    os.remove(f)
            except Exception as e:
                print(f"[WARNING] Could not delete temporary file {f}: {str(e)}")

    elapsed_time = time.time() - start_time
    print(f"[SUCCESS] Created {output_path} in {elapsed_time:.2f}s")
    
    # Return basic file info
    try:
        file_size = os.path.getsize(output_path) / (1024 * 1024)  # Size in MB
        probe = ffmpeg.probe(output_path)
        final_duration = float(probe['format']['duration'])
        bitrate = int(probe['format']['bit_rate']) / 1000  # kbps
        print(f"[INFO] Output: {output_path}, Size: {file_size:.2f}MB, Duration: {final_duration:.2f}s, Bitrate: {bitrate:.1f}kbps")
    except Exception as e:
        print(f"[WARNING] Could not get final file info: {str(e)}")
    
    return output_path

def concatenate_frames(Total_frames, uid):
    """Concatenate multiple video frames into a single output video."""
    print(f"[INFO] Concatenating {Total_frames} frames for {uid}")
    start_time = time.time()
    
    # Create list file for FFmpeg concat
    list_path = f"./temp/concat_list_{uid}.txt"
    frame_count = 0
    
    with open(list_path, "w") as f:
        for i in range(1, Total_frames+1):
            frame_path = f"./temp/combined/{i}_{uid}.mp4"
            if os.path.exists(frame_path):
                f.write(f"file './combined/{i}_{uid}.mp4'\n")
                frame_count += 1
    
    if frame_count == 0:
        print(f"[ERROR] No frames found for {uid}")
        os.remove(list_path)
        return None
    
    print(f"[INFO] Found {frame_count}/{Total_frames} frames to concatenate")

    # FFmpeg direct concatenation (no re-encoding)
    output_path = f"./output/RESULT_{uid}.mp4"
    ffmpeg_bin = get_setting("FFMPEG_BINARY")
    
    print(f"[INFO] Concatenating video segments to {output_path}")
    try:
        # Redirect stdout and stderr to avoid verbose FFmpeg output
        cmd = [
            ffmpeg_bin,
            "-y",  # overwrite
            "-f", "concat",
            "-safe", "0",
            "-i", list_path,
            "-c", "copy",  # stream copy (no re-encode)
            "-loglevel", "error",  # suppress verbose output
            output_path
        ]
        
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        if result.stderr:
            print(f"[WARNING] FFmpeg warnings: {result.stderr.strip()}")
        
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] FFmpeg concatenation failed: {e}")
        if e.stderr:
            print(f"[ERROR] FFmpeg error: {e.stderr.strip()}")
        return None
    
    # Calculate and print completion statistics
    elapsed_time = time.time() - start_time
    try:
        file_size = os.path.getsize(output_path) / (1024 * 1024)  # Size in MB
        probe = ffmpeg.probe(output_path)
        duration = float(probe['format']['duration'])
        print(f"[SUCCESS] Created {output_path} in {elapsed_time:.2f}s")
        print(f"[INFO] Output file: Size: {file_size:.2f}MB, Duration: {duration:.2f}s")
    except Exception as e:
        print(f"[WARNING] Could not get output file info: {str(e)}")
    
    # Cleanup
    os.remove(list_path)
    print(f"[INFO] Cleaned up temporary concat list")
    
    # Uncomment to delete source files if needed
    # print(f"[INFO] Cleaning up source frame files")
    # for i in range(1, Total_frames+1):
    #     delete_file(f"./temp/combined/{i}_{uid}.mp4")
    
    return output_path