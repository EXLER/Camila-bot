import os

import youtube_dl
import urllib.parse

from utils import log


def url_validator(url: str) -> bool:
    """Validate if a given string is a URL"""
    try:
        result = urllib.parse.urlparse(url)
        return all([result.scheme, result.netloc, result.path])
    except:
        return False


def youtube_download(url) -> str:
    """Downloads a given URL from YouTube using youtube-dl.
       Returns download filename if success, otherwise None"""
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
        # "outtmpl": os.path.join(
        #    os.path.abspath(os.getcwd()), "data", "%(title)s.%(ext).s"
        # ),
    }

    with youtube_dl.YoutubeDL(ytdl_opts) as ytdl:
        log.debug(f"Starting audio download from YouTube, url: {url}")
        ytdl.download([url])

    for file in os.listdir(os.getcwd()):
        if file.endswith(".mp3"):
            name = file
            log.debug(
                f"Renaming and moving file: `{os.path.join(os.getcwd(), file)}` -> `data/audio.mp3`"
            )
            os.rename(file, "data/audio.mp3")
            return name

    return None
