from ai import AI
from prompt import dialogue_prompt, manim_code_prompt, ask_for_story
from common import write_file, delete_file, move_file
from exceptions import AIError
from speech import texttospeech
from video_editor import combine_audio, concatenate_frames
import json
import re
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Writer:
    def __init__(self, ai: AI, user_prompt: str, uuid: str, MAX_THREADS: int = int(os.getenv("MAX_THREADS", 1))):
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

        with open(os.path.join(BASE_DIR, f"temp/segments_{self.uuid}.json"), "w") as f:
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
                text = self.segments["segment" + str(i)][0] + ' this are sub visuals of the following prompt: ' + self.user_prompt
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
os.makedirs(os.path.join(BASE_DIR, 'temp/videos'), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, 'temp/audios'), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, 'temp/combined'), exist_ok=True)

def write_manim(ai: AI, task, frame_no, text, uid, error='', cnt = 2):
    if cnt == 0:
        return
    print("INFO: Generating code for frame", frame_no)
    frame_no = f"{frame_no}_{uid}"
    file_name=os.path.join(BASE_DIR, f"temp/{frame_no}.py")
    code_str=ai.send_prompt(manim_code_prompt(task,text,error))
    print("INFO: Response received from AI for code generation")
    print("INFO: Cleaning code")
    code_str = re.sub(r'^```(?:\w+)?\n', '', code_str).strip()
    code_str = re.sub(r'^python(?:\w+)?\n', '', code_str).strip()
    code_str = re.sub(r'^manim(?:\w+)?\n', '', code_str).strip()
    if code_str.endswith("```"):
        code_str = code_str[:-3].strip()
    print("INFO: Code cleaned. Moving to file creation")
    try:
        print(f"INFO: Writing the generated code to {file_name}")
        write_file(code_str, file_name)
        print("INFO: Executing the manim code in the file", file_name)
        # Execute the manim command
        subprocess.run('manim -qh '+file_name+' Frame', shell=True, text=True, capture_output=True,timeout=600 )
        delete_file(file_name)
        print("INFO: Manim code executed successfully")
        if not move_file(
                os.path.join(BASE_DIR, f'media/videos/{frame_no}/1080p60/Frame.mp4'),
                os.path.join(BASE_DIR, f'temp/videos/{frame_no}.mp4')):
            print("WARNING: Multiple videos generated, only one needs to be processed. Deleting the extra video files")
            delete_file(os.path.join(BASE_DIR, f'media/videos/{frame_no}'))
            print("INFO: Sending for regenerating the manim code")
            write_manim(task,
                        frame_no,
                        text,
                        "",
                        f'''Strictly fix theError: Your last  code generated multiple video , only single video will get processed '''+'''Your last Code : '''+code_str,
                        cnt-1)
        else:
            if os.path.exists(os.path.join(BASE_DIR, f'temp/videos/{frame_no}.mp4')):
                print("SUCCESS: Manim code executed successfully in a single video")
            else:
                print("ERROR: Manim code execution FAILED")

            texttospeech(text, os.path.join(BASE_DIR, f"temp/audios/{frame_no}.mp3"))
            if not os.path.exists(os.path.join(BASE_DIR, f'temp/audios/{frame_no}.mp3')):
                print("ERROR: Audio generation FAILED")

            print("INFO: Audio generated successfully")
            print("INFO: Combining audio and video")
            combine_audio(
                os.path.join(BASE_DIR, f'temp/videos/{frame_no}.mp4'), 
                os.path.join(BASE_DIR, f'temp/audios/{frame_no}.mp3'), 
                os.path.join(BASE_DIR, f'temp/combined/{frame_no}.mp4')
            )
            print("INFO: Audio and video combined successfully")
            # print("INFO: Deleting the extra video files")
            # delete_file('./temp/videos/'+frame_no+'.mp4')
            # delete_file('./temp/audios/'+frame_no+'.mp3')
            # delete_file('./media/videos/'+frame_no)
            return True

    except subprocess.CalledProcessError as e:
        print("ERROR: Manim code execution failed")
        print("INFO: Error message:", e.stderr)
        print("INFO: Sending for regenerating the manim code")
        if os.path.exists(file_name):
            delete_file(file_name)
        delete_file(os.path.join(BASE_DIR, f'media/videos/{frame_no}.mp4'))
        write_manim(ai, task, frame_no, text,"",'''Your last CODE  generated ERROR , DONOT REPEAT SAME MISTAKE AGAIN{Error: '''+e.stderr+"}"+"Strictly make the code error less",cnt-1)
        return
    except Exception as e:
        print("ERROR: Manim code execution failed")
        print("INFO: Error message:", str(e))
        print("INFO: Sending for regenerating the manim code")
        print("INFO: Deleting the extra video files")
        if os.path.exists(file_name):
            delete_file(file_name)
        delete_file(file_name)
        delete_file(os.path.join(BASE_DIR, f'media/videos/{frame_no}.mp4'))
        write_manim(ai, task, frame_no,text, "" ,'''Your last CODE  generated ERROR , DONOT REPEAT SAME MISTAKE AGAIN{Error: '''+str(e)+"}",cnt-1)
        return