import streamlit as st
import time
import uuid
from start import start

# Configure page first
st.set_page_config(page_title="BlackBoardAI", page_icon="🎥")
st.title("🎥 BlackBoardAI")

# Initialize session state variables
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if 'youtube_url' not in st.session_state:
    st.session_state.youtube_url = None
if 'processing' not in st.session_state:
    st.session_state.processing = False

# Input section
with st.form("prompt_form"):
    prompt = st.text_area("Enter your video prompt:", height=150)
    submitted = st.form_submit_button("Generate Video")

# Handle form submission
if submitted and prompt:
    st.session_state.processing = True
    st.session_state.youtube_url = None

# Processing section
if st.session_state.processing:
    with st.status("Generating your video...", expanded=True) as status:
        try:
            # Show processing stages
            with st.container():
                st.write("🔍 Analyzing your prompt...")
                time.sleep(0.5)
                
                st.write("🎬 Creating storyboard...")
                time.sleep(0.5)
                
                st.write("📹 Rendering video content...")
                time.sleep(0.5)
            
            # Call the video generation function
            print("🚀 Starting video generation...")
            st.session_state.youtube_url = start(prompt, st.session_state.session_id)
            
            # Final processing step
            st.write("📤 Uploading to YouTube...")
            time.sleep(0.5)
            
            status.update(label="✅ Generation complete!", state="complete", expanded=False)
            
        except Exception as e:
            st.error(f"🚨 Error generating video: {str(e)}")
            st.session_state.youtube_url = None
            status.update(label="❌ Processing failed", state="error")
            
    st.session_state.processing = False

# Result section
if st.session_state.youtube_url:
    st.success("🎉 Video generated successfully!")
    st.video(st.session_state.youtube_url)
    st.markdown(f"""
    **📎 YouTube Link:**  
    `{st.session_state.youtube_url}`
    """)
    st.button("Clear Results", on_click=lambda: st.session_state.update(
        youtube_url=None,
        processing=False
    ))