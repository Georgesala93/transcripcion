"""
Configuración centralizada del proyecto.
"""

import os
from pathlib import Path

# Rutas base
BASE_DIR = Path(__file__).parent.parent
MEDIA_DIR = BASE_DIR / "media"
VIDEO_DIR = MEDIA_DIR / "video"
AUDIO_DIR = MEDIA_DIR / "mp3"
TEXT_DIR = MEDIA_DIR / "text"

# Crear directorios si no existen
MEDIA_DIR.mkdir(exist_ok=True)
VIDEO_DIR.mkdir(exist_ok=True)
AUDIO_DIR.mkdir(exist_ok=True)
TEXT_DIR.mkdir(exist_ok=True)

# Configuración de Whisper
WHISPER_MODEL = "base"  # 'base', 'small', 'medium', 'large'
WHISPER_LANGUAGE = "es"  # Idioma de transcripción
VERBOSE = False

# Patrones de archivo
VIDEO_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv"}
AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".flac", ".ogg"}

# Sufijos para archivos generados
AUDIO_SUFFIX = "_extracted"
TRANSCRIPTION_SUFFIX = "_transcripcion"
EXTENSION_TEXT = ".txt"

# Configuración de UI
MENU_SEPARATOR = "=" * 60
MENU_OPTION_FORMAT = "  [{num}] {text}"
