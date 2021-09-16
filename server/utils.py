from pathlib import Path


def validate_extension(file_name: Path, extension: str) -> None:
    if file_name.suffix != extension:
        raise ValueError(f"File with {extension} extension required")
