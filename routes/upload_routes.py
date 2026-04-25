from flask import Blueprint, jsonify, request, session

from config import Config
from services.file_service import save_uploaded_file
from services.validation_service import validate_uploaded_file


upload_bp = Blueprint("upload", __name__, url_prefix="/api/upload")


@upload_bp.post("/video")
def upload_video():
    uploaded_file = request.files.get("video")
    error = validate_uploaded_file(
        uploaded_file,
        Config.ALLOWED_VIDEO_EXTENSIONS,
        Config.MAX_VIDEO_SIZE,
        "video MP4",
    )

    if error:
        return jsonify({"ok": False, "error": error}), 400

    stored_file = save_uploaded_file(uploaded_file, Config.INPUT_VIDEO_DIR)
    session["video_path"] = str(stored_file)

    return jsonify(
        {
            "ok": True,
            "message": "Video cargado correctamente.",
            "filename": stored_file.name,
        }
    )


@upload_bp.post("/audio")
def upload_audio():
    uploaded_file = request.files.get("audio")
    error = validate_uploaded_file(
        uploaded_file,
        Config.ALLOWED_AUDIO_EXTENSIONS,
        Config.MAX_AUDIO_SIZE,
        "audio MP3",
    )

    if error:
        return jsonify({"ok": False, "error": error}), 400

    stored_file = save_uploaded_file(uploaded_file, Config.INPUT_AUDIO_DIR)
    session["audio_path"] = str(stored_file)

    return jsonify(
        {
            "ok": True,
            "message": "Audio cargado correctamente.",
            "filename": stored_file.name,
        }
    )
