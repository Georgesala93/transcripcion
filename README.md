# 🎬 Sistema de Transcripción de Video/Audio

Aplicación interactiva para transcribir videos y archivos de audio a texto usando OpenAI Whisper.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📋 ¿Qué hace este proyecto?

Convierte automáticamente videos o archivos de audio en texto mediante un **menú interactivo** que:
- ✅ Selecciona archivos de forma visual
- 📊 Muestra el estado de transcripción (✅ Transcrito / ⏳ Pendiente)
- 💾 Guarda las transcripciones organizadas por carpetas
- 🔄 Evita duplicados confirmando antes de retranscribir
- 🎯 Soporta múltiples formatos (MP4, MP3, WAV, etc.)

---

## 🏗️ Arquitectura del Proyecto

```
transcripcion/
├── 📁 src/                    # Módulos principales
│   ├── __init__.py           # Inicialización del paquete
│   ├── config.py             # Configuraciones del proyecto
│   ├── file_manager.py       # Gestión de archivos y directorios
│   ├── menu.py               # Interfaz de menú interactivo
│   └── transcriber.py        # Lógica de transcripción con Whisper
├── 📁 tests/                 # Tests unitarios
│   ├── test_menu.py          # Tests del menú
│   └── test_transcriber.py   # Tests del transcriptor
├── 📁 scripts/               # Scripts de desarrollo y utilidades
│   ├── setup_windows.py      # Instalador automático para Windows
│   ├── test_structure.py     # Verificación de estructura del proyecto
│   ├── validate.py           # Validación completa de módulos
│   ├── inspect_moviepy.py    # Inspección de MoviePy
│   └── test_audio.py         # Tests de procesamiento de audio
├── 📁 media/                 # Archivos del usuario (no versionados)
│   ├── mp3/                  # Archivos de audio para transcribir
│   ├── video/                # Archivos de video para transcribir
│   └── text/                 # Transcripciones generadas automáticamente
├── 📄 main.py                # Punto de entrada principal
├── 📄 example_usage.py       # Ejemplos de uso programático
├── 📄 requirements.txt       # Dependencias del proyecto
├── 📄 .gitignore            # Archivos ignorados por Git
└── 📄 README.md             # Esta documentación
```

---

## 🚀 Instalación y Configuración

### 1. Requisitos Previos
- **Python 3.8 o superior**
- **FFmpeg** (para procesar video/audio)
- **Git** (para clonar el repositorio)

### 2. Instalar FFmpeg
```bash
# Windows (PowerShell como Administrador)
winget install ffmpeg

# macOS
brew install ffmpeg

# Linux (Ubuntu/Debian)
sudo apt-get update && sudo apt-get install ffmpeg

# Verificar instalación
ffmpeg -version
```

### 3. Clonar y Configurar el Proyecto
```bash
# Clonar repositorio
git clone https://github.com/Georgesala93/transcripcion.git
cd transcripcion

# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 4. Verificar Instalación
```bash
# Ejecutar validación completa
python scripts/validate.py

# O verificar estructura del proyecto
python scripts/test_structure.py
```

---

## 🎯 Uso Básico

### Modo Interactivo (Recomendado)
```bash
python main.py
```
Esto abrirá un menú interactivo donde podrás:
1. Ver archivos disponibles para transcribir
2. Seleccionar archivos para procesar
3. Ver el progreso de la transcripción
4. Revisar transcripciones generadas

### Uso Programático
```python
from src.file_manager import FileManager
from src.transcriber import AudioTranscriber

# Ver archivos disponibles
videos = FileManager.get_video_files()
audios = FileManager.get_audio_files()

# Crear transcriptor
transcriber = AudioTranscriber()

# Transcribir un archivo
transcription = transcriber.transcribe_audio("ruta/al/archivo.mp3")
```

Ver `example_usage.py` para más ejemplos detallados.

---

## 📁 Estructura de Archivos

### Archivos de Entrada (Usuario)
Coloca tus archivos en estas carpetas:
- `media/mp3/` - Archivos de audio (.mp3, .wav, .ogg, .m4a)
- `media/video/` - Archivos de video (.mp4, .mkv, .avi, .mov)

### Archivos de Salida (Generados)
Las transcripciones se guardan automáticamente en:
- `media/text/` - Archivos de texto con las transcripciones

### Ejemplo de Organización
```
media/
├── mp3/
│   ├── leccion1.mp3
│   └── leccion2.wav
├── video/
│   ├── clase1.mp4
│   └── clase2.mkv
└── text/
    ├── leccion1_transcripcion.txt
    ├── leccion2_transcripcion.txt
    ├── clase1_transcripcion.txt
    └── clase2_transcripcion.txt
