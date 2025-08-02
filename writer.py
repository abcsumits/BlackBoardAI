from ai import AI
from prompt import dialogue_prompt, manim_code_prompt, ask_for_story, debug_prompt
from common import write_file, delete_file, move_file
from exceptions import AIError
from speech import texttospeech
from svg import SVGVideoCreator
from video_editor import combine_audio, concatenate_frames
import json
import re
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
load_dotenv()

class Writer:
    def __init__(self, ai: AI, user_prompt: str, uuid: str, MAX_THREADS: int = int(os.getenv("MAX_THREADS", 5))):
        self.ai = ai
        self.story = None
        self.user_prompt = user_prompt
        self.uuid = uuid
        self.segments = None
        self.MAX_THREADS = MAX_THREADS
    
    def create_video(self):
        self.story = self.ai.send_prompt(ask_for_story(self.user_prompt))
        self.__generate_segments()
        self.__shoot_video_segments()
        self.__stitch_video_segments()

    def __generate_segments(self, retry: int = 5):
        if retry == 0: 
            print("ERROR: Maximum retries reached for segment generation.")
            exit(1)

        segments = self.ai.send_prompt(dialogue_prompt(self.story))
        print("INFO: Response received from AI for segments")
        segments = re.sub(r'^```(?:\w+)?\n', '', segments).strip()
        segments = re.sub(r'^json(?:\w+)?\n', '', segments).strip()
        if segments.endswith("```"):
            segments = segments[:-3].strip()
        
        try:
            segments = json.loads(segments)
            for i in range(1, len(segments) + 1):
                if "segment" + str(i) not in segments:
                    self.__generate_segments(retry-1)
                    return
                else:
                    if len(segments["segment" + str(i)]) != 2:
                        self.__generate_segments(retry-1)
                        return
        except Exception as e:
            self.story += f" your last response raised this exception make sure not to repeat this mistake again: {str(e)}"
            self.__generate_segments(retry-1)
        
        print("INFO: Number of segments received from AI:", len(segments))

        with open(f"./temp/segments_{self.uuid}.json", "w") as f:
            json.dump(segments, f, indent=4)

        print("INFO: Segments saved to file")
        self.segments = segments
        return self.segments
    
    def __shoot_video_segments(self):
        if self.segments is None:
            raise AIError("Segments not generated. Call generate_segments() first.", error_type="SegmentError")
        print("INFO: Shooting video segments")
        with ThreadPoolExecutor(max_workers=self.MAX_THREADS) as executor:
            futures = []
            for i in range(1, len(self.segments) + 1):
                text = self.segments[f"segment{i}"][0] + ' this are sub visuals of the following prompt: ' + self.user_prompt
                image_prompt = self.segments["segment" + str(i)][1]
                futures.append(executor.submit(write_manim, self.ai, text, str(i), image_prompt, self.uuid))
            
            for future in as_completed(futures):
                future.result()  # Wait for all to complete (and catch any exceptions)
    
    def __stitch_video_segments(self):
        if self.segments is None:
            raise AIError("Segments not generated. Call generate_segments() first.", error_type="SegmentError")

        print("INFO: Stitching video segments")
        concatenate_frames(len(self.segments), self.uuid)
        print("INFO: Video created successfully")
            

# Ensure directories exist
os.makedirs('./temp/videos', exist_ok=True)
os.makedirs('./temp/audios', exist_ok=True)
os.makedirs('./temp/combined', exist_ok=True)
os.makedirs('./temp/ffmpeg', exist_ok=True)

def write_manim(ai: AI, task, frame_no, text, uid, error='', cnt = 3, code=''):
    frame_no_uid = f"{frame_no}_{uid}"
    if cnt == 0:
        SVGVideoCreator(ai, task, text, frame_no_uid).run()
        return
    
    print(f"INFO: Generating code for frame {frame_no}")
    
    if error=='' or cnt==1:
        code_str=ai.send_prompt(manim_code_prompt(task, text))
    else:
        code_str=ai.send_prompt(debug_prompt(code, error))

    print("INFO: Response received from AI for code generation")
    # Clean code
    print("INFO: Cleaning code")
    if code_str.startswith('```'):
        code_str = code_str[3:].strip()
    if code_str.startswith('python'):
        code_str = code_str[6:].strip()
    if code_str.startswith('manim'):
        code_str = code_str[5:].strip()
    if code_str.startswith('"'):
        code_str = code_str[1:].strip()
    if code_str.endswith("```"):
        code_str = code_str[:-3].strip()
    if code_str.endswith('"'):
        code_str = code_str[:-1].strip()
    
    # Write code to file
    file_name = f"./temp/{frame_no_uid}.py"
    print(f"INFO: Writing the generated code to {file_name}")
    write_file(code_str, file_name)
    
    # Execute Manim
    try:
        print(f"INFO: Executing the manim code in the file {file_name}")
        result = subprocess.run(
            ['manim', '-qh', file_name, 'Frame'], 
            text=True,
            capture_output=True,
            timeout=100,
            check=True  # we handle errors manually
        )

        if result.returncode != 0:
            print(f"ERROR: Manim execution failed with return code {result.returncode}")
            print("INFO: Manim STDERR:", result.stderr)
            raise RuntimeError(f"Manim execution failed: {result.stderr}")

        # Move the generated video
        src_video_path = f"./media/videos/{frame_no_uid}/1080p60/Frame.mp4"
        dest_video_path = f"./temp/videos/{frame_no_uid}.mp4"

        if not os.path.exists(src_video_path):
            raise FileNotFoundError(f"Expected video output not found: {src_video_path}")

        if not move_file(src_video_path, dest_video_path):
            print("WARNING: Multiple videos generated, cleaning up")
            delete_file(f"./media/videos/{frame_no_uid}")
            raise RuntimeError("Multiple videos generated, expected only one.")

        print("SUCCESS: Manim code executed successfully in a single video")

        # Generate audio
        audio_path = f"./temp/audios/{frame_no_uid}.mp3"
        texttospeech(text, audio_path)

        if not os.path.exists(audio_path):
            raise RuntimeError("Audio generation FAILED")

        print("INFO: Audio generated successfully")

        # Combine audio and video
        combine_audio(frame_no_uid)

        print("INFO: Audio and video combined successfully")
        return True

    except Exception as e:
        print(f"ERROR: Manim code execution failed with error: {str(e)}")
        print("INFO: Attempting to regenerate code")
        
        # Clean up
        if os.path.exists(file_name):
            delete_file(file_name)
        media_path = f"./media/videos/{frame_no_uid}"
        if os.path.exists(media_path):
            delete_file(media_path)

        # Retry with cnt - 1
        write_manim(
            ai, task, frame_no, text, uid, 
            f"Strictly fix the error: {str(e)}. Your last code:\n{code_str}",
            cnt-1
        )