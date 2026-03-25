"""
Gestor de archivos para el proyecto de transcripción.
Maneja la lectura, validación y organización de archivos.
"""

import os
from pathlib import Path
from typing import List, Tuple, Optional
from src.config import (
    VIDEO_DIR, AUDIO_DIR, TEXT_DIR,
    VIDEO_EXTENSIONS, AUDIO_EXTENSIONS,
    TRANSCRIPTION_SUFFIX, EXTENSION_TEXT
)


class FileManager:
    """Gestor centralizado de archivos."""

    @staticmethod
    def get_video_files() -> List[Path]:
        """Obtiene lista de videos en la carpeta video/ y subcarpetas."""
        videos = []
        for ext in VIDEO_EXTENSIONS:
            videos.extend(VIDEO_DIR.glob(f"**/*{ext}"))
        return sorted(videos)

    @staticmethod
    def get_audio_files() -> List[Path]:
        """Obtiene lista de archivos de audio en la carpeta mp3/ y subcarpetas."""
        audios = []
        for ext in AUDIO_EXTENSIONS:
            audios.extend(AUDIO_DIR.glob(f"**/*{ext}"))
        return sorted(audios)

    @staticmethod
    def get_transcription_path(source_file: Path) -> Path:
        """
        Obtiene la ruta del archivo de transcripción.
        
        Args:
            source_file: Ruta del archivo de origen (video o audio)
            
        Returns:
            Path: Ruta del archivo de transcripción
        """
        base_name = source_file.stem
        
        # Determinar si es video o audio para obtener la carpeta relativa
        try:
            if source_file.parent == VIDEO_DIR or source_file.parent == AUDIO_DIR:
                # Archivo en raíz
                return TEXT_DIR / f"{base_name}{TRANSCRIPTION_SUFFIX}{EXTENSION_TEXT}"
            else:
                # Archivo en subcarpeta, obtener la carpeta relativa
                if VIDEO_DIR in source_file.parents:
                    relative_folder = source_file.parent.relative_to(VIDEO_DIR)
                elif AUDIO_DIR in source_file.parents:
                    relative_folder = source_file.parent.relative_to(AUDIO_DIR)
                else:
                    # Fallback, asumir raíz
                    relative_folder = Path()
                
                return TEXT_DIR / relative_folder / f"{base_name}{TRANSCRIPTION_SUFFIX}{EXTENSION_TEXT}"
        except ValueError:
            # Archivo no en las carpetas esperadas, guardar en raíz
            return TEXT_DIR / f"{base_name}{TRANSCRIPTION_SUFFIX}{EXTENSION_TEXT}"

    @staticmethod
    def has_transcription(source_file: Path) -> bool:
        """
        Verifica si un archivo ya fue transcrito.
        
        Args:
            source_file: Ruta del archivo de origen
            
        Returns:
            bool: True si existe transcripción, False en caso contrario
        """
        transcription_path = FileManager.get_transcription_path(source_file)
        return transcription_path.exists()

    @staticmethod
    def list_items_with_status(
        items: List[Path], item_type: str = "video"
    ) -> List[Tuple[int, str, bool]]:
        """
        Crea una lista formateada de archivos con estado de transcripción.
        
        Args:
            items: Lista de rutas de archivos
            item_type: Tipo de elemento ("video" o "audio")
            
        Returns:
            List[Tuple[int, str, bool]]: Lista con (número, nombre con estado, ¿transcrito?)
        """
        result = []
        for idx, item in enumerate(items, 1):
            is_transcribed = FileManager.has_transcription(item)
            status = "✅ [TRANSCRITO]" if is_transcribed else "⏳ [PENDIENTE]"
            display_name = f"{status} {item.name}"
            result.append((idx, display_name, is_transcribed))
        return result

    @staticmethod
    def validate_file_exists(file_path: Path) -> bool:
        """Valida que el archivo existe."""
        return file_path.exists() and file_path.is_file()

    @staticmethod
    def get_file_size_mb(file_path: Path) -> float:
        """Obtiene el tamaño del archivo en MB."""
        if FileManager.validate_file_exists(file_path):
            return file_path.stat().st_size / (1024 * 1024)
        return 0.0

    @staticmethod
    def save_transcription(content: str, source_file: Path) -> Path:
        """
        Guarda la transcripción en archivo de texto.
        
        Args:
            content: Contenido de la transcripción
            source_file: Archivo de origen
            
        Returns:
            Path: Ruta del archivo guardado
        """
        output_path = FileManager.get_transcription_path(source_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding="utf-8")
        return output_path

    @staticmethod
    def get_extracted_audio_path(video_file: Path) -> Path:
        """Obtiene la ruta del audio extraído del video."""
        from src.config import AUDIO_SUFFIX
        base_name = video_file.stem
        
        # Determinar la carpeta relativa
        try:
            if video_file.parent == VIDEO_DIR:
                # Archivo en raíz
                return AUDIO_DIR / f"{base_name}{AUDIO_SUFFIX}.mp3"
            else:
                # Archivo en subcarpeta
                relative_folder = video_file.parent.relative_to(VIDEO_DIR)
                return AUDIO_DIR / relative_folder / f"{base_name}{AUDIO_SUFFIX}.mp3"
        except ValueError:
            # Video no está en VIDEO_DIR, guardar en raíz
            return AUDIO_DIR / f"{base_name}{AUDIO_SUFFIX}.mp3"

    @staticmethod
    def create_theme_folders(theme_name: str) -> None:
        """
        Crea las carpetas para un tema en video/, text/ y mp3/.
        
        Args:
            theme_name: Nombre del tema
        """
        (VIDEO_DIR / theme_name).mkdir(parents=True, exist_ok=True)
        (TEXT_DIR / theme_name).mkdir(parents=True, exist_ok=True)
        (AUDIO_DIR / theme_name).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def get_video_folders() -> List[Path]:
        """Obtiene lista de carpetas en video/."""
        return [p for p in VIDEO_DIR.iterdir() if p.is_dir()]

    @staticmethod
    def get_audio_folders() -> List[Path]:
        """Obtiene lista de carpetas en mp3/."""
        return [p for p in AUDIO_DIR.iterdir() if p.is_dir()]

    @staticmethod
    def get_text_folders() -> List[Path]:
        """Obtiene lista de carpetas en text/."""
        return [p for p in TEXT_DIR.iterdir() if p.is_dir()]
