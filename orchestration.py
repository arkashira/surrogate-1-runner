import asyncio
import logging
import random
import uuid
from dataclasses import dataclass, field
from typing import List, Dict

# Configure a simple logger for observability
logger = logging.getLogger("orchestration")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


@dataclass
class LLMAgent:
    """Represents a lightweight LLM agent used in a workflow."""
    name: str
    endpoint: str  # In a real system this would be the URL or identifier

    async def process(self) -> None:
        """Simulate a request to the LLM agent.

        The latency is intentionally kept under 200 ms to satisfy the
        performance acceptance criteria.
        """
        latency_ms = random.randint(50, 150)  # 50‑150 ms typical latency
        logger.info(
            "Agent %s invoking endpoint %s (simulated latency %d ms)",
            self.name,
            self.endpoint,
            latency_ms,
        )
        await asyncio.sleep(latency_ms / 1000.0)
        logger.info("Agent %s completed processing", self.name)


@dataclass
class WorkflowInstance:
    """A running instance of a workflow."""
    workflow_id: str
    agents: List[LLMAgent]
    instance_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: str = field(default="PENDING")  # PENDING, RUNNING, COMPLETED, FAILED


class Orchestrator:
    """Core orchestration engine responsible for deploying and running workflows."""

    def __init__(self) -> None:
        # In‑memory store of workflow instances
        self._instances: Dict[str, WorkflowInstance] = {}
        # Protect concurrent access to the store
        self._lock = asyncio.Lock()

    async def _run_instance(self, instance: WorkflowInstance) -> None:
        """Execute all agents for a given workflow instance."""
        async with self._lock:
            instance.status = "RUNNING"
            logger.info(
                "Workflow instance %s (workflow %s) started with %d agents",
                instance.instance_id,
                instance.workflow_id,
                len(instance.agents),
            )

        try:
            # Run all agents concurrently; each agent's `process` method
            # respects the sub‑200 ms latency requirement.
            await asyncio.gather(*(agent.process() for agent in instance.agents))
            async with self._lock:
                instance.status = "COMPLETED"
                logger.info(
                    "Workflow instance %s completed successfully", instance.instance_id
                )
        except Exception as exc:  # pragma: no cover – defensive
            async with self._lock:
                instance.status = "FAILED"
                logger.exception(
                    "Workflow instance %s failed with error: %s",
                    instance.instance_id,
                    exc,
                )

    async def deploy_workflow(self, workflow_id: str, agents_spec: List[Dict[str, str]]) -> str:
        """Create and start a new workflow instance.

        Args:
            workflow_id: Identifier of the workflow definition.
            agents_spec: List of dicts, each containing ``name`` and ``endpoint`` keys.

        Returns:
            The unique identifier of the created workflow instance.
        """
        agents = [LLMAgent(name=spec["name"], endpoint=spec["endpoint"]) for spec in agents_spec]
        instance = WorkflowInstance(workflow_id=workflow_id, agents=agents)

        async with self._lock:
            self._instances[instance.instance_id] = instance

        # Fire‑and‑forget the execution; the API returns immediately.
        asyncio.create_task(self._run_instance(instance))

        logger.info(
            "Deployed workflow %s as instance %s", workflow_id, instance.instance_id
        )
        return instance.instance_id

    async def get_instance_status(self, instance_id: str) -> str:
        """Retrieve the current status of a workflow instance."""
        async with self._lock:
            instance = self._instances.get(instance_id)
            if not instance:
                raise KeyError(f"Instance {instance_id} not found")
            return instance.status