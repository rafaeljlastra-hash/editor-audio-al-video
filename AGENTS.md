# AGENTS.md

Guia rapida para trabajar en este repositorio con Codex.

## Proyecto

Aplicacion web local para reemplazar el audio de un video MP4 por un audio MP3 y generar un MP4 final descargable.

## Stack

- Python
- Flask
- FFmpeg via `subprocess`
- HTML/CSS/JS simple

## Estructura

- `routes/`: endpoints Flask para subida, procesado y descarga.
- `services/`: validacion, archivos y ejecucion de FFmpeg.
- `templates/`: HTML de la interfaz.
- `static/`: CSS y JavaScript.
- `storage/`: archivos subidos, temporales y resultados locales.

## Flujo Funcional

1. Seleccionar MP4 -> auto-subida.
2. Seleccionar MP3 -> auto-subida.
3. Ajustar delay opcional.
4. Generar MP4 final.
5. Descargar resultado.

## Reglas

- No versionar `.env`.
- No tocar `storage/` salvo que el usuario lo pida explicitamente.
- No anadir archivos generados al repositorio.
- Mantener separacion entre `routes/` y `services/`.
- Usar `secure_filename` para nombres de archivo.
- No implementar YouTube hasta nueva orden.
- No cambiar la logica FFmpeg sin justificacion clara.

## Ejecucion

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python app.py
```
