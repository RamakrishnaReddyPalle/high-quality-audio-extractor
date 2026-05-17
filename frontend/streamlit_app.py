# frontend/streamlit_app.py

import time
import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000"


# =========================================================
# SESSION STATE
# =========================================================

if "processing" not in st.session_state:

    st.session_state.processing = False


# =========================================================
# HELPERS
# =========================================================

def safe_json(response):

    try:
        return response.json()

    except Exception:

        return {
            "status": "error",
            "detail": response.text
        }


def api_failed(data):

    return (
        isinstance(data, dict)
        and (
            "detail" in data
            or data.get("status") == "error"
        )
    )


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Audio EX",
    page_icon="🎵",
    layout="wide"
)

# =========================================================
# HEADER
# =========================================================

st.title("🎵 Audio EX")

st.caption(
    "High Quality Audio Extraction & Smart Conversion Engine"
)

st.markdown(
    """
Audio EX extracts the highest-quality available audio directly from YouTube
and intelligently converts it into your preferred format.

### Features
- High-quality Opus/WebM extraction
- MP3 / FLAC / WAV / Opus conversion
- Embedded metadata & thumbnails
- Playlist batch processing (UNDER CONSTRUCTION YET!)
"""
)

st.divider()

# =========================================================
# TABS
# =========================================================

single_tab, playlist_tab = st.tabs(
    [
        "🎵 Single Song",
        "📂 Playlist"
    ]
)

# =========================================================
# SINGLE SONG TAB
# =========================================================

with single_tab:

    st.subheader(
        "Single Song Conversion"
    )

    youtube_url = st.text_input(
        "Paste YouTube Video URL"
    )

    output_format = st.selectbox(
        "Output Format",
        [
            "webm",
            "mp3",
            "flac",
            "wav",
            "opus"
        ],
        key="single_format"
    )

    # =====================================================
    # BUTTONS
    # =====================================================

    convert_button = st.button(
        (
            "⏳ Converting..."
            if st.session_state.processing
            else "⚡ Convert Audio"
        ),
        disabled=st.session_state.processing,
        use_container_width=True
    )

    cancel_button = st.button(
        "🛑 Cancel Current Process",
        disabled=(
            not st.session_state.processing
        ),
        use_container_width=True
    )

    # =====================================================
    # CANCEL
    # =====================================================

    if cancel_button:

        try:

            requests.post(
                f"{API_URL}/cancel/"
            )

        except Exception:
            pass

        st.session_state.processing = False

        st.warning(
            "Processing cancelled"
        )

        st.stop()

    # =====================================================
    # START PROCESS
    # =====================================================

    if convert_button and youtube_url:

        st.session_state.processing = True

        try:

            # =================================================
            # FETCH METADATA
            # =================================================

            metadata_response = requests.get(
                f"{API_URL}/metadata/",
                params={
                    "url": youtube_url
                }
            )

            metadata = safe_json(
                metadata_response
            )

            if api_failed(metadata):

                st.session_state.processing = False

                st.error(
                    f"Metadata fetch failed:\n"
                    f"{metadata}"
                )

                st.stop()

            # =================================================
            # SONG CARD
            # =================================================

            col1, col2 = st.columns([1, 2])

            with col1:

                st.image(
                    metadata["thumbnail"],
                    width="stretch"
                )

            with col2:

                st.markdown(
                    f"## {metadata['title']}"
                )

                st.write(
                    f"👤 {metadata['uploader']}"
                )

                duration = metadata.get(
                    "duration"
                )

                if duration:

                    minutes = duration // 60
                    seconds = duration % 60

                    st.write(
                        f"⏱ {minutes}:{seconds:02d}"
                    )

            st.divider()

            # =================================================
            # PROGRESS
            # =================================================

            progress_bar = st.progress(0)

            status_text = st.empty()

            # =================================================
            # DOWNLOAD SOURCE
            # =================================================

            response = requests.post(
                f"{API_URL}/download/",
                json={
                    "url": youtube_url
                }
            )

            result = safe_json(response)

            if api_failed(result):

                st.session_state.processing = False

                st.error(
                    f"Download failed:\n"
                    f"{result}"
                )

                st.stop()

            input_path = result["file_path"]

            # =================================================
            # CONVERSION
            # =================================================

            conversion_response = requests.post(
                f"{API_URL}/convert/",
                json={
                    "input_path": input_path,
                    "output_format": output_format,
                    "title": metadata["title"],
                    "artist": metadata["uploader"],
                    "thumbnail": metadata["thumbnail"]
                }
            )

            final_result = safe_json(
                conversion_response
            )

            if api_failed(final_result):

                st.session_state.processing = False

                st.error(
                    f"Conversion failed:\n"
                    f"{final_result}"
                )

                st.stop()

            # =================================================
            # PROGRESS LOOP
            # =================================================

            while True:

                progress_response = requests.get(
                    f"{API_URL}/progress/"
                )

                progress = safe_json(
                    progress_response
                )

                if api_failed(progress):
                    break

                progress_bar.progress(
                    int(
                        progress.get(
                            "progress",
                            0
                        )
                    )
                )

                status_text.write(
                    progress.get(
                        "message",
                        "Processing..."
                    )
                )

                if progress.get(
                    "status"
                ) in [
                    "finished",
                    "cancelled"
                ]:

                    break

                time.sleep(0.5)

            st.session_state.processing = False

            if (
                progress.get("status")
                == "cancelled"
            ):

                st.warning(
                    "Processing cancelled"
                )

                st.stop()

            st.success(
                "Audio processing completed"
            )

            # =================================================
            # DOWNLOAD BUTTON
            # =================================================

            if (
                "download_url"
                in final_result
            ):

                download_url = (
                    API_URL
                    + final_result[
                        "download_url"
                    ]
                )

                st.link_button(
                    "⬇ Download Processed Audio",
                    download_url,
                    use_container_width=True
                )

            # =================================================
            # ADVANCED DETAILS
            # =================================================

            with st.expander(
                "Advanced Audio Details"
            ):

                st.json(final_result)

        except Exception as e:

            st.session_state.processing = False

            st.error(
                f"Unexpected Error:\n{e}"
            )

