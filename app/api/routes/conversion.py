# app/api/routes/conversion.py

from pathlib import Path

from urllib.parse import quote

from fastapi import (
    APIRouter,
    HTTPException
)

from app.models.conversion_models import (
    ConversionRequest
)

from app.services.ffmpeg_service import (
    FFmpegService
)

from app.services.quality_service import (
    QualityService
)

from app.core.logger import logger

router = APIRouter()


@router.post("/")
def convert_audio(
    request: ConversionRequest
):

    try:

        before = (
            QualityService.probe_audio(
                request.input_path
            )
        )

        output_path = (
            FFmpegService.convert_audio(
                input_path=request.input_path,
                output_format=request.output_format,
                bitrate=request.bitrate,
                metadata={
                    "title": request.title,
                    "artist": request.artist,
                    "thumbnail": request.thumbnail
                }
            )
        )

        after = (
            QualityService.probe_audio(
                output_path
            )
        )

        filename = Path(
            output_path
        ).name

        encoded_path = quote(
            output_path
        )

        logger.info(
            f"Conversion route success: "
            f"{filename}"
        )

        return {
            "status": "success",

            "input_analysis": before,

            "output_analysis": after,

            "output_path": output_path,

            "filename": filename,

            "download_url":
            f"/serve/?path={encoded_path}"
        }

    except Exception as e:

        logger.error(
            f"Conversion route failed: "
            f"{str(e)}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )