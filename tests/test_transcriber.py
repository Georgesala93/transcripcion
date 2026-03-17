import importlib
import os
from pathlib import Path
import pytest

import src.transcriber as trans_mod


def test_ffmpeg_check(monkeypatch):
    """Si no hay ffmpeg en el PATH el constructor debe fallar con RuntimeError."""
    monkeypatch.setattr("shutil.which", lambda cmd: None)
    with pytest.raises(RuntimeError) as exc:
        trans_mod.AudioTranscriber()
    assert "ffmpeg" in str(exc.value).lower()


def test_transcriber_instantiation(monkeypatch):
    """Con ffmpeg disponible el transcriptor se crea sin excepciones."""
    # haga que `which` encuentre ffmpeg inmediatamente
    monkeypatch.setattr("shutil.which", lambda cmd: "/usr/bin/ffmpeg")
    # evitar que Whisper descargue o cargue modelo pesado
    class DummyModel:
        def transcribe(self, *args, **kwargs):
            return {"text": ""}

    monkeypatch.setattr(trans_mod.whisper, "load_model", lambda name: DummyModel())

    tr = trans_mod.AudioTranscriber()
    assert tr.model is not None
    assert hasattr(tr, "transcribe_audio")


def test_ffmpeg_auto_add_from_winget(monkeypatch, tmp_path):
    """Si no está en PATH pero hay un binario en la carpeta de WinGet se añade."""
    # simulación de ubicación de winget
    fake_root = tmp_path / "Microsoft" / "WinGet" / "Packages" / "Some.FFmpeg_vX"
    fake_bin = fake_root / "ffmpeg-xyz" / "bin"
    fake_bin.mkdir(parents=True)
    # crear un archivo dummy llamado ffmpeg.exe
    (fake_bin / "ffmpeg.exe").write_text("")

    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))

    # implementamos which que detecta la ruta sólo si está en PATH
    def fake_which(cmd):
        for p in os.environ.get("PATH", "").split(os.pathsep):
            if p == str(fake_bin):
                return str(fake_bin / "ffmpeg.exe")
        return None
    monkeypatch.setattr("shutil.which", fake_which)

    # impedir la carga real del modelo
    class DummyModel:
        def transcribe(self, *args, **kwargs):
            return {"text": ""}
    monkeypatch.setattr(trans_mod.whisper, "load_model", lambda name: DummyModel())

    # ahora la inicialización debería funcionar; el path se añade internamente
    tr = trans_mod.AudioTranscriber()
    assert str(fake_bin) in os.environ["PATH"].split(os.pathsep)


def test_extract_audio_uses_correct_parameters(monkeypatch, tmp_path):
    """Al extraer audio no debe pasarse el argumento `verbose` a MoviePy."""
    # preparar un archivo falso de video
    video_file = tmp_path / "video.mp4"
    video_file.write_text("dummy")

    written = {}
    class DummyAudio:
        def write_audiofile(self, filename, **kwargs):
            written['filename'] = filename
            written['kwargs'] = kwargs
    class DummyVideo:
        def __init__(self, path):
            pass
        @property
        def audio(self):
            return DummyAudio()
        def close(self):
            pass

    monkeypatch.setattr(trans_mod.mp, "VideoFileClip", DummyVideo)
    monkeypatch.setattr("shutil.which", lambda cmd: "/usr/bin/ffmpeg")

    # evitar carga real de modelo
    class DummyModel:
        def transcribe(self, *a, **kw):
            return {"text": ""}
    monkeypatch.setattr(trans_mod.whisper, "load_model", lambda name: DummyModel())

    tr = trans_mod.AudioTranscriber()
    tr.extract_audio_from_video(video_file)

    # el nombre sigue convención _extracted.mp3
    assert written['filename'].endswith('_extracted.mp3')
    assert 'verbose' not in written['kwargs']
