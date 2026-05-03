# #manim -qh manim_run.py Frame
# from manim import *
# from manim import config
# # ----------------- User settings -----------------
# # Path to your image (change if necessary)
# IMAGE_PATH = "teminator.gif"
# # How many seconds the image should appear
# DISPLAY_SECONDS = 5
# # Output resolution and frame rate (set here so running via `manim file.py` uses these)
# config.pixel_width = 1920
# config.pixel_height = 1080
# config.frame_rate = 60
# # -------------------------------------------------

# class Frame(Scene):
#     """Scene that scales an image to fully cover a 1920x1080 frame and holds it."""

#     def construct(self):
#         # Load the image
#         img = ImageMobject(IMAGE_PATH)
#         # Center the image
#         img.move_to(ORIGIN)
#         FRAME_WIDTH = self.camera.frame_width
#         FRAME_HEIGHT = self.camera.frame_height

#         # Compute scale factors (manim units). We use FRAME_WIDTH / img.width etc.
#         # Use the larger factor so the image fully covers the frame (may crop the other axis).
#         scale_x = FRAME_WIDTH / img.width
#         scale_y = FRAME_HEIGHT / img.height
#         scale = min(scale_x, scale_y)
#         img.scale(scale)

#         # Add and hold the image for the requested duration
#         self.add(img)
#         self.wait(DISPLAY_SECONDS)


# # Optional: allow running this file with `python manim_cover_image.py` (manim's CLI still preferred)
"""
Manim Community v0.19.0 script — Cover an entire 1920x1080 frame with any input image.

This updated version supports animated GIFs correctly (instead of showing only the first
frame). For GIFs we extract frames with Pillow, write temporary PNG frames, and display
them in sequence — looping if necessary so the total visible time matches DISPLAY_SECONDS.

Place your image in the same folder as this script (default name: "screenshot.png")
or change the IMAGE_PATH variable below.

Usage (from terminal):
    manim -p -ql manim_cover_image.py CoverImageScene

"""
from manim import *
from PIL import Image, ImageSequence
import tempfile
import os
import math
import shutil

# ----------------- User settings -----------------
# Path to your image (change if necessary)
IMAGE_PATH = "teminator.gif"
# How many seconds the image (or animated GIF) should appear
DISPLAY_SECONDS = 5
# Output resolution and frame rate (set here so running via `manim file.py` uses these)
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 60
# -------------------------------------------------


def extract_gif_frames(path: str):
    """Extract frames from a GIF to a temporary directory.

    Returns: (frame_filepaths, frame_durations_seconds, tempdir)
    """
    im = Image.open(path)
    tempdir = tempfile.mkdtemp(prefix="manim_gif_")
    frames = []
    durations = []
    index = 0
    for frame in ImageSequence.Iterator(im):
        # Convert to RGBA to preserve transparency if any
        f = frame.convert("RGBA")
        fname = os.path.join(tempdir, f"frame_{index:04d}.png")
        f.save(fname)
        frames.append(fname)
        # duration is in milliseconds in many GIFs; default to 100ms if missing
        dur_ms = frame.info.get("duration", 100)
        durations.append(dur_ms / 1000.0)
        index += 1
    return frames, durations, tempdir


class Frame(Scene):
    """Scene that scales an image (static or animated GIF) to fully cover a 1920x1080 frame
    and holds it for DISPLAY_SECONDS seconds.
    """

    def construct(self):
        path = IMAGE_PATH
        lower = path.lower()
        FRAME_WIDTH = self.camera.frame_width
        FRAME_HEIGHT = self.camera.frame_height
        if lower.endswith(".gif"):
            # Handle animated GIF by extracting frames and displaying them in sequence.
            frames, durations, tempdir = extract_gif_frames(path)
            total_gif_duration = sum(durations) if durations else 0.0

            # If the GIF is shorter than DISPLAY_SECONDS, we'll loop it until we reach at least
            # DISPLAY_SECONDS (this prevents showing only the first frame). If the GIF is longer,
            # we'll play it once but stop when DISPLAY_SECONDS is reached.
            if total_gif_duration <= 0:
                # Fallback: treat as static image if something went wrong
                
                img = ImageMobject(path)
                img.move_to(ORIGIN)
                scale_x = FRAME_WIDTH / img.width
                scale_y = FRAME_HEIGHT / img.height
                img.scale(min(scale_x, scale_y))
                self.add(img)
                self.wait(DISPLAY_SECONDS)
                # cleanup
                shutil.rmtree(tempdir, ignore_errors=True)
                return

            # Determine how many loops needed to reach DISPLAY_SECONDS
            loops = math.ceil(DISPLAY_SECONDS / total_gif_duration)

            elapsed = 0.0
            prev = None
            try:
                for loop_index in range(loops):
                    for i, frame_path in enumerate(frames):
                        # Stop if we've already shown enough
                        if elapsed >= DISPLAY_SECONDS:
                            break

                        img = ImageMobject(frame_path)
                        img.move_to(ORIGIN)

                        # Scale to cover the full frame (may crop)
                        scale_x = FRAME_WIDTH / img.width
                        scale_y = FRAME_HEIGHT / img.height
                        img.scale(max(scale_x, scale_y))

                        if prev is None:
                            self.add(img)
                        else:
                            # Replace previous frame with current one (no transition)
                            self.remove(prev)
                            self.add(img)

                        # How long to show this frame — don't overshoot DISPLAY_SECONDS
                        frame_display = durations[i]
                        remaining = DISPLAY_SECONDS - elapsed
                        wait_time = min(frame_display, remaining)

                        self.wait(wait_time)
                        elapsed += wait_time
                        prev = img

                    if elapsed >= DISPLAY_SECONDS:
                        break
            finally:
                # Clean up temporary frame files
                shutil.rmtree(tempdir, ignore_errors=True)

        else:
            # Static image path (jpg/png/etc.) — original behavior
            img = ImageMobject(path)
            img.move_to(ORIGIN)

            # Compute scale factors (manim units). Use the larger factor so the image fully covers the frame.
            scale_x = FRAME_WIDTH / img.width
            scale_y = FRAME_HEIGHT / img.height
            scale = max(scale_x, scale_y)
            img.scale(scale)

            # Add and hold the image for the requested duration
            self.add(img)
            self.wait(DISPLAY_SECONDS)


