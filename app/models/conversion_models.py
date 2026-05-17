# app/models/conversion_models.py

from pydantic import BaseModel
from typing import Optional


class ConversionRequest(BaseModel):

    input_path: str
    output_format: str
    bitrate: Optional[str] = None

    title: Optional[str] = None
    artist: Optional[str] = None
    thumbnail: Optional[str] = None