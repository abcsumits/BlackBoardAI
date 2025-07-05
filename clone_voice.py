import subprocess
def clone_voice(clone_voice_path,output_path,voice_text,reference_text=""):
    command=f'''f5-tts_infer-cli --model F5TTS_v1_Base --ref_audio "{clone_voice_path}" --ref_text "{reference_text}" --gen_text "{voice_text}" --output_file "{output_path}"'''
    subprocess.run(command,shell=True)