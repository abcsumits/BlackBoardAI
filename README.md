---

  # BlackBoardAI 🎥

  An AI-powered pipeline that automatically generates and uploads educational
  YouTube videos and Reels/Shorts from a single text prompt. It uses Google
  Gemini to write scripts, Manim to animate visuals, Kokoro TTS for voiceover,
  and the YouTube Data API to publish — all orchestrated through a Streamlit UI.

  ---

  ## How It Works

  1. **Prompt → Script** — Gemini generates a structured video script broken
  into timed segments.
  2. **Script → Visuals** — Each segment is rendered as an animated Manim scene.
  If Manim fails after retries, an SVG fallback is used instead.
  3. **Script → Audio** — Each segment's narration is synthesized with Kokoro
  TTS (voice `am_puck` by default). Optionally, F5-TTS can clone a custom voice.
  4. **Assembly** — Audio and video for each segment are combined and stitched
  into a final MP4 with FFmpeg/MoviePy.
  5. **Thumbnail** — An AI-designed SVG thumbnail is generated and rasterized.
  6. **Upload** — The finished video is uploaded to YouTube (private) via the
  YouTube Data API.

  ---

  ## Features

  - **YouTube videos & Reels/Shorts** — switchable format; Reels target < 2.5
  min with 9:16 aspect ratio.
  - **Parallel rendering** — all segments are rendered concurrently via Python
  threads.
  - **Auto-retry & fallback** — Manim scenes retry up to 3 times with LLM-based
  debug prompts; on failure they fall back to SVG → PNG → MP4.
  - **Regenerate individual frames** — `regenerate_controls.py` lets you
  re-render specific segments without re-running the full pipeline.
  - **Streamlit UI** — `ui.py` provides a simple web interface to submit prompts
  and track progress.
  - **Multi-key Gemini pool** — rotates across up to 22 API keys
  (`API_KEY1`…`API_KEY22`) to stay within rate limits.

  ---
  
  ## Tech Stack

  | Layer | Library / Service |
  |---|---|
  | LLM | Google Gemini (`gemini-3-flash-preview`) via `google-genai` |
  | Animation | Manim Community v0.19.0 |
  | SVG rendering | CairoSVG |
  | TTS | Kokoro (`kokoro`) |
  | Voice cloning | F5-TTS (`f5-tts_infer-cli`) |
  | Video editing | FFmpeg, MoviePy |
  | UI | Streamlit |
  | Upload | YouTube Data API v3 |

  ---
  ## Prerequisites
  
  - Python 3.10+
  - FFmpeg installed and on `PATH`
  - A Google Cloud project with the **YouTube Data API v3** enabled
  - OAuth 2.0 credentials downloaded as `token.json`
  - Google Gemini API keys (supports up to 22 keys for load balancing)
  
  ---
  
  ## Setup
  
  ### 1. Clone the repo (regenerate branch)
  
  ```bash
  git clone -b regenerate https://github.com/abcsumits/BlackBoardAI.git
  cd BlackBoardAI
  
  2. Install dependencies

  pip install -r requirements.txt
  python -m spacy download en_core_web_sm

  3. Configure environment variables

  Create a .env file in the project root:

  API_KEY1=your_gemini_api_key_1
  API_KEY2=your_gemini_api_key_2
  # ... up to API_KEY22

  4. Add YouTube OAuth credentials

  Place your OAuth 2.0 client secrets file at token.json in the project root.
  On first run the browser will open for authorization; subsequent runs reuse
  the token.

  ---
  Usage
  
  Web UI (recommended)

  streamlit run ui.py

  Enter a prompt, choose Video (16:9) or Reel (9:16), and click Generate Video.
  The UI shows live progress and returns the YouTube URL when done.

  Programmatic

  from start import start

  # Full YouTube video
  url = start("Explain how transformers work in deep learning")

  # Short / Reel
  url = start("What is gradient descent?", reel=True)

  Regenerate specific segments

  Edit regenerate_controls.py to set the frame numbers you want to redo, then
  run:

  python regenerate_controls.py

  ---
  Project Structure

  BlackBoardAI/
  ├── ui.py                    # Streamlit web interface
  ├── start.py                 # Main entry point — orchestrates the full
  pipeline
  ├── dialogue_writer.py       # Calls Gemini to produce per-segment scripts
  ├── manim_writer.py          # Generates & executes Manim code per segment
  ├── svg_video.py             # SVG fallback renderer
  ├── speech.py                # Kokoro TTS synthesis
  ├── clone_voice.py           # F5-TTS voice cloning
  ├── video_editor.py          # FFmpeg/MoviePy audio-video assembly
  ├── thumbnail.py             # SVG thumbnail generator
  ├── youtube_uploader.py      # YouTube Data API upload
  ├── titlendecription.py      # Generates title & description via Gemini
  ├── regenerate_controls.py   # Re-render individual segments
  ├── openAIapi.py             # Gemini client with multi-key rotation
  ├── add_audio.py             # Audio post-processing helpers
  ├── code_writer.py           # File write utility
  ├── delete_file.py           # File cleanup helpers
  ├── manim_prompt.py          # Manim code generation prompt
  ├── dialogue_prompt.py       # Script segmentation prompt
  ├── debug_prompt.py          # LLM debug prompt for Manim errors
  ├── svg_prompt.py            # SVG generation prompt
  ├── svgtopng.py              # CairoSVG rasterizer
  ├── image_to_video.py        # Still image → MP4 helper
  ├── insta_uploader.py        # Instagram upload (experimental)
  ├── requirements.txt
  └── template.svg             # Base SVG template

  ---
  Environment Notes
  
  - The pipeline creates temporary .py, .mp4, .mp3, .svg, and .png files per
  session identified by a UUID. These are cleaned up after upload.
  - Manim renders use the session UUID as a filename suffix to prevent
  collisions during parallel segment rendering.
  - If you are hosting on a web server, add your server's URL to the OAuth
  authorized redirect URIs in Google Cloud Console
  (https://console.cloud.google.com/auth/clients).

  ---
  
