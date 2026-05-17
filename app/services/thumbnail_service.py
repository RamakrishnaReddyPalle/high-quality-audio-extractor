# app/services/thumbnail_service.py

import requests
from pathlib import Path

from app.core.config import TEMP_DIR


class ThumbnailService:

    @staticmethod
    def download_thumbnail(
        thumbnail_url: str,
        filename: str
    ):

        response = requests.get(thumbnail_url)

        if response.status_code != 200:
            raise Exception(
                "Failed to download thumbnail"
            )

        thumbnail_path = (
            TEMP_DIR / f"{filename}.jpg"
        )

        with open(thumbnail_path, "wb") as f:
            f.write(response.content)

        return str(thumbnail_path)