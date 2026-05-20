"""
Python SDK for interacting with the Axentx Surrogate-1 pipeline.

Provides a thin wrapper around the pipeline's HTTP API, enabling developers
to start pipeline jobs and query their status programmatically.

Typical usage::

    from sdk import PipelineClient

    client = PipelineClient(base_url="https://api.axentx.com/pipeline")
    job_id = client.start_pipeline({"input": "s3://bucket/data.json"})
    status = client.get_status(job_id)
"""

import os
import json
from typing import Any, Dict, Optional

import requests


class PipelineError(Exception):
    """Base exception for all pipeline SDK errors."""


class PipelineClient:
    """
    Client for the Surrogate-1 pipeline API.

    Parameters
    ----------
    base_url: str, optional
        Base URL of the pipeline service. If omitted, the environment variable
        ``AXENTX_PIPELINE_URL`` is used. Raises ``PipelineError`` if no URL is
        available.
    timeout: float, optional
        HTTP request timeout in seconds (default: 10).
    """

    def __init__(self, base_url: Optional[str] = None, timeout: float = 10.0):
        self.base_url = base_url or os.getenv("AXENTX_PIPELINE_URL")
        if not self.base_url:
            raise PipelineError(
                "Pipeline base URL not provided. Set AXENTX_PIPELINE_URL env var or pass base_url."
            )
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def _url(self, path: str) -> str:
        return f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"

    def start_pipeline(self, payload: Dict[str, Any]) -> str:
        """
        Submit a new pipeline job.

        Parameters
        ----------
        payload: dict
            JSON‑serialisable payload describing the job (e.g. input locations,
            processing options).

        Returns
        -------
        str
            The job identifier returned by the service.

        Raises
        ------
        PipelineError
            If the request fails or the response is malformed.
        """
        url = self._url("/jobs")
        try:
            resp = self.session.post(url, data=json.dumps(payload), timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
            job_id = data.get("job_id")
            if not job_id:
                raise PipelineError("Response missing 'job_id'")
            return job_id
        except (requests.RequestException, ValueError) as exc:
            raise PipelineError(f"Failed to start pipeline: {exc}") from exc

    def get_status(self, job_id: str) -> Dict[str, Any]:
        """
        Retrieve the current status of a pipeline job.

        Parameters
        ----------
        job_id: str
            Identifier of the job to query.

        Returns
        -------
        dict
            JSON payload containing status information (e.g. ``status``,
            ``started_at``, ``completed_at``).

        Raises
        ------
        PipelineError
            If the request fails or the response is malformed.
        """
        url = self._url(f"/jobs/{job_id}")
        try:
            resp = self.session.get(url, timeout=self.timeout)
            resp.raise_for_status()
            return resp.json()
        except (requests.RequestException, ValueError) as exc:
            raise PipelineError(f"Failed to get status for job {job_id}: {exc}") from exc