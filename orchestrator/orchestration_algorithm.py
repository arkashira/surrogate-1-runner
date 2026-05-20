"""
Orchestrator – a lightweight, generic async scheduler.

The orchestrator is intentionally agnostic: it can schedule
any async callable – whether it is an LLM agent, a dataset‑ingest
worker, or any other coroutine.

Key features
------------
* **Concurrency limiting** – `max_concurrent` workers run in parallel.
* **Per‑agent timeout** – `agent_timeout` seconds; a timeout raises
  `asyncio.TimeoutError` which is captured and returned in the results.
* **Result collection** – `asyncio.gather(..., return_exceptions=True)`
  ensures that a failure in one worker does not abort the whole batch.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Awaitable, Callable, Iterable, List, Sequence, Union

# A worker can be a coroutine function or an async callable instance.
Worker = Union[Callable[[], Awaitable], Callable[[], Awaitable]]


@dataclass
class OrchestratorConfig:
    """Configuration for the orchestrator."""
    max_concurrent: int = 5          # Max workers running in parallel
    agent_timeout: float = 0.2      # Seconds before a worker is timed out


class Orchestrator:
    """
    Orchestrator runs a collection of async workers with a concurrency limit
    and per‑worker timeout.
    """

    def __init__(self, workers: Sequence[Worker], config: OrchestratorConfig | None = None):
        self.workers: List[Worker] = list(workers)
        self.config = config or OrchestratorConfig()

    async def _run_worker(self, worker: Worker) -> Union[object, Exception]:
        """
        Execute a single worker with timeout.  Any exception (including
        asyncio.TimeoutError) is returned instead of raised.
        """
        try:
            return await asyncio.wait_for(worker(), timeout=self.config.agent_timeout)
        except Exception as exc:          # noqa: BLE001
            return exc

    async def orchestrate(self) -> List[Union[object, Exception]]:
        """
        Run all workers respecting the concurrency limit and return a list
        of results (or exceptions) in the same order as the input workers.
        """
        semaphore = asyncio.Semaphore(self.config.max_concurrent)

        async def sem_task(worker: Worker):
            async with semaphore:
                return await self._run_worker(worker)

        tasks = [asyncio.create_task(sem_task(w)) for w in self.workers]
        return await asyncio.gather(*tasks, return_exceptions=True)


def run_orchestration(
    workers: Sequence[Worker],
    *,
    max_concurrent: int | None = None,
    agent_timeout: float | None = None,
) -> List[Union[object, Exception]]:
    """
    Convenience wrapper that can be called from synchronous code.
    It creates an event loop (or re‑uses the current one) and returns
    the list of results.

    Parameters
    ----------
    workers : Sequence[Worker]
        Iterable of async callables.
    max_concurrent : int, optional
        Override the default concurrency limit.
    agent_timeout : float, optional
        Override the default per‑worker timeout.

    Returns
    -------
    List[Union[object, Exception]]
        Results or exceptions in the same order as `workers`.
    """
    config = OrchestratorConfig(
        max_concurrent=max_concurrent or OrchestratorConfig().max_concurrent,
        agent_timeout=agent_timeout or OrchestratorConfig().agent_timeout,
    )
    orchestrator = Orchestrator(workers, config)

    # `asyncio.run` creates a fresh event loop and is safe to call from scripts.
    return asyncio.run(orchestrator.orchestrate())