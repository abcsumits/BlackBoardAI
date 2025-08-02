from common import delete_file
import numpy as np
from moviepy.config import get_setting
import subprocess
import ffmpeg
import os
import ffmpeg
import os

def get_duration(path):
        try:
            return float(ffmpeg.probe(path)['format']['duration'])
        except Exception as e:
            raise ValueError(f"Could not get duration for {path}: {str(e)}")

def combine_audio(num):
    video_path = f"./temp/videos/{num}.mp4"
    audio_path = f"./temp/audios/{num}.mp3"
    output_path = f"./temp/combined/{num}.mp4"
    
    
    try:
        video_duration = get_duration(video_path)
        audio_duration = get_duration(audio_path)
    except ValueError as e:
        print(f"Error: {str(e)}")
        return None

    # Calculate speed factor with safe clamping
    speed_factor = video_duration / audio_duration if audio_duration != 0 else 1.0
    speed_factor = max(min(speed_factor, 2.0), 0.5)
    new_video_duration = video_duration / speed_factor

    input_video = ffmpeg.input(video_path)
    video_stream = input_video.video.filter('setpts', f'{1/speed_factor}*PTS')
    
    temp_files = []
    
    try:
        # Case 1: Audio longer than adjusted video (freeze frame)
        if audio_duration > new_video_duration:
            freeze_duration = round(audio_duration - new_video_duration, 3)
            
            if freeze_duration < 0.1:
                ffmpeg.output(
                    video_stream,
                    ffmpeg.input(audio_path).audio,
                    output_path,
                    acodec='aac',
                    vcodec='libx264'
                ).run(overwrite_output=True)
                return output_path

            adjusted_video_path = f'./temp/ffmpeg/adjusted_{num}.mp4'
            ffmpeg.output(video_stream, adjusted_video_path, vcodec='libx264').run(overwrite_output=True)
            temp_files.append(adjusted_video_path)

            last_frame_path = f'./temp/ffmpeg/last_frame_{num}.png'
            frame_time = max(0, round(new_video_duration - 0.05, 2))
            try:
                ffmpeg.input(adjusted_video_path, ss=frame_time).output(
                    last_frame_path, vframes=1
                ).run(overwrite_output=True)
            except:
                ffmpeg.input(adjusted_video_path, ss=0).output(
                    last_frame_path, vframes=1
                ).run(overwrite_output=True)
            temp_files.append(last_frame_path)

            freeze_path = f'./temp/ffmpeg/freeze_{num}.mp4'
            ffmpeg.input(last_frame_path, loop=1, t=round(freeze_duration, 2)).output(
                freeze_path, c='libx264', pix_fmt='yuv420p'
            ).run(overwrite_output=True)
            temp_files.append(freeze_path)

            final_video_path = f'./temp/combined/combined_{num}.mp4'
            concat_list = f'./temp/ffmpeg/concat_{num}.txt'
            with open(concat_list, 'w') as f:
                f.write(f"file '{os.path.abspath(adjusted_video_path)}'\nfile '{os.path.abspath(freeze_path)}'")
            ffmpeg.input(concat_list, format='concat', safe=0).output(
                final_video_path, c='copy'
            ).run(overwrite_output=True)
            temp_files.extend([concat_list, final_video_path])

            ffmpeg.input(final_video_path).output(
                ffmpeg.input(audio_path).audio,
                output_path,
                acodec='aac',
                vcodec='copy'
            ).run(overwrite_output=True)

        # Case 2: Audio shorter than adjusted video (add silence)
        elif audio_duration < new_video_duration:
            silence_duration = round(new_video_duration - audio_duration, 3)
            
            if silence_duration < 0.1:
                ffmpeg.output(
                    video_stream,
                    ffmpeg.input(audio_path).audio,
                    output_path,
                    acodec='aac',
                    vcodec='libx264'
                ).run(overwrite_output=True)
                return output_path

            # Get original audio parameters
            audio_info = ffmpeg.probe(audio_path)
            audio_stream = next((s for s in audio_info['streams'] if s['codec_type'] == 'audio'), None)
            if not audio_stream:
                raise ValueError("No audio stream found in input file")

            sample_rate = audio_stream.get('sample_rate', '44100')
            channels = audio_stream.get('channels', 2)

            # Generate silence in MP3 format
            silence_path = f'./temp/ffmpeg/silence_{num}.mp3'
            ffmpeg.input(
                'anullsrc',
                f='lavfi',
                t=round(silence_duration, 2)
            ).output(
                silence_path,
                acodec='libmp3lame',
                ar=sample_rate,
                ac=channels
            ).run(overwrite_output=True)
            temp_files.append(silence_path)

            # Concatenate audio files
            extended_audio_path = f'./temp/ffmpeg/extended_{num}.mp3'
            audio_concat_list = f'./temp/ffmpeg/audio_concat_{num}.txt'
            with open(audio_concat_list, 'w') as f:
                f.write(f"file '{os.path.abspath(audio_path)}'\nfile '{os.path.abspath(silence_path)}'")
            
            ffmpeg.input(
                audio_concat_list,
                format='concat',
                safe=0
            ).output(
                extended_audio_path,
                c='copy'
            ).run(overwrite_output=True)
            temp_files.extend([audio_concat_list, extended_audio_path])

            # Merge with adjusted video
            adjusted_video_path = f'./temp/ffmpeg/adjusted_{num}.mp4'
            ffmpeg.output(video_stream, adjusted_video_path, vcodec='libx264').run(overwrite_output=True)
            temp_files.append(adjusted_video_path)

            ffmpeg.input(adjusted_video_path).output(
                ffmpeg.input(extended_audio_path).audio,
                output_path,
                acodec='aac',  # Convert final output to AAC
                vcodec='copy'
            ).run(overwrite_output=True)

        # Case 3: Exact match
        else:
            ffmpeg.output(
                video_stream,
                ffmpeg.input(audio_path).audio,
                output_path,
                acodec='aac',
                vcodec='libx264'
            ).run(overwrite_output=True)

    except Exception as e:
        print(f"Error processing {num}: {str(e)}")
        return None
    finally:
        for f in temp_files:
            try:
                if os.path.exists(f):
                    os.remove(f)
            except Exception as e:
                print(f"Warning: Could not delete temporary file {f}: {str(e)}")

    return output_path


