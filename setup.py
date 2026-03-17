#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de instalación rápida para Windows.
Configura el entorno y todas las dependencias necesarias.
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """Ejecuta un comando y muestra el resultado."""
    print(f"\n{'=' * 60}")
    print(f"📦 {description}")
    print(f"{'=' * 60}")
    try:
        subprocess.run(cmd, shell=True, check=True)
        print(f"✅ {description} - Completado\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}\n")
        return False


def main():
    """Función principal de instalación."""
    print("\n" + "=" * 60)
    print(" 🚀 INSTALACIÓN DE TRANSCRIPCIÓN DE VIDEO/AUDIO")
    print("=" * 60)
    
    # Paso 1: Crear entorno virtual
    if not Path(".venv").exists():
        if not run_command("python -m venv .venv", "Creando entorno virtual"):
            print("❌ Fallo en la creación del entorno virtual")
            return
    else:
        print("✅ Entorno virtual ya existe")
    
    # Paso 2: Instalar dependencias
    pip_cmd = ".venv\\Scripts\\pip.exe install -r requirements.txt"
    if not run_command(pip_cmd, "Instalando dependencias"):
        print("❌ Fallo en la instalación de dependencias")
        return
    
    # Paso 3: Instalar FFmpeg
    print(f"\n{'=' * 60}")
    print(" 🎬 FFmpeg - Gestor de video/audio")
    print(f"{'=' * 60}")
    print("\nFFmpeg es necesario para procesar video y audio.")
    print("¿Desea instalarlo ahora? (s/n): ", end="")
    
    if input().lower() == "s":
        if not run_command("winget install ffmpeg", "Instalando FFmpeg"):
            print("⚠️  No se pudo instalar FFmpeg automáticamente.")
            print("   Descárgalo en: https://ffmpeg.org/")
            print("   O ejecuta: winget install ffmpeg")
    
    print("\n" + "=" * 60)
    print(" ✅ INSTALACIÓN COMPLETADA")
    print("=" * 60)
    print("\n🎉 Para iniciar la aplicación, ejecuta:")
    print("   python main.py\n")


if __name__ == "__main__":
    main()
