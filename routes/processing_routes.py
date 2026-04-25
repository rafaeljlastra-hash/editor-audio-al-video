from pathlib import Path

from flask import Blueprint, jsonify, request, send_file, session

from config import Config
from services.ffmpeg_service import FFmpegNotAvailableError, replace_video_audio


processing_bp = Blueprint("processing", __name__, url_prefix="/api")


def is_inside_storage(path: Path) -> bool:
    try:
        path.resolve().relative_to(Config.STORAGE_DIR.resolve())
    except ValueError:
        return False

    return True


def parse_audio_delay(value) -> tuple[float | None, str | None]:
    if value in (None, ""):
        return 0.0, None

    try:
        delay = float(value)
    except (TypeError, ValueError):
        return None, "El retraso del audio debe ser un numero mayor o igual a 0."

    if delay < 0:
        return None, "El retraso del audio debe ser mayor o igual a 0."

    return delay, None


@processing_bp.post("/process")
def process_video():
    video_path = session.get("video_path")
    audio_path = session.get("audio_path")
    payload = request.get_json(silent=True) or {}
    delay, delay_error = parse_audio_delay(payload.get("delay", 0))

    if delay_error:
        return jsonify({"ok": False, "error": delay_error}), 400

    if not video_path:
        return jsonify({"ok": False, "error": "Primero debes subir un video MP4."}), 400

    if not audio_path:
        return jsonify({"ok": False, "error": "Primero debes subir un audio MP3."}), 400

    video_file = Path(video_path)
    audio_file = Path(audio_path)

    if not is_inside_storage(video_file):
        return jsonify({"ok": False, "error": "La ruta del video no es valida."}), 400

    if not is_inside_storage(audio_file):
        return jsonify({"ok": False, "error": "La ruta del audio no es valida."}), 400

    if not video_file.exists():
        return jsonify({"ok": False, "error": "El archivo de video ya no existe."}), 400

    if not audio_file.exists():
        return jsonify({"ok": False, "error": "El archivo de audio ya no existe."}), 400

    try:
        output_file = replace_video_audio(video_file, audio_file, Config.OUTPUT_DIR, delay)
    except FFmpegNotAvailableError as exc:
        return jsonify({"ok": False, "error": str(exc)}), 500
    except RuntimeError as exc:
        return jsonify({"ok": False, "error": str(exc)}), 500

    session["output_path"] = str(output_file)

    return jsonify(
        {
            "ok": True,
            "message": "Video final generado correctamente.",
            "download_url": "/api/download",
            "filename": output_file.name,
        }
    )


@processing_bp.get("/download")
def download_output():
    output_path = session.get("output_path")

    if not output_path:
        return jsonify({"ok": False, "error": "Todavia no hay un video generado."}), 400

    output_file = Path(output_path)

    if not is_inside_storage(output_file):
        return jsonify({"ok": False, "error": "La ruta del video generado no es valida."}), 400

    if not output_file.exists():
        return jsonify({"ok": False, "error": "El archivo final ya no existe."}), 404

    return send_file(output_file, as_attachment=True, download_name=output_file.name)
