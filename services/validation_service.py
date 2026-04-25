from pathlib import Path

from werkzeug.datastructures import FileStorage


def validate_uploaded_file(
    uploaded_file: FileStorage | None,
    allowed_extensions: set[str],
    max_size: int,
    label: str,
) -> str | None:
    if uploaded_file is None:
        return f"No se recibio ningun archivo de {label}."

    if not uploaded_file.filename:
        return f"Selecciona un archivo de {label}."

    extension = Path(uploaded_file.filename).suffix.lower()

    if extension not in allowed_extensions:
        allowed = ", ".join(sorted(allowed_extensions))
        return f"Formato invalido para {label}. Formatos permitidos: {allowed}."

    uploaded_file.stream.seek(0, 2)
    size = uploaded_file.stream.tell()
    uploaded_file.stream.seek(0)

    if size <= 0:
        return f"El archivo de {label} esta vacio."

    if size > max_size:
        max_mb = max_size // (1024 * 1024)
        return f"El archivo de {label} supera el limite de {max_mb} MB."

    return None
