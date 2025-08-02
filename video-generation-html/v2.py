import os
import time
import cv2
import base64
import shutil
import tempfile
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# === CONFIGURATION ===
INPUT_FILE = "index.svg"  # Or an animated SVG
OUTPUT_VIDEO = "video.mp4"
WIDTH, HEIGHT = 1024, 1024
FPS = 60
DURATION = 5  # Seconds
TOTAL_FRAMES = DURATION * FPS
OUTPUT_DIR = tempfile.mkdtemp(prefix="svg_video_")

def wrap_svg(svg_path):
    """Wrap SVG content in HTML"""
    with open(svg_path, "r", encoding="utf-8") as f:
        svg = f.read()
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8" />
      <style>
        html, body {{
          margin: 0;
          padding: 0;
          background: white;
          display: flex;
          justify-content: center;
          align-items: center;
          width: 100vw;
          height: 100vh;
        }}
        svg {{
          width: 80vmin;
          height: 80vmin;
        }}
      </style>
    </head>
    <body>
      {svg}
    </body>
    </html>
    """
    wrapped_path = os.path.join(tempfile.gettempdir(), "wrapped_svg.html")
    with open(wrapped_path, "w", encoding="utf-8") as f:
        f.write(html)
    return wrapped_path

def init_browser():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument(f"--window-size={WIDTH},{HEIGHT}")
    chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def capture_frames(driver, url):
    print(f"Capturing {TOTAL_FRAMES} frames at {FPS}fps...")

    driver.get(url)
    time.sleep(1)  # Let JS initialize
    frames = []

    for i in range(TOTAL_FRAMES):
        screenshot = driver.get_screenshot_as_png()
        img = Image.open(BytesIO(screenshot)).resize((WIDTH, HEIGHT), Image.LANCZOS)
        path = os.path.join(OUTPUT_DIR, f"frame_{i:04d}.png")
        img.save(path)
        print(f"Captured frame {i+1}/{TOTAL_FRAMES}", end="\r")

    print("\nFrame capture complete.")

def encode_video():
    print("Encoding video with OpenCV...")
    out = cv2.VideoWriter(OUTPUT_VIDEO, cv2.VideoWriter_fourcc(*'mp4v'), FPS, (WIDTH, HEIGHT))
    for i in range(TOTAL_FRAMES):
        frame_path = os.path.join(OUTPUT_DIR, f"frame_{i:04d}.png")
        img = cv2.imread(frame_path)
        out.write(img)
    out.release()
    print(f"✅ Video saved: {OUTPUT_VIDEO}")

def cleanup():
    shutil.rmtree(OUTPUT_DIR)

def main():
    input_path = INPUT_FILE
    if input_path.endswith(".svg"):
        input_path = wrap_svg(input_path)

    driver = init_browser()
    try:
        file_url = f"file://{os.path.abspath(input_path)}"
        capture_frames(driver, file_url)
    finally:
        driver.quit()

    encode_video()
    cleanup()

if __name__ == "__main__":
    main()