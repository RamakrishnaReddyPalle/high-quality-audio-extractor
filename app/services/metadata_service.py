# app/services/metadata_service.py

from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.id3 import (
    ID3,
    APIC,
    TIT2,
    TPE1,
    error
)

from app.core.logger import logger


class MetadataService:

    @staticmethod
    def embed_mp3_metadata(
        file_path: str,
        title: str,
        artist: str,
        thumbnail_path: str = None
    ):

        try:
            tags = ID3(file_path)

        except error:
            tags = ID3()

        tags.add(
            TIT2(
                encoding=3,
                text=title
            )
        )

        tags.add(
            TPE1(
                encoding=3,
                text=artist
            )
        )

        if thumbnail_path:

            with open(
                thumbnail_path,
                "rb"
            ) as albumart:

                tags.add(
                    APIC(
                        encoding=3,
                        mime="image/jpeg",
                        type=3,
                        desc="Cover",
                        data=albumart.read()
                    )
                )

        tags.save(file_path)

        logger.info(
            f"Embedded MP3 metadata: {file_path}"
        )

    @staticmethod
    def embed_flac_metadata(
        file_path: str,
        title: str,
        artist: str
    ):

        audio = FLAC(file_path)

        audio["title"] = title
        audio["artist"] = artist

        audio.save()

        logger.info(
            f"Embedded FLAC metadata: {file_path}"
        )