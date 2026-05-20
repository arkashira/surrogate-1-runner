"""
Deterministic orchestration algorithm for LLM agents.

The algorithm guarantees that for a given request identifier the same
ordering of agents is used, and that all agents are invoked concurrently
to meet sub‑200 ms latency requirements.

Key features
------------
* Deterministic ordering: agents are sorted by their name and the
  starting index is derived from a hash of the request identifier.
* Concurrent execution: all agents are awaited in parallel using
  asyncio.gather.
* Timeout handling: the entire orchestration is bounded by a configurable
  timeout (default 200 ms). If the timeout is exceeded, the function
  returns partial results with a TimeoutError for the unfinished
  agents.
* Simple Agent interface: an agent must expose an async `run(request)`
  coroutine that returns a string result.

Usage
-----
>>> from orchestrator.orchestration_algorithm import orchestrate, DummyAgent
>>> agents = [DummyAgent('A'), DummyAgent('B'), DummyAgent('C')]
>>> results = await orchestrate(agents, request_id='12345')
>>> print(results)
{'A': 'A-12345', 'B': 'B-12345', 'C': 'C-12345'}
"""

import asyncio
import hashlib
import time
from typing import Any, Dict, Iterable, List, Sequence, Tuple

# --------------------------------------------------------------------------- #
# Agent interface
# --------------------------------------------------------------------------- #
class Agent:
    """
    Base class for LLM agents.

    Subclasses must implement the async `run(request: Any) -> str` method.
    """
    name: str

    async def run(self, request: Any) -> str:
        raise NotImplementedError


# --------------------------------------------------------------------------- #
# Orchestration logic
# --------------------------------------------------------------------------- #
def _hash_request(request_id: str) -> int:
    """Return a deterministic integer hash for the request identifier."""
    return int(hashlib.sha256(request_id.encode()).hexdigest(), 16)


def _deterministic_order(
    agents: Sequence[Agent], request_id: str
) -> List[Agent]:
    """
    Return a deterministic ordering of agents based on the request_id.

    The ordering is a rotation of the agents sorted by name, starting at
    an index derived from the request_id hash.
    """
    sorted_agents = sorted(agents, key=lambda a: a.name)
    start_index = _hash_request(request_id) % len(sorted_agents)
    return sorted_agents[start_index:] + sorted_agents[:start_index]


async def orchestrate(
    agents: Iterable[Agent],
    request_id: str,
    timeout: float = 0.2,
) -> Dict[str, str]:
    """
    Orchestrate the given agents for the specified request.

    Parameters
    ----------
    agents : Iterable[Agent]
        The LLM agents to invoke.
    request_id : str
        Identifier for the request; used to deterministically order agents.
    timeout : float, optional
        Maximum allowed time in seconds for the entire orchestration.
        Defaults to 0.2 (200 ms).

    Returns
    -------
    Dict[str, str]
        Mapping from agent name to its result. If an agent fails or times
        out, its entry will be the exception string.
    """
    ordered_agents = _deterministic_order(list(agents), request_id)

    async def _run_agent(agent: Agent) -> Tuple[str, Any]:
        try:
            result = await agent.run(request_id)
            return agent.name, result
        except Exception as exc:
            return agent.name, f"Error: {exc}"

    # Start all agents concurrently
    tasks = [_run_agent(a) for a in ordered_agents]
    try:
        results = await asyncio.wait_for(
            asyncio.gather(*tasks), timeout=timeout
        )
    except asyncio.TimeoutError:
        # If timeout occurs, gather partial results
        results = []
        for task in tasks:
            if task.done():
                results.append(task.result())
            else:
                task.cancel()
                results.append((task.get_coro().cr_frame.f_locals['agent'].name, "Timeout"))

    return dict(results)


# --------------------------------------------------------------------------- #
# Dummy agent for testing and demonstration
# --------------------------------------------------------------------------- #
class DummyAgent(Agent):
    """
    Simple agent that returns its name appended with the request_id after a
    short sleep. Useful for unit tests and demonstrations.
    """

    def __init__(self, name: str, sleep_ms: int = 50):
        self.name = name
        self.sleep_ms = sleep_ms

    async def run(self, request: Any) -> str:
        await asyncio.sleep(self.sleep_ms / 1000.0)
        return f"{self.name}-{request}"


# --------------------------------------------------------------------------- #
# If run as a script, demonstrate usage
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    async def demo():
        agents = [DummyAgent("A"), DummyAgent("B"), DummyAgent("C")]
        start = time.perf_counter()
        results = await orchestrate(agents, request_id="demo-123")
        elapsed = (time.perf_counter() - start) * 1000
        print(f"Results: {results}")
        print(f"Elapsed: {elapsed:.2f} ms")

    asyncio.run(demo())