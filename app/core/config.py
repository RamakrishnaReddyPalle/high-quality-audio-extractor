# app\core\config.py

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

TEMP_DIR = BASE_DIR / "app" / "temp"

TEMP_DIR.mkdir(
    parents=True,
    exist_ok=True
)

DEFAULT_AUDIO_PRIORITY = [
    "opus",
    "aac",
    "mp4a",
    "vorbis",
    "mp3"
]

MAX_FILENAME_LENGTH = 150