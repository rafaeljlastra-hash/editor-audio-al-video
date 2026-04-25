from pathlib import Path
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
    safe_stem = (secure_filename(video_path.stem) or "video")[:80]
    return output_dir / f"{safe_prefix}-{safe_stem}-{uuid4().hex}.mp4"
