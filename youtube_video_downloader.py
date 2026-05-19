import os
import json
import logging
from datetime import datetime
from typing import Optional

from pytube import YouTube
from pytube.exceptions import PytubeError, RegexMatchError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# --------------------------------------------------------------------------- #
# Logger configuration – compliance‑ready JSON logs
# --------------------------------------------------------------------------- #
_logger = logging.getLogger("youtube_video_downloader")
if not _logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    _logger.addHandler(handler)
    _logger.setLevel(logging.INFO)


def _log_event(event: str, url: str, status: str, extra: Optional[dict] = None) -> None:
    """Emit a single JSON line log for compliance auditing."""
    log_record = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "event": event,
        "url": url,
        "status": status,
    }
    if extra:
        log_record.update(extra)
    _logger.info(json.dumps(log_record))


# --------------------------------------------------------------------------- #
# Rate‑limit aware download implementation
# --------------------------------------------------------------------------- #
class YouTubeDownloadError(RuntimeError):
    """Raised when a YouTube video cannot be downloaded after retries."""


@retry(
    retry=retry_if_exception_type((PytubeError, RegexMatchError)),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    reraise=True,
)
def _download_with_retry(url: str, output_dir: str) -> str:
    """
    Download a YouTube video, retrying on transient errors (including rate‑limit).

    Returns the absolute path to the downloaded file.
    """
    yt = YouTube(url)
    # Choose the highest‑resolution progressive stream (audio+video)
    stream = (
        yt.streams.filter(progressive=True, file_extension="mp4")
        .order_by("resolution")
        .desc()
        .first()
    )
    if not stream:
        raise YouTubeDownloadError("No suitable stream found for URL.")
    return stream.download(output_path=output_dir)


def download_video(url: str, output_dir: Optional[str] = None) -> str:
    """
    Public API: download a YouTube video and return the local file path.

    Parameters
    ----------
    url: str
        A valid YouTube video URL.
    output_dir: Optional[str]
        Directory where the video will be saved. If omitted, uses
        ``./downloads`` relative to the current working directory.

    Returns
    -------
    str
        Absolute path to the downloaded video file.

    Raises
    ------
    YouTubeDownloadError
        If the video cannot be downloaded after retries.
    """
    if not output_dir:
        output_dir = os.path.join(os.getcwd(), "downloads")
    os.makedirs(output_dir, exist_ok=True)

    _log_event(event="download_requested", url=url, status="started")
    try:
        file_path = _download_with_retry(url, output_dir)
        _log_event(
            event="download_completed",
            url=url,
            status="success",
            extra={"file_path": os.path.abspath(file_path)},
        )
        return os.path.abspath(file_path)
    except (PytubeError, RegexMatchError, YouTubeDownloadError) as exc:
        _log_event(
            event="download_failed",
            url=url,
            status="error",
            extra={"error": str(exc)},
        )
        raise YouTubeDownloadError(f"Failed to download video from {url}") from exc