import logging
import threading
import time
from dataclasses import dataclass, field
from typing import List, Optional

import requests

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)


@dataclass
class Provider:
    """Simple representation of an LLM provider."""

    name: str
    base_url: str
    health_path: str = "/health"
    timeout: int = 5
    is_healthy: bool = field(default=False, init=False)
    _lock: threading.Lock = field(default_factory=threading.Lock, init=False)

    def health_url(self) -> str:
        return f"{self.base_url.rstrip('/')}{self.health_path}"

    def set_health(self, healthy: bool) -> None:
        with self._lock:
            self.is_healthy = healthy

    def get_health(self) -> bool:
        with self._lock:
            return self.is_healthy


class HealthChecker:
    """
    Periodically checks the health of a list of providers and maintains
    round‑robin selection among the healthy ones.
    """

    def __init__(self, providers: List[Provider], interval: int = 30):
        if not providers:
            raise ValueError("At least one provider must be supplied")
        self.providers = providers
        self.interval = interval
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._rr_index = 0
        self._rr_lock = threading.Lock()

    # --------------------------------------------------------------------- #
    # Public API
    # --------------------------------------------------------------------- #
    def start(self) -> None:
        """Start the background health‑check loop."""
        if self._running:
            logger.debug("HealthChecker already running")
            return
        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True, name="HealthChecker")
        self._thread.start()
        logger.info("HealthChecker started")

    def stop(self) -> None:
        """Stop the background health‑check loop."""
        self._running = False
        if self._thread:
            self._thread.join()
            logger.info("HealthChecker stopped")

    def get_healthy_providers(self) -> List[Provider]:
        """Return a snapshot list of currently healthy providers."""
        return [p for p in self.providers if p.get_health()]

    def get_next_provider(self) -> Provider:
        """
        Return the next healthy provider using round‑robin.
        Raises RuntimeError if no providers are healthy.
        """
        healthy = self.get_healthy_providers()
        if not healthy:
            raise RuntimeError("No healthy providers available")
        with self._rr_lock:
            provider = healthy[self._rr_index % len(healthy)]
            self._rr_index = (self._rr_index + 1) % len(healthy)
        logger.debug("Selected provider %s", provider.name)
        return provider

    # --------------------------------------------------------------------- #
    # Internal helpers
    # --------------------------------------------------------------------- #
    def _run(self) -> None:
        """Background thread that performs health checks at the configured interval."""
        while self._running:
            start = time.time()
            self._check_all()
            elapsed = time.time() - start
            sleep_time = max(0, self.interval - elapsed)
            time.sleep(sleep_time)

    def _check_all(self) -> None:
        """Check health of each provider and update its status."""
        for provider in self.providers:
            self._check_provider(provider)

    def _check_provider(self, provider: Provider) -> None:
        """Perform a single health‑check request."""
        try:
            response = requests.get(provider.health_url(), timeout=provider.timeout)
            healthy = response.status_code == 200
        except Exception as exc:  # noqa: BLE001 – we want to treat any exception as unhealthy
            logger.debug("Health check failed for %s: %s", provider.name, exc)
            healthy = False

        previous = provider.get_health()
        provider.set_health(healthy)

        if healthy != previous:
            state = "healthy" if healthy else "unhealthy"
            logger.info("Provider %s marked %s", provider.name, state)


# ------------------------------------------------------------------------- #
# Convenience singleton for the rest of the codebase
# ------------------------------------------------------------------------- #
def create_default_checker() -> HealthChecker:
    """
    Factory that creates a HealthChecker using environment‑defined providers.
    This function can be extended by the system integrator to pull configuration
    from a file, env vars, or a service discovery mechanism.
    """
    # Placeholder: in a real deployment this would be dynamic.
    default_providers = [
        Provider(name="OpenAI", base_url="https://api.openai.com/v1"),
        Provider(name="Anthropic", base_url="https://api.anthropic.com/v1"),
        Provider(name="Cohere", base_url="https://api.cohere.com/v1"),
    ]
    checker = HealthChecker(default_providers, interval=30)
    checker.start()
    return checker


# Exported symbols
__all__ = ["Provider", "HealthChecker", "create_default_checker"]