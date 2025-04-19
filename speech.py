from kokoro import KPipeline
from IPython.display import display, Audio
import soundfile as sf
import torch
def texttospeech(text,filename):
    pipeline = KPipeline(lang_code='a')
    generator = pipeline(text+"   ", voice='af_heart')
    for i, (gs, ps, audio) in enumerate(generator):
        print(i, gs, ps)
        display(Audio(data=audio, rate=24000, autoplay=i==0))
        sf.write(filename, audio, 24000)
