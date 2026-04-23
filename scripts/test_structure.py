#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de prueba para verificar la estructura modular.
"""

import sys
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent))

from src.file_manager import FileManager
from src.config import VIDEO_DIR, AUDIO_DIR, TEXT_DIR


def test_structure():
    """Prueba la estructura del proyecto."""
    print("\n" + "=" * 60)
    print(" 🧪 PRUEBA DE ESTRUCTURA DEL PROYECTO")
    print("=" * 60 + "\n")
    
    # Test 1: Verificar carpetas
    print("✅ VERIFICANDO CARPETAS...")
    print(f"   📁 Video: {VIDEO_DIR} -> {'✓' if VIDEO_DIR.exists() else '✗'}")
    print(f"   📁 Audio: {AUDIO_DIR} -> {'✓' if AUDIO_DIR.exists() else '✗'}")
    print(f"   📁 Texto: {TEXT_DIR} -> {'✓' if TEXT_DIR.exists() else '✗'}")
    
    # Test 2: Listar archivos
    print("\n✅ ARCHIVOS DISPONIBLES...")
    videos = FileManager.get_video_files()
    audios = FileManager.get_audio_files()
    
    print(f"\n   📹 VIDEOS ({len(videos)}):")
    for video in videos:
        is_trans = FileManager.has_transcription(video)
        status = "✅ TRANSCRITO" if is_trans else "⏳ PENDIENTE"
        print(f"      • {video.name} [{status}]")
    
    if not videos:
        print("      (No hay videos)")
    
    print(f"\n   🎵 AUDIOS ({len(audios)}):")
    for audio in audios:
        is_trans = FileManager.has_transcription(audio)
        status = "✅ TRANSCRITO" if is_trans else "⏳ PENDIENTE"
        print(f"      • {audio.name} [{status}]")
    
    if not audios:
        print("      (No hay audios)")
    
    # Test 3: Transcripciones generadas
    print(f"\n✅ TRANSCRIPCIONES GENERADAS:")
    transcriptions = list(TEXT_DIR.glob("*_transcripcion.txt"))
    
    if transcriptions:
        for trans in transcriptions:
            size_kb = trans.stat().st_size / 1024
            lines = len(trans.read_text(encoding="utf-8").split("\n"))
            print(f"      • {trans.name} ({size_kb:.2f} KB, {lines} líneas)")
    else:
        print("      (No hay transcripciones aún)")
    
    print("\n" + "=" * 60)
    print(" ✅ PRUEBA COMPLETADA")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    test_structure()
