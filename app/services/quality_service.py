# app/services/quality_service.py

import subprocess
import json


class QualityService:

    @staticmethod
    def probe_audio(file_path: str):

        try:

            command = [
                "ffprobe",
                "-v",
                "quiet",
                "-print_format",
                "json",
                "-show_streams",
                file_path
            ]

            result = subprocess.run(
                command,
                capture_output=True,
                text=True
            )

            if not result.stdout:

                return {
                    "codec": "unknown",
                    "bit_rate": None,
                    "sample_rate": None,
                    "channels": None
                }

            data = json.loads(
                result.stdout
            )

            audio_stream = None

            for stream in data.get(
                "streams",
                []
            ):

                if (
                    stream.get("codec_type")
                    == "audio"
                ):

                    audio_stream = stream
                    break

            if not audio_stream:

                return {
                    "codec": "unknown",
                    "bit_rate": None,
                    "sample_rate": None,
                    "channels": None
                }

            return {
                "codec":
                audio_stream.get(
                    "codec_name"
                ),

                "bit_rate":
                audio_stream.get(
                    "bit_rate"
                ),

                "sample_rate":
                audio_stream.get(
                    "sample_rate"
                ),

                "channels":
                audio_stream.get(
                    "channels"
                )
            }

        except Exception:

            return {
                "codec": "unknown",
                "bit_rate": None,
                "sample_rate": None,
                "channels": None
            }