```

---

## 🛠️ Scripts Disponibles

### Instalación
- `scripts/setup_windows.py` - Instalador automático para Windows

### Validación y Tests
- `scripts/validate.py` - Validación completa de todos los módulos
- `scripts/test_structure.py` - Verificación de estructura del proyecto
- `scripts/test_audio.py` - Tests específicos de procesamiento de audio

### Utilidades
- `scripts/inspect_moviepy.py` - Inspección y debugging de MoviePy

### Ejecutar Scripts
```bash
# Desde la raíz del proyecto
python scripts/validate.py
python scripts/test_structure.py
```

---

## 🧪 Ejecutar Tests

```bash
# Instalar pytest si no está incluido
pip install pytest

# Ejecutar todos los tests
pytest tests/

# Ejecutar tests específicos
pytest tests/test_menu.py
pytest tests/test_transcriber.py

# Con cobertura
pytest --cov=src tests/
```

---

## 🔧 Desarrollo

### Configuración para Desarrolladores
```bash
# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt  # Si existe

# Ejecutar validación antes de commits
python scripts/validate.py

# Ver estructura del proyecto
python scripts/test_structure.py
```

### Contribuir
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

---

## 📋 Dependencias

### Principales
- `openai-whisper` - Motor de transcripción con IA
- `moviepy` - Procesamiento de video/audio
- `torch` - Framework de machine learning
- `numpy` - Computación numérica

### De Desarrollo
- `pytest` - Framework de testing
- `pytest-cov` - Cobertura de tests

Ver `requirements.txt` para versiones específicas.

---

## ❓ Solución de Problemas

### Error: "ffmpeg no encontrado"
```bash
# Verificar instalación
ffmpeg -version

# Reinstalar si es necesario
winget install ffmpeg  # Windows
```

### Error: "No module named 'whisper'"
```bash
# Asegurar que el entorno virtual esté activado
.venv\Scripts\activate  # Windows

# Reinstalar dependencias
pip install -r requirements.txt
```

### Error: "CUDA out of memory"
- El modelo de Whisper puede requerir mucha memoria GPU
- Usa un modelo más pequeño: modifica `config.py`
- O ejecuta en CPU: `torch.device('cpu')`

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

## 👥 Autor

**Jorge Sala** - [Georgesala93](https://github.com/Georgesala93)

---

## 🙏 Agradecimientos

- OpenAI por Whisper
- Comunidad de Python por las librerías utilizadas
- Contribuidores del proyecto

---

*Última actualización: Abril 2026*
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
├── media/                  # 📂 Carpeta contenedora de contenido
│   ├── video/             # 📁 Coloca aquí los videos
│   ├── mp3/               # 🎵 Coloca aquí los audios
│   └── text/              # 📄 Transcripciones (auto-generadas)
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

1. Muestra todos los videos en `media/video/`
2. Indica el estado:
   ```
   [1] ⏳ [PENDIENTE] Clase I.mp4
   [2] ✅ [TRANSCRITO] Clase II.mp4
   ```
3. Selecciona un número
4. El sistema:
   - Extrae el audio del video
   - Transcribe con Whisper
   - Guarda en `media/text/nombre_transcripcion.txt`

### Opción 2: Transcribir AUDIO

1. Muestra todos los audios en `media/mp3/`
2. Selecciona uno
3. Transcribe directamente (sin necesidad de extraer audio)

### Opción 3: Ver Transcripciones

1. Lista todas las transcripciones en `media/text/`
2. Muestra tamaño y número de líneas
3. Permite leer el contenido completo

---

## 💡 Ejemplos de Uso

### Uso Básico
```bash
# 1. Coloca videos en media/video/
# 2. Ejecuta la aplicación
python main.py

# 3. Selecciona opción 1
# 4. Selecciona el video
# 5. Espera (puede tomar 10-30 min en CPU)
# 6. ¡Listo! Revisa media/text/
```

### Uso Programático
```python
from src.transcriber import AudioTranscriber
from pathlib import Path

# Transcribir un video
transcriber = AudioTranscriber()
video = Path("media/video/mi_video.mp4")
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
MEDIA_DIR = BASE_DIR / "media"
VIDEO_DIR = MEDIA_DIR / "video"
AUDIO_DIR = MEDIA_DIR / "mp3"
TEXT_DIR = MEDIA_DIR / "text"
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
