import importlib
from pathlib import Path


def test_menu_flow(tmp_path, monkeypatch, capsys):
    """Recorre todos los submenús sin lanzar excepciones.

    - Se crean directorios temporales para `video/`, `mp3/` y `text/`.
    - Se parchean las constantes de `src.config` para apuntar a esos paths.
    - Se recarga `file_manager` y `menu` para que utilicen los nuevos directorios.
    - Se generan archivos "dummy" en las carpetas de video y audio.
    - Se sustituye `AudioTranscriber` por una versión simplificada que no
      carga Whisper ni MoviePy y que deja un archivo de transcripción.
    - Se simula la interacción de usuario con `builtins.input`.
    - Finalmente se comprueba que la salida contiene indicios de cada paso.
    """

    # configurar rutas temporales
    video_dir = tmp_path / "video"
    audio_dir = tmp_path / "mp3"
    text_dir = tmp_path / "text"
    video_dir.mkdir()
    audio_dir.mkdir()
    text_dir.mkdir()

    # parchear configuración
    import src.config as config
    monkeypatch.setattr(config, "VIDEO_DIR", video_dir)
    monkeypatch.setattr(config, "AUDIO_DIR", audio_dir)
    monkeypatch.setattr(config, "TEXT_DIR", text_dir)

    # recargar módulos que usan las rutas
    import src.file_manager as fm
    importlib.reload(fm)
    import src.menu as menu_mod
    importlib.reload(menu_mod)

    # crear archivos de ejemplo
    (video_dir / "video1.mp4").write_text("dummy")
    (audio_dir / "audio1.mp3").write_text("dummy")

    # transcriptor de prueba que únicamente escribe la transcripción
    class DummyTranscriber:
        def __init__(self):
            pass

        def transcribe_video(self, path: Path):
            fm.FileManager.save_transcription("texto de video", path)
            return "texto de video"

        def transcribe_audio_file(self, path: Path):
            fm.FileManager.save_transcription("texto de audio", path)
            return "texto de audio"

    monkeypatch.setattr(menu_mod, "AudioTranscriber", DummyTranscriber)

    menu = menu_mod.Menu()

    # secuencia de entradas: video->primer video->enter->audio->primer audio->enter->ver texto->1->enter->salir
    inputs = iter([
        "1",  # menú principal: Transcribir VIDEO
        "1",  # elegir el primer video
        "",   # presionar Enter cuando termine
        "2",  # menú principal: Transcribir AUDIO
        "1",  # elegir el primer audio
        "",   # presionar Enter
        "3",  # menú principal: Ver archivos de TEXTO
        "1",  # seleccionar primera transcripción
        "",   # volver
        "0",  # salir
    ])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))

    menu.run()
    stdout = capsys.readouterr().out

    # comprobaciones básicas sobre la salida
    assert "SISTEMA DE TRANSCRIPCIÓN" in stdout
    assert "Transcribir VIDEO" in stdout
    assert "Transcribir AUDIO MP3" in stdout
    assert "ARCHIVOS DE TRANSCRIPCIÓN" in stdout
    assert "texto de video" in stdout or "texto de audio" in stdout
