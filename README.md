# 🎬 Sistema de Transcripción de Video/Audio

Aplicación interactiva para transcribir videos y archivos de audio a texto usando OpenAI Whisper.

---

## 📋 ¿Qué hace este proyecto?

Convierte automáticamente videos o archivos de audio en texto mediante un **menú interactivo** que:
- Selecciona archivos de forma visual
- Muestra el estado de transcripción (✅ Transcrito / ⏳ Pendiente)
- Guarda las transcripciones organizadas
- Evita duplicados confirmando antes de retranscribir

---

## 🚀 Instalación Rápida

### 1. Requisitos Previos
- **Python 3.8+**
- **FFmpeg** (para procesar video/audio)

### 2. Instalar FFmpeg
```bash
# Windows
winget install ffmpeg

# macOS
brew install ffmpeg

# Linux
sudo apt-get install ffmpeg
```

### 3. Configurar el Proyecto
```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt
```

### 4. Ejecutar
```bash
python main.py
```

---

## 📁 Estructura del Proyecto

```
transcripcion/
│
├── src/                    # Código fuente modular
│   ├── config.py          # Configuración (rutas, modelos)
│   ├── file_manager.py    # Gestión de archivos
│   ├── transcriber.py     # Lógica de transcripción
│   ├── menu.py            # Menú interactivo
│   └── __init__.py
│
├── video/                  # 📁 Coloca aquí los videos
├── mp3/                    # 🎵 Coloca aquí los audios
├── text/                   # 📄 Transcripciones (auto-generadas)
│
├── main.py                 # ⭐ Ejecuta esto
├── requirements.txt        # Dependencias
├── test_structure.py       # Validar proyecto
├── example_usage.py        # Ejemplos de código
└── README.md              # Este archivo
```

---

## 🎯 Guía del Menú

### Pantalla Principal
```
============================================================
          🎬 SISTEMA DE TRANSCRIPCIÓN DE VIDEO/AUDIO
============================================================

Seleccione una opción:

  [1] Transcribir VIDEO
  [2] Transcribir AUDIO MP3
  [3] Ver archivos de TEXTO
  [0] Salir

👉 Opción: 
```

### Opción 1: Transcribir VIDEO

1. Muestra todos los videos en `video/`
2. Indica el estado:
   ```
   [1] ⏳ [PENDIENTE] Clase I.mp4
   [2] ✅ [TRANSCRITO] Clase II.mp4
   ```
3. Selecciona un número
4. El sistema:
   - Extrae el audio del video
   - Transcribe con Whisper
   - Guarda en `text/nombre_transcripcion.txt`

### Opción 2: Transcribir AUDIO

1. Muestra todos los audios en `mp3/`
2. Selecciona uno
3. Transcribe directamente (sin necesidad de extraer audio)

### Opción 3: Ver Transcripciones

1. Lista todas las transcripciones en `text/`
2. Muestra tamaño y número de líneas
3. Permite leer el contenido completo

---

## 💡 Ejemplos de Uso

### Uso Básico
```bash
# 1. Coloca videos en video/
# 2. Ejecuta la aplicación
python main.py

# 3. Selecciona opción 1
# 4. Selecciona el video
# 5. Espera (puede tomar 10-30 min en CPU)
# 6. ¡Listo! Revisa text/
```

### Uso Programático
```python
from src.transcriber import AudioTranscriber
from pathlib import Path

# Transcribir un video
transcriber = AudioTranscriber()
video = Path("video/mi_video.mp4")
texto = transcriber.transcribe_video(video)

# Verificar si ya está transcrito
from src.file_manager import FileManager
if FileManager.has_transcription(video):
    print("Ya está transcrito")
```

### Validar el Proyecto
```bash
# Ver estructura y archivos
python test_structure.py

# Ver ejemplos de código
python example_usage.py
```

---

## ⚙️ Configuración

Edita `src/config.py` para personalizar:

```python
# Modelo de Whisper (tiny, base, small, medium, large)
WHISPER_MODEL = "base"  # Cambia aquí

# Idioma
WHISPER_LANGUAGE = "es"  # Español

# Rutas (auto-configuradas)
VIDEO_DIR = "video/"
AUDIO_DIR = "mp3/"
TEXT_DIR = "text/"
```

**Modelos disponibles:**
- `tiny` (39MB) - ⚡ Muy rápido, baja precisión
- `base` (140MB) - ⚡ Rápido, buena precisión (recomendado)
- `small` (466MB) - Normal, alta precisión
- `medium` (1.5GB) - Lento, muy alta precisión
- `large` (3GB) - Muy lento, precisión perfecta

---

## 🏗️ Arquitectura

El proyecto usa **arquitectura modular** para facilitar mantenimiento:

| Módulo | Responsabilidad |
|--------|-----------------|
| `config.py` | Configuración centralizada |
| `file_manager.py` | Listar, validar y guardar archivos |
| `transcriber.py` | Extraer audio y transcribir |
| `menu.py` | Interfaz de usuario |
| `main.py` | Punto de entrada |

**Ventajas:**
- ✅ Fácil de mantener
- ✅ Fácil de extender
- ✅ Código reutilizable
- ✅ Separación de responsabilidades

---

## ❓ Solución de Problemas

### FFmpeg no encontrado
```bash
# Instalar FFmpeg
winget install ffmpeg

# Reiniciar terminal
# Verificar
ffmpeg -version
```

### Transcripción muy lenta
- Es normal en CPU (20-30 minutos por video)
- Usa modelo más pequeño: `WHISPER_MODEL = "tiny"`
- Considera usar GPU (requiere configuración adicional)

### Error de módulos
```bash
# Reinstalar dependencias
pip install -r requirements.txt
```

### Video sin audio
El sistema verifica que el video tenga audio. Si no tiene, mostrará error.

---

## 📊 Características Técnicas

- **Lenguaje:** Python 3.8+
- **Transcripción:** OpenAI Whisper
- **Video:** MoviePy
- **Type hints:** Sí
- **Docstrings:** Sí
- **Tests:** Incluidos
- **Modular:** Sí

---

## 📝 Notas

- La primera vez descarga el modelo Whisper (~140MB)
- El tiempo depende del tamaño del archivo y CPU
- Funciona sin GPU (más lento pero funcional)
- Soporta múltiples formatos: MP4, AVI, MOV, MP3, WAV, M4A, etc.

---

## 📄 Licencia

Este proyecto está bajo licencia MIT.
