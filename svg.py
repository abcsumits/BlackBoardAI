from ai import AI
from dotenv import load_dotenv
from cairosvg import svg2png
from prompt import svg_prompt
from common import write_file, delete_file
from speech import texttospeech
from video_editor import combine_audio, get_media_duration
import ffmpeg

load_dotenv()

def image_to_video(input_image, output_video,duration):
    (
        ffmpeg
        .input(input_image, loop=1, t=duration)   # loop image, duration 1s
        .output(
            output_video,
            vcodec='libx264',
            pix_fmt='yuv420p',
            vf='scale=trunc(iw/2)*2:trunc(ih/2)*2'
        )
        .overwrite_output()
        .run()
    )
    delete_file(input_image)


class SVGVideoCreator:
    def __init__(self, ai: AI, task: str, text: str, frame_no_uid: str):
        self.ai = ai
        self.task = task
        self.text = text
        self.frame_no_uid = frame_no_uid
        self.svg_file_path = f"./temp/videos/{frame_no_uid}.svg"
        self.png_file_path = f"./temp/videos/{frame_no_uid}.png"
        self.audio_file_path = f"./temp/audios/{frame_no_uid}.mp3"
        self.video_file_path = f"./temp/videos/{frame_no_uid}.mp4"
        self.combined_video_path = f"./temp/combined/{frame_no_uid}.mp4"

    def run(self):
        try:
            self.generate_svg()
            self.convert_svg_to_png()
            self.generate_speech()
            self.create_video()
            self.merge_audio()
            self.cleanup()
        except Exception as e:
            print(f"Error occurred: {e}")
            self.run()

    def generate_svg(self):
        prompt = svg_prompt(self.task, self.text)
        svg_code = self.ai.send_prompt(prompt)

        # Clean up SVG code
        svg_code = svg_code.strip()
        for prefix in ['```', 'svg', 'xml', '"']:
            if svg_code.startswith(prefix):
                svg_code = svg_code[len(prefix):].strip()
        for suffix in ['```', '"']:
            if svg_code.endswith(suffix):
                svg_code = svg_code[:-len(suffix)].strip()

        write_file(svg_code, self.svg_file_path)
    
    def convert_svg_to_png(self, width=1920, height=1080):
        """
        Renders the SVG at specified width/height and writes a PNG.
        """
        try:
            svg2png(
                url=self.svg_file_path,
                write_to=self.png_file_path,
                output_width=width,
                output_height=height
            )
            print(f"Written PNG: {self.png_file_path}")
        finally:
            delete_file(self.svg_file_path)

    def generate_speech(self):
        texttospeech(self.text, self.audio_file_path)

    def create_video(self):
        duration = get_media_duration(self.audio_file_path) + 1
        image_to_video(self.png_file_path, self.video_file_path, duration)

    def merge_audio(self):
        combine_audio(self.frame_no_uid)

    def cleanup(self):
        pass
        # delete_file(self.temp_video_filename)
        # delete_file(self.audio_filename)
        # Optionally delete self.png_filename if you want to clean that too
        # delete_file(self.png_filename)