def create_video(total_frames, uid):
    ffmpeg_bin  = get_setting("FFMPEG_BINARY")
    output_path = f"./output/video_{uid}.mp4"

    # 1) Gather all existing MP4 segments
    inputs = []
    for i in range(1, total_frames + 1):
        fn = f"./temp/combined/{i}_{uid}.mp4"
        if os.path.exists(fn):
            inputs.append(fn)
        else:
            print(f"Warning: {fn} missing, skipping.")

    if not inputs:
        raise RuntimeError("No input segments found!")

    # 2) Build ffmpeg command with one -i per file
    cmd = [ffmpeg_bin, "-y"]
    for fn in inputs:
        cmd += ["-i", fn]

    # 3) Build the filter_complex string: "[0:v][0:a][1:v][1:a]...concat=n=N:v=1:a=1[v][a]"
    N = len(inputs)
    spec = []
    for idx in range(N):
        spec += [f"[{idx}:v:0]", f"[{idx}:a:0]"]
    filter_complex = "".join(spec) + f"concat=n={N}:v=1:a=1[v][a]"

    cmd += [
        "-filter_complex", filter_complex,
        "-map", "[v]", "-map", "[a]",
        output_path
    ]

    # 4) Run it
    subprocess.run(cmd, check=True)
    for i in range(1, total_frames+1):
        delete_file(f"./temp/combined/{i}_{uid}.mp4")