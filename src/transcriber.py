"""
Módulo de transcripción usando OpenAI Whisper.
Maneja la extracción de audio y la transcripción de archivos.
"""

import warnings
from pathlib import Path
from typing import Optional, Dict, Any
import moviepy as mp
import whisper

from src.config import WHISPER_MODEL, WHISPER_LANGUAGE, VERBOSE
from src.file_manager import FileManager


class AudioTranscriber:
    """Transcriptor de audio usando OpenAI Whisper."""

    def __init__(self, model_name: str = WHISPER_MODEL):
        """
        Inicializa el transcriptor.
        
        Args:
            model_name: Modelo de Whisper a utilizar
        """
        self.model_name = model_name
        self.model = None

        # antes de hacer nada más, nos aseguramos de que ffmpeg esté disponible;
        # Whisper y MoviePy dependen de esta utilidad y el fallo era el que
        # aparecía en el menú al intentar transcribir un mp3 sin ffmpeg.
        self._ensure_ffmpeg()

        self._load_model()

    def _ensure_ffmpeg(self) -> None:
        """Verifica que `ffmpeg` esté disponible en el PATH.

        Whisper y MoviePy dependen de esta utilidad externa. El método intenta
        localizar el ejecutable por varios medios:

        1. `shutil.which` en el `PATH` actual.
        2. Búsqueda automática en la carpeta de WinGet, ya que en Windows el
           usuario suele instalar el paquete con `winget install ffmpeg`.

        Si encontramos el binario en la segunda opción, lo añadimos al `PATH`
        en tiempo de ejecución para que las llamadas posteriores lo detecten.
        En caso contrario, se lanza un `RuntimeError` con instrucciones.
        """
        import shutil
        import os

        # primer intento simple
        if shutil.which("ffmpeg"):
            return

        # segundo intento: escanear el directorio de WinGet para una instalación
        winget_root = os.path.join(os.environ.get("LOCALAPPDATA", ""),
                                   "Microsoft", "WinGet", "Packages")
        if os.path.isdir(winget_root):
            for root, dirs, files in os.walk(winget_root):
                if "ffmpeg.exe" in files:
                    candidate = os.path.join(root, "ffmpeg.exe")
                    bin_dir = os.path.dirname(candidate)
                    # agregar al PATH y revalidar
                    os.environ["PATH"] += os.pathsep + bin_dir
                    if shutil.which("ffmpeg"):
                        print(f"⚙️  Añadido ffmpeg al PATH: {bin_dir}")
                        return
                    # si no lo encuentra, continuar buscando
        # si seguimos aquí, no se ha detectado ningún ejecutable
        raise RuntimeError(
            "❌ ffmpeg no está instalado o no se encuentra en el PATH. "
            "Instale ffmpeg (por ejemplo via winget, brew, apt) y asegúrese de que "
            "la carpeta bin esté en la variable de entorno PATH."
        )

    def _load_model(self) -> None:
        """Carga el modelo de Whisper."""
        print(f"📥 Cargando modelo Whisper '{self.model_name}'...")
        try:
            self.model = whisper.load_model(self.model_name)
            print("✅ Modelo cargado exitosamente")
        except Exception as e:
            raise RuntimeError(f"❌ Error al cargar modelo: {e}")

    def extract_audio_from_video(self, video_path: Path) -> Path:
        """
        Extrae audio de un archivo de video.
        
        Args:
            video_path: Ruta del archivo de video
            
        Returns:
            Path: Ruta del archivo de audio extraído
            
        Raises:
            FileNotFoundError: Si el video no existe
            RuntimeError: Si hay error al extraer el audio
        """
        if not video_path.exists():
            raise FileNotFoundError(f"El archivo {video_path} no existe")

        audio_path = FileManager.get_extracted_audio_path(video_path)
        audio_path.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"\n--- 🎞️  Extrayendo audio del video ---")
        print(f"Video: {video_path.name}")
        print(f"Tamaño: {FileManager.get_file_size_mb(video_path):.2f} MB")
        
        try:
            import subprocess
            # Usar ffmpeg directamente para extraer audio
            cmd = [
                "ffmpeg",
                "-i", str(video_path),
                "-vn",  # No video
                "-acodec", "mp3",
                "-ab", "128k",
                "-y",  # Overwrite
                str(audio_path)
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print(f"✅ Audio guardado: {audio_path.name}")
            return audio_path
            
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"❌ Error al extraer audio: {e.stderr}")
        except Exception as e:
            raise RuntimeError(f"❌ Error al extraer audio: {e}")

    def transcribe_audio(
        self, audio_path: Path, language: str = WHISPER_LANGUAGE
    ) -> Dict[str, Any]:
        """
        Transcribe un archivo de audio.
        
        Args:
            audio_path: Ruta del archivo de audio
            language: Código de idioma (ej: 'es' para español)
            
        Returns:
            Dict: Resultado de la transcripción con clave 'text'
            
        Raises:
            FileNotFoundError: Si el audio no existe
            RuntimeError: Si hay error en la transcripción
        """
        if not audio_path.exists():
            raise FileNotFoundError(f"El archivo {audio_path} no existe")

        print(f"\n--- 🧠 Iniciando transcripción con Whisper ---")
        print(f"Audio: {audio_path.name}")
        print(f"Tamaño: {FileManager.get_file_size_mb(audio_path):.2f} MB")
        print(f"Idioma: {language}")
        print("Por favor espere, esto puede tomar varios minutos...")
        
        try:
            # Suprimir advertencia de FP16
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                resultado = self.model.transcribe(
                    str(audio_path),
                    verbose=VERBOSE,
                    language=language
                )
            return resultado
            
        except KeyboardInterrupt:
            print("\n⚠️  Transcripción cancelada por el usuario")
            raise
        except Exception as e:
            raise RuntimeError(f"❌ Error en la transcripción: {e}")

    def transcribe_video(self, video_path: Path) -> Optional[str]:
        """
        Flujo completo: extrae audio del video y transcribe.
        
        Args:
            video_path: Ruta del archivo de video
            
        Returns:
            str: Texto transcrito, o None si hay error
        """
        try:
            # Extraer audio
            audio_path = self.extract_audio_from_video(video_path)
            
            # Transcribir
            resultado = self.transcribe_audio(audio_path)
            
            # Guardar transcripción
            output_path = FileManager.save_transcription(
                resultado["text"], video_path
            )
            
            # Mostrar fragmento
            text_preview = resultado["text"][:300]
            print(f"\n✅ Transcripción completada exitosamente!")
            print(f"📄 Archivo guardado: {output_path.name}")
            print(f"\nFragmento:\n{text_preview}...\n")
            
            return resultado["text"]
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            return None

    def transcribe_audio_file(self, audio_path: Path) -> Optional[str]:
        """
        Transcribe un archivo de audio.
        
        Args:
            audio_path: Ruta del archivo de audio
            
        Returns:
            str: Texto transcrito, o None si hay error
        """
        try:
            resultado = self.transcribe_audio(audio_path)
            
            # Guardar transcripción
            output_path = FileManager.save_transcription(
                resultado["text"], audio_path
            )
            
            # Mostrar fragmento
            text_preview = resultado["text"][:300]
            print(f"\n✅ Transcripción completada exitosamente!")
            print(f"📄 Archivo guardado: {output_path.name}")
            print(f"\nFragmento:\n{text_preview}...\n")
            
            return resultado["text"]
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            return None
