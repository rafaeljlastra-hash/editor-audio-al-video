from pathlib import Path
from datetime import datetime
import shutil
from uuid import uuid4

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename


def save_uploaded_file(uploaded_file: FileStorage, destination_dir: Path) -> Path:
    destination_dir.mkdir(parents=True, exist_ok=True)

    original_name = secure_filename(uploaded_file.filename or "archivo")
    stem = (Path(original_name).stem or "archivo")[:80]
    suffix = Path(original_name).suffix.lower()
    filename = f"{stem}-{uuid4().hex}{suffix}"
    destination = destination_dir / filename

    uploaded_file.save(destination)
    return destination


def unique_output_path(output_dir: Path, video_path: Path, output_prefix: str) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)

    safe_prefix = (secure_filename(output_prefix) or "video-final")[:40]
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    unique_id = uuid4().hex[:6]
    return output_dir / f"{safe_prefix}_{timestamp}_{unique_id}.mp4"


def cleanup_temp_files(temp_dir: Path) -> None:
    if not temp_dir.exists() or not temp_dir.is_dir():
        return

    for item in temp_dir.iterdir():
        try:
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
        except OSError:
            pass


def cleanup_files(paths: list[Path]) -> None:
    for path in paths:
        try:
            if path.exists() and path.is_file():
                path.unlink()
        except OSError:
            pass
