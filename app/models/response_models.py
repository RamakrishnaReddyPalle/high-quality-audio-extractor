# app/models/response_models.py

from pydantic import BaseModel
from typing import List, Optional


class AudioFormat(BaseModel):
    format_id: str
    ext: Optional[str]
    acodec: Optional[str]
    abr: Optional[float]


class MetadataResponse(BaseModel):
    title: str
    uploader: Optional[str]
    duration: Optional[int]
    thumbnail: Optional[str]
    formats: List[AudioFormat]


class DownloadResponse(BaseModel):
    status: str
    file_path: str
    codec: Optional[str]