#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Ejemplo de uso de los módulos de forma programática.
Muestra cómo usar la aplicación sin el menú interactivo.
"""

import sys
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent))

from src.file_manager import FileManager
from src.transcriber import AudioTranscriber
from src.config import VIDEO_DIR, AUDIO_DIR


def example_usage():
    """Ejemplo de uso de los módulos."""
    print("\n" + "=" * 60)
    print(" 📚 EJEMPLO DE USO DE MÓDULOS")
    print("=" * 60 + "\n")
    
    # ============== EJEMPLO 1: FileManager ==============
    print("1️⃣  USANDO FileManager\n")
    
    videos = FileManager.get_video_files()
    print(f"   📹 Se encontraron {len(videos)} video(s)")
    
    if videos:
        print(f"\n   Primer video: {videos[0].name}")
        
        # Verificar si ya fue transcrito
        is_transcribed = FileManager.has_transcription(videos[0])
        print(f"   ¿Ya transcrito? {'Sí ✅' if is_transcribed else 'No ⏳'}")
        
        # Obtener ruta de transcripción
        trans_path = FileManager.get_transcription_path(videos[0])
        print(f"   Ruta de transcripción: {trans_path}")
        
        # Tamaño del archivo
        size_mb = FileManager.get_file_size_mb(videos[0])
        print(f"   Tamaño: {size_mb:.2f} MB")
    
    # ============== EJEMPLO 2: AudioTranscriber ==============
    print("\n\n2️⃣  USANDO AudioTranscriber\n")
    
    audios = FileManager.get_audio_files()
    print(f"   🎵 Se encontraron {len(audios)} archivo(s) de audio")
    
    if audios:
        print(f"\n   Primer audio: {audios[0].name}")
        print(f"   Tamaño: {FileManager.get_file_size_mb(audios[0]):.2f} MB")
        
        # Para transcribir, descomenta las siguientes líneas:
        # transcriber = AudioTranscriber()
        # transcriber.transcribe_audio_file(audios[0])
    
    # ============== EJEMPLO 3: Listar con estado ==============
    print("\n\n3️⃣  LISTAR ARCHIVOS CON ESTADO\n")
    
    if videos:
        print("   📹 VIDEOS:")
        items = FileManager.list_items_with_status(videos, "video")
        for num, display_name, is_trans in items:
            print(f"      [{num}] {display_name}")
    
    print("\n" + "=" * 60)
    print(" ✅ EJEMPLO COMPLETADO")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    example_usage()
