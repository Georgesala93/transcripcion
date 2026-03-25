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
        print(MENU_OPTION_FORMAT.format(num=4, text="Crear nueva carpeta de tema"))
        print(MENU_OPTION_FORMAT.format(num=0, text="Salir"))
        print()

    def display_video_menu(self, selected_folder: Optional[Path] = None) -> None:
        """Muestra menú de selección de videos."""
        self.print_header("SELECCIONAR VIDEO")
        
        if selected_folder:
            videos = [f for f in FileManager.get_video_files() if f.parent == selected_folder]
            folder_name = selected_folder.name
        else:
            videos = FileManager.get_video_files()
            folder_name = "todas las carpetas"
        
        if not videos:
            print(f"⚠️  No hay videos disponibles en {folder_name}")
            input("\nPresione Enter para continuar...")
            return None
        
        items = FileManager.list_items_with_status(videos, "video")
        print(f"\nEncontrados {len(videos)} video(s) en {folder_name}:\n")
        
        for num, display_name, _ in items:
            print(MENU_OPTION_FORMAT.format(num=num, text=display_name))
        
        print(MENU_OPTION_FORMAT.format(num=0, text="Volver al menú principal"))
        print()
        
        return videos, items

    def display_audio_menu(self, selected_folder: Optional[Path] = None) -> None:
        """Muestra menú de selección de audios."""
        self.print_header("SELECCIONAR AUDIO MP3")
        
        if selected_folder:
            audios = [f for f in FileManager.get_audio_files() if f.parent == selected_folder]
            folder_name = selected_folder.name
        else:
            audios = FileManager.get_audio_files()
            folder_name = "todas las carpetas"
        
        if not audios:
            print(f"⚠️  No hay archivos MP3 disponibles en {folder_name}")
            input("\nPresione Enter para continuar...")
            return None
        
        items = FileManager.list_items_with_status(audios, "audio")
        print(f"\nEncontrados {len(audios)} archivo(s) de audio en {folder_name}:\n")
        
        for num, display_name, _ in items:
            print(MENU_OPTION_FORMAT.format(num=num, text=display_name))
        
        print(MENU_OPTION_FORMAT.format(num=0, text="Volver al menú principal"))
        print()
        
        return audios, items

    def display_text_menu(self) -> None:
        """Muestra los archivos de texto generados."""
        self.print_header("ARCHIVOS DE TRANSCRIPCIÓN")
        
        folders = FileManager.get_text_folders()
        
        if not folders:
            print("\n⚠️  No hay carpetas de tema en text/.")
            input("Presione Enter para continuar...")
            return
        
        print("\nCarpetas disponibles:\n")
        
        for idx, folder in enumerate(folders, 1):
            transcription_files = list(folder.glob("*_transcripcion.txt"))
            print(MENU_OPTION_FORMAT.format(num=idx, text=f"{folder.name} ({len(transcription_files)} transcripción(es))"))
        
        print(MENU_OPTION_FORMAT.format(num=0, text="Volver al menú principal"))
        print()
        
        choice = self._get_valid_input(0, len(folders))
        
        if choice == 0:
            return
        
        selected_folder = folders[choice - 1]
        transcriptions = sorted(selected_folder.glob("*_transcripcion.txt"))
        
        if not transcriptions:
            print(f"\n⚠️  No hay transcripciones en la carpeta '{selected_folder.name}'.\n")
            input("Presione Enter para continuar...")
            return
        
        self.print_header(f"TRANSCRIPCIONES - {selected_folder.name}")
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
        # Mostrar carpetas disponibles
        folders = FileManager.get_video_folders()
        
        if not folders:
            print("⚠️  No hay carpetas de tema en video/. Use la opción 4 para crear una.")
            input("\nPresione Enter para continuar...")
            return
        
        self.print_header("SELECCIONAR CARPETA DE VIDEO")
        print("\nCarpetas disponibles:\n")
        
        for idx, folder in enumerate(folders, 1):
            video_count = len([f for f in FileManager.get_video_files() if f.parent == folder])
            print(MENU_OPTION_FORMAT.format(num=idx, text=f"{folder.name} ({video_count} video(s))"))
        
        print(MENU_OPTION_FORMAT.format(num=0, text="Volver al menú principal"))
        print()
        
        choice = self._get_valid_input(0, len(folders))
        
        if choice == 0:
            return
        
        selected_folder = folders[choice - 1]
        
        # Mostrar videos en la carpeta seleccionada
        result = self.display_video_menu(selected_folder)
        
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
        # Mostrar carpetas disponibles
        folders = FileManager.get_audio_folders()
        
        if not folders:
            print("⚠️  No hay carpetas de tema en mp3/. Use la opción 4 para crear una.")
            input("\nPresione Enter para continuar...")
            return
        
        self.print_header("SELECCIONAR CARPETA DE AUDIO")
        print("\nCarpetas disponibles:\n")
        
        for idx, folder in enumerate(folders, 1):
            audio_count = len([f for f in FileManager.get_audio_files() if f.parent == folder])
            print(MENU_OPTION_FORMAT.format(num=idx, text=f"{folder.name} ({audio_count} audio(s))"))
        
        print(MENU_OPTION_FORMAT.format(num=0, text="Volver al menú principal"))
        print()
        
        choice = self._get_valid_input(0, len(folders))
        
        if choice == 0:
            return
        
        selected_folder = folders[choice - 1]
        
        # Mostrar audios en la carpeta seleccionada
        result = self.display_audio_menu(selected_folder)
        
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

    def process_create_folder_option(self) -> None:
        """Procesa la opción de crear nueva carpeta de tema."""
        self.print_header("CREAR NUEVA CARPETA DE TEMA")
        
        theme_name = input("Ingrese el nombre del tema: ").strip()
        
        if not theme_name:
            print("❌ El nombre del tema no puede estar vacío.")
            input("\nPresione Enter para continuar...")
            return
        
        # Validar caracteres inválidos para nombres de carpeta
        invalid_chars = ['<', '>', ':', '"', '|', '?', '*']
        if any(char in theme_name for char in invalid_chars):
            print("❌ El nombre del tema contiene caracteres inválidos.")
            input("\nPresione Enter para continuar...")
            return
        
        try:
            FileManager.create_theme_folders(theme_name)
            print(f"✅ Carpetas creadas exitosamente para el tema '{theme_name}' en video/, text/ y mp3/.")
        except Exception as e:
            print(f"❌ Error al crear las carpetas: {e}")
        
        input("\nPresione Enter para continuar...")

    def run(self) -> None:
        """Ejecuta el menú principal."""
        while self.running:
            self.display_main_menu()
            choice = self._get_valid_input(0, 4)
            
            if choice == 0:
                print("\n👋 ¡Hasta luego!\n")
                self.running = False
            elif choice == 1:
                self.process_video_option()
            elif choice == 2:
                self.process_audio_option()
            elif choice == 3:
                self.display_text_menu()
            elif choice == 4:
                self.process_create_folder_option()
