from pathlib import Path


def validate_allowed_extensions(file_name: Path) -> None:
    if file_name.suffix not in [".zip", ".jar"]:
        raise ValueError(f"File with {file_name.suffix} extension is not allowed")
