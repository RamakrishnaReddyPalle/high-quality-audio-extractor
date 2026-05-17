# app/models/request_models.py

from pydantic import BaseModel


class DownloadRequest(BaseModel):
    url: str