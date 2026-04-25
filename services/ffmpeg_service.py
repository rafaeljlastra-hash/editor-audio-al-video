import subprocess
from pathlib import Path

from config import Config
from services.file_service import unique_output_path


class FFmpegNotAvailableError(RuntimeError):
    pass


def ensure_ffmpeg_available() -> None:
    try:
        result = subprocess.run(
            [Config.FFMPEG_BINARY, "-version"],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError as exc:
        raise FFmpegNotAvailableError(
            "FFmpeg no esta instalado o no esta disponible en el PATH. "
            "Instala FFmpeg y reinicia la terminal antes de procesar el video."
        ) from exc

    if result.returncode != 0:
        raise FFmpegNotAvailableError(
            "FFmpeg esta disponible, pero no respondio correctamente al verificar la version."
        )


def replace_video_audio(video_path: Path, audio_path: Path, output_dir: Path) -> Path:
    ensure_ffmpeg_available()

    output_path = unique_output_path(output_dir, video_path, Config.OUTPUT_PREFIX)
    command = [
        Config.FFMPEG_BINARY,
        "-y",
        "-i",
        str(video_path),
        "-i",
        str(audio_path),
        "-map",
        "0:v:0",
        "-map",
        "1:a:0",
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "-movflags",
        "+faststart",
        "-shortest",
        str(output_path),
    ]

    result = subprocess.run(command, capture_output=True, text=True, check=False)

    if result.returncode != 0:
        details = result.stderr.strip() or "FFmpeg no devolvio detalles del error."
        raise RuntimeError(f"No se pudo generar el video final. Detalle: {details}")

    return output_path
