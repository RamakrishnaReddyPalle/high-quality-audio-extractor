# app/services/yt_dlp_service.py

from yt_dlp import YoutubeDL

from app.core.logger import logger
from app.core.progress_tracker import progress_data

from app.utils.file_utils import (
    sanitize_filename,
    create_session_directory
)


class YTDLPService:

    @staticmethod
    def fetch_metadata(url: str):

        ydl_opts = {
            "quiet": True,
            "skip_download": True
        }

        with YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(
                url,
                download=False
            )

        return info

    @staticmethod
    def get_best_audio_format(formats):

        audio_formats = []

        for fmt in formats:

            if fmt.get("vcodec") != "none":
                continue

            acodec = fmt.get("acodec")

            if acodec == "none":
                continue

            audio_formats.append(fmt)

        if not audio_formats:
            return None

        def score(fmt):

            codec = (
                fmt.get("acodec") or ""
            ).lower()

            abr = fmt.get("abr") or 0

            codec_score = 0

            if "opus" in codec:
                codec_score = 1000

            elif "aac" in codec:
                codec_score = 800

            elif "vorbis" in codec:
                codec_score = 700

            elif "mp3" in codec:
                codec_score = 500

            return codec_score + abr

        best = sorted(
            audio_formats,
            key=score,
            reverse=True
        )[0]

        return best

    @staticmethod
    def progress_hook(d):

        if d["status"] == "downloading":

            total = d.get(
                "total_bytes"
            ) or d.get(
                "total_bytes_estimate",
                1
            )

            downloaded = d.get(
                "downloaded_bytes",
                0
            )

            percent = (
                downloaded / total
            ) * 100

            progress_data["status"] = (
                "downloading"
            )

            progress_data["progress"] = round(
                percent,
                2
            )

            speed = d.get("speed")

            if speed:

                speed_mb = (
                    speed / 1024 / 1024
                )

                progress_data["message"] = (
                    f"Downloading: {speed_mb:.2f} MB/s"
                )

        elif d["status"] == "finished":

            progress_data["status"] = (
                "finished"
            )

            progress_data["progress"] = 100

            progress_data["message"] = (
                "Download completed"
            )

    @staticmethod
    def download_best_audio(url: str):

        info = YTDLPService.fetch_metadata(url)

        title = sanitize_filename(
            info.get("title", "audio")
        )

        best_audio = (
            YTDLPService.get_best_audio_format(
                info.get("formats", [])
            )
        )

        if not best_audio:
            raise Exception(
                "No audio format found"
            )

        session_id, session_dir = (
            create_session_directory()
        )

        format_id = best_audio["format_id"]

        ext = best_audio.get(
            "ext",
            "webm"
        )

        output_template = str(
            session_dir / f"{title}.%(ext)s"
        )

        ydl_opts = {
            "format": format_id,
            "outtmpl": output_template,
            "quiet": False,
            "noplaylist": True,
            "progress_hooks": [
                YTDLPService.progress_hook
            ]
        }

        logger.info(
            f"Downloading format: {format_id}"
        )

        with YoutubeDL(ydl_opts) as ydl:

            ydl.download([url])

        final_path = str(
            session_dir / f"{title}.{ext}"
        )

        return {
            "status": "success",
            "session_id": session_id,
            "session_dir": str(session_dir),
            "file_path": final_path,
            "codec": best_audio.get("acodec")
        }

    @staticmethod
    def fetch_playlist_entries(url: str):

        ydl_opts = {
            "quiet": True,
            "extract_flat": True,
            "skip_download": True
        }

        with YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(
                url,
                download=False
            )

        entries = info.get("entries", [])

        return [
            {
                "id": entry.get("id"),
                "title": entry.get("title"),
                "url": (
                    f"https://youtube.com/watch?v="
                    f"{entry.get('id')}"
                )
            }
            for entry in entries
        ]