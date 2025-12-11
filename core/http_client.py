from __future__ import annotations
from typing import Iterable, Any, Protocol
import logging
import time
import requests


class HttpClient(Protocol):
    def get(self, path: str, **kwargs: Any): ...
    def post(self, path: str, **kwargs: Any): ...


class RequestsHttpClient:
    """SRP: Only handles network I/O.
       DIP: Can be replaced by any HttpClient."""
    def __init__(
        self,
        base_url: str,
        timeout: float = 5.0,
        retry_statuses: Iterable[int] = (502, 503, 504),
        max_retries: int = 3,
        logger: logging.Logger | None = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.retry_statuses = set(retry_statuses)
        self.max_retries = max_retries
        self.session = requests.Session()
        self.log = logger or logging.getLogger(self.__class__.__name__)

    def _request(self, method: str, path: str, **kwargs: Any):
        url = f"{self.base_url}{path}"

        for attempt in range(1, self.max_retries + 1):
            try:
                response = self.session.request(
                    method, url, timeout=self.timeout, **kwargs
                )

                if response.status_code in self.retry_statuses and attempt < self.max_retries:
                    time.sleep(0.1 * attempt)
                    continue

                return response

            except requests.RequestException:
                if attempt == self.max_retries:
                    raise
                time.sleep(0.1 * attempt)

    def get(self, path: str, **kwargs: Any):
        return self._request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any):
        return self._request("POST", path, **kwargs)
