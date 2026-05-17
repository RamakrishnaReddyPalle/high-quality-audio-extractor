# run.py

import os

import uvicorn

from app.utils.session_manager import (
    SessionManager
)

from app.core.config import (
    TEMP_DIR
)


# =========================================
# CLEANUP OLD SESSIONS
# =========================================

SessionManager.cleanup_stale_sessions(
    temp_dir=str(TEMP_DIR),
    max_age_hours=2
)


# =========================================
# START SERVER
# =========================================

if __name__ == "__main__":

    host = os.getenv(
        "API_HOST",
        "0.0.0.0"
    )

    port = int(
        os.getenv(
            "API_PORT",
            8000
        )
    )

    uvicorn.run(
        "app.api.main:app",

        host=host,

        port=port,

        reload=True
    )