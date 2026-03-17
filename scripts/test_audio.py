import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.transcriber import AudioTranscriber
from src.file_manager import FileManager
from src.config import AUDIO_DIR

print("videos", FileManager.get_video_files())
print("audios", FileManager.get_audio_files())

trans = AudioTranscriber()
try:
    result = trans.transcribe_audio_file(AUDIO_DIR / 'Clase I.mp3')
    print('RESULT LENGTH', len(result) if result else 'None')
except Exception as e:
    import traceback
    traceback.print_exc()
    print('EXCEPTION', e)
