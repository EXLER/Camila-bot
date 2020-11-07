import os
import uuid

import youtube_dlc

from utils import log, validators


def youtube_download(query) -> dict:
    """Downloads a given URL from YouTube using youtube-dl.
       Returns dict if success, otherwise None"""
    filename = str(uuid.uuid4())

    ytdl_opts = {
        "quiet": "True",
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "outtmpl": os.path.join(
            os.path.abspath(os.getcwd()), "data", "audio", f"{filename}.%(ext)s"
        ),
    }

    with youtube_dlc.YoutubeDL(ytdl_opts) as ytdl:
        log.debug(f"Trying to download using query: {query}")
        if validators.url_validator(query):
            result = ytdl.extract_info(query)
        else:
            result = ytdl.extract_info(f"ytsearch:{query}")["entries"][0]
        title = result.get("title", None)
        duration = result.get("duration", None)
        log.debug(f"Found and downloaded: {title}")

    if not title:
        return None

    return {"filename": filename, "title": title, "duration": duration}
