#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de validación completa del proyecto.
Prueba todos los módulos y flujos sin necesitar entrada manual.
"""

import sys
import warnings

sys.path.insert(0, ".")
warnings.filterwarnings("ignore")

PASS = "  ✅ PASS"
FAIL = "  ❌ FAIL"
SKIP = "  ⚠️  SKIP"
SEP  = "─" * 55


def check(label, fn):
    try:
        result = fn()
        print(f"{PASS}  {label}")
        return result
    except Exception as e:
        print(f"{FAIL}  {label}")
        print(f"          Error: {e}")
        return None


# ══════════════════════════════════════════════════════════
print(f"\n{'═' * 55}")
print("  VALIDACIÓN COMPLETA DEL PROYECTO")
print(f"{'═' * 55}")

# ─── TEST 1: Importaciones ────────────────────────────────
print(f"\n{'─' * 55}")
print("  TEST 1 — Importación de módulos")
print(SEP)

check("src.config",        lambda: __import__("src.config", fromlist=["VIDEO_DIR"]))
check("src.file_manager",  lambda: __import__("src.file_manager", fromlist=["FileManager"]))
check("src.transcriber",   lambda: __import__("src.transcriber", fromlist=["AudioTranscriber"]))
check("src.menu",          lambda: __import__("src.menu", fromlist=["Menu"]))
check("moviepy",           lambda: __import__("moviepy"))
check("whisper",           lambda: __import__("whisper"))
check("torch",             lambda: __import__("torch"))

# ─── TEST 2: FileManager ─────────────────────────────────
print(f"\n{'─' * 55}")
print("  TEST 2 — FileManager")
print(SEP)

from src.file_manager import FileManager
from src.config import VIDEO_DIR, AUDIO_DIR, TEXT_DIR

videos = check("get_video_files()",  FileManager.get_video_files) or []
audios = check("get_audio_files()",  FileManager.get_audio_files) or []

print(f"\n          📹 Videos detectados ({len(videos)}):")
for v in videos:
    status = "TRANSCRITO ✅" if FileManager.has_transcription(v) else "PENDIENTE ⏳"
    size_mb = FileManager.get_file_size_mb(v)
    print(f"             [{status}] {v.name} ({size_mb:.1f} MB)")

print(f"\n          🎵 Audios detectados ({len(audios)}):")
for a in audios:
    status = "TRANSCRITO ✅" if FileManager.has_transcription(a) else "PENDIENTE ⏳"
    size_mb = FileManager.get_file_size_mb(a)
    print(f"             [{status}] {a.name} ({size_mb:.1f} MB)")

if videos:
    v0 = videos[0]
    check("get_transcription_path(video)",       lambda: FileManager.get_transcription_path(v0))
    check("get_extracted_audio_path(video)",     lambda: FileManager.get_extracted_audio_path(v0))
    check("list_items_with_status(videos)",      lambda: FileManager.list_items_with_status(videos, "video"))

if audios:
    check("list_items_with_status(audios)",      lambda: FileManager.list_items_with_status(audios, "audio"))

# ─── TEST 3: FFmpeg ───────────────────────────────────────
print(f"\n{'─' * 55}")
print("  TEST 3 — FFmpeg en PATH")
print(SEP)

import shutil

def check_ffmpeg():
    path = shutil.which("ffmpeg")
    if not path:
        raise RuntimeError("ffmpeg no encontrado en PATH")
    return path

ffmpeg_path = check("ffmpeg disponible en PATH", check_ffmpeg)
if ffmpeg_path:
    print(f"          Ruta: {ffmpeg_path}")

# ─── TEST 4: MoviePy - apertura de video ─────────────────
print(f"\n{'─' * 55}")
print("  TEST 4 — MoviePy (apertura video sin extraer)")
print(SEP)

import moviepy as mp
from pathlib import Path

video_path = VIDEO_DIR / "Clase I.mp4"

def test_moviepy():
    video = mp.VideoFileClip(str(video_path))
    duracion = video.duration
    tiene_audio = video.audio is not None
    video.close()
    return duracion, tiene_audio

if video_path.exists():
    result = check("VideoFileClip abre correctamente", test_moviepy)
    if result:
        duracion, tiene_audio = result
        print(f"          Duración: {duracion:.1f}s  |  Tiene audio: {'Sí ✅' if tiene_audio else 'No ❌'}")
else:
    print(f"{SKIP}  Video no existe: {video_path.name}")

# ─── TEST 5: Whisper carga modelo ────────────────────────
print(f"\n{'─' * 55}")
print("  TEST 5 — Whisper (carga modelo 'base')")
print(SEP)

import whisper

def load_whisper():
    m = whisper.load_model("base")
    return type(m).__name__

result = check("whisper.load_model('base')", load_whisper)
if result:
    print(f"          Tipo de objeto: {result}")

# ─── TEST 6: AudioTranscriber inicializa ─────────────────
print(f"\n{'─' * 55}")
print("  TEST 6 — AudioTranscriber.__init__")
print(SEP)

from src.transcriber import AudioTranscriber

def build_transcriber():
    t = AudioTranscriber()
    nombre_modelo = type(t.model).__name__
    return nombre_modelo

result = check("AudioTranscriber() carga modelo interno", build_transcriber)
if result:
    print(f"          Modelo interno: {result}")

# ─── TEST 7: Menu instancia sin ejecutar ─────────────────
print(f"\n{'─' * 55}")
print("  TEST 7 — Menu (instancia, sin ejecutar run())")
print(SEP)

from unittest.mock import patch
from src.menu import Menu

def init_menu():
    # Interceptar AudioTranscriber para no cargar el modelo 2 veces
    with patch.object(AudioTranscriber, "__init__", lambda self: (
        setattr(self, "model_name", "base") or
        setattr(self, "model", None)
    )):
        m = Menu()
    return m

result = check("Menu() se instancia correctamente", init_menu)
if result:
    check("Menu.display_video_menu accesible",   lambda: callable(result.display_video_menu))
    check("Menu.display_audio_menu accesible",   lambda: callable(result.display_audio_menu))
    check("Menu.display_text_menu accesible",    lambda: callable(result.display_text_menu))
    check("Menu.process_video_option accesible", lambda: callable(result.process_video_option))
    check("Menu.process_audio_option accesible", lambda: callable(result.process_audio_option))

# ─── TEST 8: Transcripciones existentes ──────────────────
print(f"\n{'─' * 55}")
print("  TEST 8 — Transcripciones guardadas en text/")
print(SEP)

transcriptions = list(TEXT_DIR.glob("*_transcripcion.txt"))
print(f"          Archivos en text/: {len(transcriptions)}")
if transcriptions:
    for t in transcriptions:
        kb = t.stat().st_size / 1024
        lines = len(t.read_text(encoding="utf-8").split("\n"))
        print(f"             📄 {t.name}  ({kb:.1f} KB, {lines} líneas)")
else:
    print("          (ninguna aún — es normal en primera ejecución)")

# ─── RESUMEN FINAL ────────────────────────────────────────
print(f"\n{'═' * 55}")
print("  VALIDACIÓN COMPLETADA")
print(f"{'═' * 55}")
print()
print("  Para ejecutar la app:")
print("  👉  python main.py")
print()
