import warnings
warnings.filterwarnings("ignore", message=r".*torch\.nn\.utils\.weight_norm.*", category=FutureWarning)
warnings.filterwarnings("ignore", message=r".*dropout option adds dropout after all but last recurrent layer.*", category=UserWarning)
from kokoro import KPipeline
from IPython.display import display, Audio
import soundfile as sf

def texttospeech(text,filename):
    pipeline = KPipeline(lang_code='a')
    generator = pipeline(text.strip(), voice='af_heart')
    for i, (gs, ps, audio) in enumerate(generator):
        display(Audio(data=audio, rate=24000, autoplay=i==0))
        sf.write(filename, audio, 24000)
