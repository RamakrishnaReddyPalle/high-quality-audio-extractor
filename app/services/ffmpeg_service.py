# app/services/ffmpeg_service.py

import subprocess

from pathlib import Path

from app.core.logger import logger

from app.core.progress_tracker import (
    progress_data
)

from app.services.metadata_service import (
    MetadataService
)

from app.services.thumbnail_service import (
    ThumbnailService
)

from app.utils.cleanup import (
    cleanup_file
)

from app.utils.process_registry import (
    active_processes
)

from app.utils.file_utils import (
    sanitize_filename
)


class FFmpegService:

    @staticmethod
    def convert_audio(
        input_path: str,
        output_format: str,
        bitrate: str = None,
        metadata: dict = None
    ):

        progress_data["active"] = True

        progress_data["cancelled"] = False

        input_path = Path(input_path)

        input_ext = (
            input_path.suffix
            .replace(".", "")
            .lower()
        )

        # =====================================
        # SKIP UNNECESSARY CONVERSION
        # =====================================

        if input_ext == output_format:

            logger.info(
                "Skipping conversion "
                "- format already matches"
            )

            progress_data["status"] = (
                "finished"
            )

            progress_data["progress"] = 100

            progress_data["message"] = (
                "No conversion required"
            )

            progress_data["active"] = False

            return str(input_path)

        output_path = input_path.with_suffix(
            f".{output_format}"
        )

        command = [
            "ffmpeg",
            "-y",
            "-i",
            str(input_path)
        ]

        # =====================================
        # FORMAT HANDLING
        # =====================================

        if output_format == "flac":

            command.extend([
                "-c:a",
                "flac"
            ])

        elif output_format == "wav":

            command.extend([
                "-c:a",
                "pcm_s16le"
            ])

        elif output_format == "mp3":

            # =================================
            # STABLE MP3 ENCODING
            # =================================

            command.extend([
                "-c:a",
                "libmp3lame",
                "-b:a",
                "320k"
            ])

        elif output_format == "aac":

            command.extend([
                "-c:a",
                "aac"
            ])

        elif output_format == "opus":

            command.extend([
                "-c:a",
                "libopus"
            ])

        elif output_format == "m4a":

            command.extend([
                "-c:a",
                "copy"
            ])

        else:

            raise Exception(
                f"Unsupported format: "
                f"{output_format}"
            )

        # =====================================
        # OPTIONAL CUSTOM BITRATE
        # =====================================

        if (
            bitrate
            and output_format != "mp3"
        ):

            command.extend([
                "-b:a",
                bitrate
            ])

        command.append(
            str(output_path)
        )

        logger.info(
            f"Running FFmpeg: "
            f"{' '.join(command)}"
        )

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        process_id = str(id(process))

        active_processes[
            process_id
        ] = process

        stdout, stderr = process.communicate()

        active_processes.pop(
            process_id,
            None
        )

        # =====================================
        # CANCEL HANDLING
        # =====================================

        if progress_data["cancelled"]:

            progress_data["status"] = (
                "cancelled"
            )

            progress_data["message"] = (
                "Processing cancelled"
            )

            progress_data["active"] = False

            cleanup_file(
                str(output_path)
            )

            raise Exception(
                "Processing cancelled"
            )

        # =====================================
        # FFmpeg ERROR
        # =====================================

        if process.returncode != 0:

            logger.error(
                f"FFmpeg stderr:\n"
                f"{stderr}"
            )

            cleanup_file(
                str(output_path)
            )

            raise Exception(stderr)

        # =====================================
        # METADATA
        # =====================================

        thumbnail_path = None

        if metadata:

            title = metadata.get("title")

            artist = metadata.get("artist")

            thumbnail = metadata.get(
                "thumbnail"
            )

            # =================================
            # ONLY MP3 COVER
            # =================================

            if (
                thumbnail
                and output_format == "mp3"
            ):

                safe_name = sanitize_filename(
                    title
                ) if title else "thumbnail"

                try:

                    thumbnail_path = (
                        ThumbnailService
                        .download_thumbnail(
                            thumbnail_url=thumbnail,
                            filename=safe_name
                        )
                    )

                except Exception as e:

                    logger.warning(
                        f"Thumbnail download failed: "
                        f"{e}"
                    )

                    thumbnail_path = None

            # =================================
            # MP3 METADATA
            # =================================

            if output_format == "mp3":

                try:

                    MetadataService.embed_mp3_metadata(
                        file_path=str(output_path),
                        title=title or "",
                        artist=artist or "",
                        thumbnail_path=thumbnail_path
                    )

                except Exception as e:

                    logger.warning(
                        f"MP3 metadata failed: "
                        f"{e}"
                    )

            # =================================
            # FLAC METADATA
            # =================================

            elif output_format == "flac":

                try:

                    MetadataService.embed_flac_metadata(
                        file_path=str(output_path),
                        title=title or "",
                        artist=artist or ""
                    )

                except Exception as e:

                    logger.warning(
                        f"FLAC metadata failed: "
                        f"{e}"
                    )

        logger.info(
            f"Conversion completed: "
            f"{output_path}"
        )

        # =====================================
        # CLEANUP
        # =====================================

        if (
            input_path.exists()
            and input_path.suffix
            != output_path.suffix
        ):

            cleanup_file(
                str(input_path)
            )

        if thumbnail_path:

            cleanup_file(
                thumbnail_path
            )

        progress_data["status"] = (
            "finished"
        )

        progress_data["progress"] = 100

        progress_data["message"] = (
            "Conversion completed"
        )

        progress_data["active"] = False

        return str(output_path)