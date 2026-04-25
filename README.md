# Video Audio Replacer

Aplicacion web local para cargar un video MP4, cargar un audio MP3 y generar un nuevo archivo MP4 que conserva el video original pero reemplaza su audio por el MP3 elegido.

## Requisitos

- Python 3.10 o superior.
- FFmpeg instalado y disponible en el `PATH`.
- Navegador web moderno.

La aplicacion puede arrancar aunque FFmpeg no este instalado. FFmpeg solo es obligatorio al pulsar `Generar video final`.

## Instalacion

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Configuracion con .env

Puedes crear un archivo `.env` en la raiz del proyecto para ajustar la configuracion local. El archivo `.env` no se versiona.

Variables disponibles:

- `FLASK_HOST`: direccion donde Flask escucha conexiones.
- `FLASK_PORT`: puerto local de Flask.
- `FLASK_DEBUG`: activa (`1`) o desactiva (`0`) el modo debug.
- `MAX_VIDEO_MB`: tamano maximo permitido para el video MP4.
- `MAX_AUDIO_MB`: tamano maximo permitido para el audio MP3.
- `FFMPEG_BINARY`: nombre o ruta del binario de FFmpeg.
- `OUTPUT_PREFIX`: prefijo usado para nombrar los videos generados.

Ejemplo minimo:

```env
FLASK_HOST=127.0.0.1
FLASK_PORT=5000
FLASK_DEBUG=1
MAX_VIDEO_MB=500
MAX_AUDIO_MB=100
FFMPEG_BINARY=ffmpeg
OUTPUT_PREFIX=video-final
```

Tambien puedes copiar `.env.example` como punto de partida.

## Uso rapido

```bash
python app.py
```

Luego abre:

```text
http://127.0.0.1:5000
```

Flujo del MVP:

1. Seleccionar video MP4. Se sube automaticamente.
2. Seleccionar audio MP3. Se sube automaticamente.
3. Ajustar el retraso del audio si es necesario.
4. Pulsar `Generar video final`.
5. Descargar el MP4 generado.

Nota: Este MVP reemplaza el audio desde el inicio. La sincronizacion fina se abordara en futuras versiones.

## Comando FFmpeg usado

```bash
ffmpeg -i video_original.mp4 -i audio_nuevo.mp3 -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -movflags +faststart -shortest salida_final.mp4
```

La implementacion usa el mismo flujo y agrega `-y` para permitir que FFmpeg escriba el archivo de salida generado automaticamente. Los nombres de salida son unicos y usan `OUTPUT_PREFIX`, por lo que no deberia sobrescribir resultados anteriores.

## Limitaciones actuales

- Solo acepta video `.mp4`.
- Solo acepta audio `.mp3`.
- No hay barra de progreso real de FFmpeg, solo estados basicos.
- El procesamiento se ejecuta en la misma peticion HTTP.
- No hay base de datos ni historial persistente.
- No se limpian automaticamente archivos antiguos de `storage`.
- No incluye descarga desde YouTube en esta fase.
- No incluye sincronizacion automatica o ajuste fino entre audio y video.

## Mejoras futuras

- Soporte para URL de YouTube usando `yt-dlp`.
- Barra de progreso basada en salida de FFmpeg.
- Limpieza automatica de archivos temporales y resultados antiguos.
- Vista de historial local de resultados generados.
- Opciones para mantener duracion completa de video o audio segun preferencia.
