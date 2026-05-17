# app/utils/validators.py

from urllib.parse import urlparse
from app.core.constants import YOUTUBE_DOMAINS


def validate_youtube_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()

        return any(ytd in domain for ytd in YOUTUBE_DOMAINS)

    except Exception:
        return False