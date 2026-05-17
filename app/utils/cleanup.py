# app/utils/cleanup.py

import shutil

from pathlib import Path


def cleanup_file(file_path: str):

    try:

        path = Path(file_path)

        if path.exists():
            path.unlink()

    except Exception as e:

        print(
            f"Cleanup failed: {e}"
        )


def cleanup_directory(directory_path: str):

    try:

        path = Path(directory_path)

        if path.exists():

            shutil.rmtree(path)

    except Exception as e:

        print(
            f"Directory cleanup failed: {e}"
        )