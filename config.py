import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


def _env_int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, default))
    except ValueError:
        return default


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)

    if value is None:
        return default

    return value.strip().lower() in {"1", "true", "yes", "on"}


class Config:
    BASE_DIR = Path(__file__).resolve().parent
    STORAGE_DIR = BASE_DIR / "storage"
    INPUT_VIDEO_DIR = STORAGE_DIR / "input_video"
    INPUT_AUDIO_DIR = STORAGE_DIR / "input_audio"
    OUTPUT_DIR = STORAGE_DIR / "output"
    TEMP_DIR = STORAGE_DIR / "temp"

    SECRET_KEY = "change-this-local-dev-key"
    MAX_CONTENT_LENGTH = 600 * 1024 * 1024

    FLASK_HOST = os.getenv("FLASK_HOST", "127.0.0.1")
    FLASK_PORT = _env_int("FLASK_PORT", 5000)
    FLASK_DEBUG = _env_bool("FLASK_DEBUG", True)

    MAX_VIDEO_SIZE = _env_int("MAX_VIDEO_MB", 500) * 1024 * 1024
    MAX_AUDIO_SIZE = _env_int("MAX_AUDIO_MB", 100) * 1024 * 1024

    FFMPEG_BINARY = os.getenv("FFMPEG_BINARY", "ffmpeg")
    OUTPUT_PREFIX = os.getenv("OUTPUT_PREFIX", "video-final")
    CLEANUP_INPUT_FILES = _env_bool("CLEANUP_INPUT_FILES", False)

    ALLOWED_VIDEO_EXTENSIONS = {".mp4"}
    ALLOWED_AUDIO_EXTENSIONS = {".mp3"}


def ensure_storage_directories():
    for directory in (
        Config.INPUT_VIDEO_DIR,
        Config.INPUT_AUDIO_DIR,
        Config.OUTPUT_DIR,
        Config.TEMP_DIR,
    ):
        directory.mkdir(parents=True, exist_ok=True)
