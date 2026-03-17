import inspect
import moviepy as mp

try:
    sig = inspect.signature(mp.AudioClip.write_audiofile)
    print('AudioClip.write_audiofile signature', sig)
except Exception as e:
    print('AudioClip error', e)

try:
    sig2 = inspect.signature(mp.VideoFileClip.write_audiofile)
    print('VideoFileClip.write_audiofile signature', sig2)
except Exception as e:
    print('VideoFileClip write_audiofile error', e)

# For completeness also inspect audio.component
print('Available methods in AudioFileClip:', [m for m in dir(mp.AudioFileClip) if 'write' in m.lower()])
