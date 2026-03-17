"""
Menú interactivo para la aplicación de transcripción.
Maneja la interfaz de usuario y selección de opciones.
"""

from typing import Optional, Callable
from pathlib import Path
from src.config import MENU_SEPARATOR, MENU_OPTION_FORMAT
from src.file_manager import FileManager
from src.transcriber import AudioTranscriber


class Menu:
    """Menú interactivo de la aplicación."""

    def __init__(self):
        """Inicializa el menú y el transcriptor."""
        self.transcriber = AudioTranscriber()
        self.running = True

    def clear_screen(self) -> None:
        """Limpia la pantalla."""
        import os
        os.system("cls" if os.name == "nt" else "clear")

    def print_header(self, title: str) -> None:
        """Imprime un encabezado."""
        print(f"\n{MENU_SEPARATOR}")
        print(f" 🎬 {title}".center(60))
        print(MENU_SEPARATOR)

    def display_main_menu(self) -> None:
        """Muestra el menú principal."""
        self.clear_screen()
        self.print_header("SISTEMA DE TRANSCRIPCIÓN DE VIDEO/AUDIO")
        
        print("\nSeleccione una opción:\n")
        print(MENU_OPTION_FORMAT.format(num=1, text="Transcribir VIDEO"))
        print(MENU_OPTION_FORMAT.format(num=2, text="Transcribir AUDIO MP3"))
        print(MENU_OPTION_FORMAT.format(num=3, text="Ver archivos de TEXTO"))
        print(MENU_OPTION_FORMAT.format(num=0, text="Salir"))
        print()

    def display_video_menu(self) -> None:
        """Muestra menú de selección de videos."""
        self.print_header("SELECCIONAR VIDEO")
        
        videos = FileManager.get_video_files()
        
        if not videos:
            print("⚠️  No hay videos disponibles en la carpeta 'video/'")
            input("\nPresione Enter para continuar...")
            return None
        
        items = FileManager.list_items_with_status(videos, "video")
        print(f"\nEncontrados {len(videos)} video(s):\n")
        
        for num, display_name, _ in items:
            print(MENU_OPTION_FORMAT.format(num=num, text=display_name))
        
        print(MENU_OPTION_FORMAT.format(num=0, text="Volver al menú principal"))
        print()
        
        return videos, items

    def display_audio_menu(self) -> None:
        """Muestra menú de selección de audios."""
        self.print_header("SELECCIONAR AUDIO MP3")
        
        audios = FileManager.get_audio_files()
        
        if not audios:
            print("⚠️  No hay archivos MP3 disponibles en la carpeta 'mp3/'")
            input("\nPresione Enter para continuar...")
            return None
        
        items = FileManager.list_items_with_status(audios, "audio")
        print(f"\nEncontrados {len(audios)} archivo(s) de audio:\n")
        
        for num, display_name, _ in items:
            print(MENU_OPTION_FORMAT.format(num=num, text=display_name))
        
        print(MENU_OPTION_FORMAT.format(num=0, text="Volver al menú principal"))
        print()
        
        return audios, items

    def display_text_menu(self) -> None:
        """Muestra los archivos de texto generados."""
        self.print_header("ARCHIVOS DE TRANSCRIPCIÓN")
        
        from src.config import TEXT_DIR
        transcriptions = sorted(TEXT_DIR.glob(f"*_transcripcion.txt"))
        
        if not transcriptions:
            print("\n⚠️  No hay transcripciones generadas aún.\n")
            input("Presione Enter para continuar...")
            return
        
        print(f"\nEncontradas {len(transcriptions)} transcripción(es):\n")
        
        for idx, trans_file in enumerate(transcriptions, 1):
            size_kb = trans_file.stat().st_size / 1024
            num_lines = len(trans_file.read_text(encoding="utf-8").split("\n"))
            print(f"  [{idx}] 📄 {trans_file.name}")
            print(f"      Tamaño: {size_kb:.2f} KB | Líneas: {num_lines}")
        
        print(f"\n  [0] Volver al menú principal\n")
        
        option = self._get_valid_input(0, len(transcriptions))
        
        if option > 0:
            selected_trans = transcriptions[option - 1]
            self._display_transcription_content(selected_trans)

    def _display_transcription_content(self, file_path: Path) -> None:
        """Muestra el contenido de un archivo de transcripción."""
        self.clear_screen()
        print(f"\n{MENU_SEPARATOR}")
        print(f" 📖 {file_path.name}".center(60))
        print(MENU_SEPARATOR)
        
        content = file_path.read_text(encoding="utf-8")
        print(f"\n{content}\n")
        
        input("Presione Enter para volver...")

    def _get_valid_input(self, min_val: int, max_val: int) -> int:
        """
        Obtiene un input válido del usuario.
        
        Args:
            min_val: Valor mínimo
            max_val: Valor máximo
            
        Returns:
            int: Opción seleccionada
        """
        while True:
            try:
                choice = int(input("👉 Opción: ").strip())
                if min_val <= choice <= max_val:
                    return choice
                print(f"❌ Ingrese un número entre {min_val} y {max_val}")
            except ValueError:
                print("❌ Ingrese un número válido")

    def process_video_option(self) -> None:
        """Procesa la opción de transcribir video."""
        result = self.display_video_menu()
        if result is None:
            return
        
        videos, items = result
        choice = self._get_valid_input(0, len(videos))
        
        if choice == 0:
            return
        
        selected_video = videos[choice - 1]
        is_transcribed = items[choice - 1][2]
        
        if is_transcribed:
            print(f"\n⚠️  Este video ya fue transcrito.")
            confirm = input("¿Desea transcribir nuevamente? (s/n): ").lower()
            if confirm != "s":
                input("\nPresione Enter para continuar...")
                return
        
        print()
        self.transcriber.transcribe_video(selected_video)
        input("\nPresione Enter para continuar...")

    def process_audio_option(self) -> None:
        """Procesa la opción de transcribir audio."""
        result = self.display_audio_menu()
        if result is None:
            return
        
        audios, items = result
        choice = self._get_valid_input(0, len(audios))
        
        if choice == 0:
            return
        
        selected_audio = audios[choice - 1]
        is_transcribed = items[choice - 1][2]
        
        if is_transcribed:
            print(f"\n⚠️  Este audio ya fue transcrito.")
            confirm = input("¿Desea transcribir nuevamente? (s/n): ").lower()
            if confirm != "s":
                input("\nPresione Enter para continuar...")
                return
        
        print()
        self.transcriber.transcribe_audio_file(selected_audio)
        input("\nPresione Enter para continuar...")

    def run(self) -> None:
        """Ejecuta el menú principal."""
        while self.running:
            self.display_main_menu()
            choice = self._get_valid_input(0, 3)
            
            if choice == 0:
                print("\n👋 ¡Hasta luego!\n")
                self.running = False
            elif choice == 1:
                self.process_video_option()
            elif choice == 2:
                self.process_audio_option()
            elif choice == 3:
                self.display_text_menu()
