import os
import time
import cv2
import tempfile
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# === CONFIGURATION ===
# INPUT_FILE = "index.html"  # Change to .svg or .html
INPUT_FILE = "index.svg"  # Change to .svg or .html
OUTPUT_VIDEO = "video.mp4"
WIDTH, HEIGHT = 800, 800
FPS = 120
DURATION = 5  # seconds
TOTAL_FRAMES = DURATION * FPS
OUTPUT_DIR = tempfile.mkdtemp(prefix="svg_video_frames_")

def setup_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument(f"--window-size={WIDTH},{HEIGHT}")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    return webdriver.Chrome(options=options)

def wrap_svg_if_needed(input_path):
    if input_path.endswith(".svg"):
        with open(input_path, "r", encoding="utf-8") as f:
            svg_content = f.read()
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{
                    margin: 0;
                    background: white;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                }}
                svg {{
                    width: 100vmin;
                    height: 100vmin;
                }}
            </style>
        </head>
        <body>{svg_content}</body>
        </html>
        """
        temp_html = os.path.join(tempfile.gettempdir(), "wrapped_svg.html")
        with open(temp_html, "w", encoding="utf-8") as f:
            f.write(html_content)
        return temp_html
    else:
        return input_path

def render_frames(driver, html_path):
    file_url = f"file://{os.path.abspath(html_path)}"
    driver.get(file_url)
    time.sleep(1)  # Wait for animation to load

    print(f"Rendering {TOTAL_FRAMES} frames...")
    for i in range(TOTAL_FRAMES):
        png = driver.get_screenshot_as_png()
        img = Image.open(BytesIO(png)).resize((WIDTH, HEIGHT))
        img_path = os.path.join(OUTPUT_DIR, f"frame_{i:04d}.png")
        img.save(img_path)
        time.sleep(1 / FPS)

def create_video_from_frames():
    print("Encoding video...")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(OUTPUT_VIDEO, fourcc, FPS, (WIDTH, HEIGHT))

    for i in range(TOTAL_FRAMES):
        frame_path = os.path.join(OUTPUT_DIR, f"frame_{i:04d}.png")
        frame = cv2.imread(frame_path)
        video.write(frame)

    video.release()
    print(f"✅ Saved video to: {OUTPUT_VIDEO}")

def cleanup_frames():
    import shutil
    shutil.rmtree(OUTPUT_DIR)

def main():
    html_input = wrap_svg_if_needed(INPUT_FILE)
    driver = setup_driver()
    try:
        render_frames(driver, html_input)
    finally:
        driver.quit()

    create_video_from_frames()
    cleanup_frames()

if __name__ == "__main__":
    main()