# =========================================================
# PLAYLIST TAB
# =========================================================

with playlist_tab:

    st.subheader(
        "Playlist Conversion"
    )

    st.info(
        """
Paste a YouTube playlist URL.

Audio EX will:
- Currently under Dev : Not Ready Yet, Stay Tuned! (But you can test it if you want, just expect some hiccups)
- Process videos individually
- Skip broken videos safely if needed
- Continue conversion automatically
- Stream downloadable outputs
"""
    )

    playlist_url = st.text_input(
        "Paste Playlist URL"
    )

    playlist_format = st.selectbox(
        "Playlist Output Format",
        [
            "webm",
            "mp3",
            "flac",
            "wav",
            "opus"
        ],
        key="playlist_format"
    )

    playlist_button = st.button(
        "⚡ Convert Playlist",
        use_container_width=True
    )

    if playlist_button and playlist_url:

        try:

            playlist_response = requests.get(
                f"{API_URL}/playlist/",
                params={
                    "url": playlist_url
                }
            )

            playlist_data = safe_json(
                playlist_response
            )

            if api_failed(playlist_data):

                st.error(
                    f"Playlist fetch failed:\n"
                    f"{playlist_data}"
                )

                st.stop()

            entries = playlist_data.get(
                "entries",
                []
            )

            st.write(
                f"Found {len(entries)} videos"
            )

            downloaded = []
            skipped = []

            overall_progress = st.progress(0)

            status_box = st.empty()

            # =================================================
            # PLAYLIST LOOP
            # =================================================

            for idx, entry in enumerate(entries):

                try:

                    status_box.write(
                        f"Processing: "
                        f"{entry['title']}"
                    )

                    metadata_response = requests.get(
                        f"{API_URL}/metadata/",
                        params={
                            "url": entry["url"]
                        }
                    )

                    metadata = safe_json(
                        metadata_response
                    )

                    if api_failed(metadata):

                        skipped.append(entry)

                        continue

                    response = requests.post(
                        f"{API_URL}/download/",
                        json={
                            "url": entry["url"]
                        }
                    )

                    result = safe_json(
                        response
                    )

                    if api_failed(result):

                        skipped.append(entry)

                        continue

                    input_path = result[
                        "file_path"
                    ]

                    conversion_response = requests.post(
                        f"{API_URL}/convert/",
                        json={
                            "input_path": input_path,
                            "output_format":
                            playlist_format,
                            "title":
                            metadata["title"],
                            "artist":
                            metadata["uploader"],
                            "thumbnail":
                            metadata["thumbnail"]
                        }
                    )

                    final_result = safe_json(
                        conversion_response
                    )

                    if api_failed(final_result):

                        skipped.append(entry)

                        continue

                    if (
                        "download_url"
                        not in final_result
                    ):

                        skipped.append(entry)

                        continue

                    downloaded.append(
                        {
                            "title":
                            metadata["title"],

                            "thumbnail":
                            metadata["thumbnail"],

                            "download_url":
                            final_result[
                                "download_url"
                            ]
                        }
                    )

                except Exception:

                    skipped.append(entry)

                overall_progress.progress(
                    int(
                        ((idx + 1)
                         / len(entries))
                        * 100
                    )
                )

            status_box.empty()

            # =================================================
            # RESULTS
            # =================================================

            st.success(
                f"Processed "
                f"{len(downloaded)} tracks"
            )

            cols = st.columns(4)

            for idx, item in enumerate(downloaded):

                with cols[idx % 4]:

                    st.image(
                        item["thumbnail"]
                    )

                    st.caption(
                        item["title"]
                    )

                    download_url = (
                        API_URL
                        + item[
                            "download_url"
                        ]
                    )

                    st.link_button(
                        "⬇ Download",
                        download_url,
                        key=f"dl_{idx}",
                        use_container_width=True
                    )

            # =================================================
            # SKIPPED
            # =================================================

            if skipped:

                st.warning(
                    f"Skipped "
                    f"{len(skipped)} videos"
                )

                with st.expander(
                    "Skipped Videos"
                ):

                    for item in skipped:

                        st.error(
                            item["title"]
                        )

        except Exception as e:

            st.error(
                f"Unexpected Playlist Error:\n"
                f"{e}"
            )