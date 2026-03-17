#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Aplicación de Transcripción de Video/Audio.

Permite transcribir videos o archivos de audio directamente a texto
utilizando OpenAI Whisper.

Uso:
    python main.py
"""

import sys
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent))

from src.menu import Menu


def main():
    """Función principal de la aplicación."""
    try:
        menu = Menu()
        menu.run()
    except KeyboardInterrupt:
        print("\n\n⚠️  Aplicación interrumpida por el usuario.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
