# app/utils/file_utils.py

import re
import uuid

from pathlib import Path

from app.core.config import TEMP_DIR


MAX_FILENAME_LENGTH = 80


def sanitize_filename(
    filename: str
):

    # REMOVE ILLEGAL CHARS

    filename = re.sub(
        r'[\\/*?:"<>|&]',
        "",
        filename
    )

    # REMOVE EXTRA SPACES

    filename = re.sub(
        r"\s+",
        " ",
        filename
    ).strip()

    return filename[
        :MAX_FILENAME_LENGTH
    ]


def file_exists(
    path: str
) -> bool:

    return Path(path).exists()


def create_session_directory():

    session_id = str(
        uuid.uuid4()
    )[:8]

    session_dir = (
        TEMP_DIR
        / session_id
    )

    session_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    return (
        session_id,
        session_dir
    )