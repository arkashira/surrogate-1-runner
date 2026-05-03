from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional, Set, Tuple

from pydantic import BaseModel, Field, validator


class PipelineStage(str, Enum):
    RESEARCH = "research"
    SIGNAL = "signal"
    RISK = "risk"
    EXECUTION = "execution"


class PipelineState(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    REJECTED = "rejected"


# Strict forward-only flow
_ALLOWED_TRANSITIONS: Set[Tuple[PipelineStage, PipelineStage]] = {
    (PipelineStage.RESEARCH, PipelineStage.SIGNAL),
    (PipelineStage.SIGNAL, PipelineStage.RISK),
    (PipelineStage.RISK, PipelineStage.EXECUTION),
}


class PipelineTransitionEvent(BaseModel):
    from_stage: Optional[PipelineStage] = Field(
        None, description="Source stage (None for pipeline start)"
    )
    to_stage: PipelineStage = Field(..., description="Target stage")
    state: PipelineState = Field(
        default=PipelineState.RUNNING, description="Node state at transition"
    )
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="ISO 8601 UTC timestamp",
    )
    metadata: dict = Field(default_factory=dict, description="Optional context")

    class Config:
        frozen = True
        json_encoders = {
            PipelineStage: lambda v: v.value,
            PipelineState: lambda v: v.value,
        }


class PipelineNode(BaseModel):
    stage: PipelineStage
    state: PipelineState = PipelineState.PENDING
    config: dict = Field(default_factory=dict)

    def transition_to(self, next_stage: PipelineStage) -> PipelineTransitionEvent:
        """Validate and perform transition; emit immutable event."""
        if not is_valid_transition(self.stage, next_stage):
            raise ValueError(
                f"Invalid transition: {self.stage.value} -> {next_stage.value}"
            )
        previous = self.stage
        self.stage = next_stage
        self.state = PipelineState.RUNNING
        return PipelineTransitionEvent(
            from_stage=previous,
            to_stage=next_stage,
            state=self.state,
            metadata={"previous_stage": previous.value},
        )


class PipelineDefinition(BaseModel):
    id: str = Field(..., description="Unique pipeline identifier")
    name: str = Field(..., min_length=1, max_length=128)
    stages: List[PipelineNode] = Field(..., min_items=1)
    version: str = Field(default="1.0.0", regex=r"^\d+\.\d+\.\d+$")
    created_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    @validator("stages")
    def stages_must_be_unique_and_canonical(cls, v: List[PipelineNode]) -> List[PipelineNode]:
        if not v:
            return v

        stage_values = [node.stage for node in v]
        if len(set(stage_values)) != len(stage_values):
            raise ValueError("Stages must be unique within a pipeline definition")

        canonical_order = list(PipelineStage)
        indices = [canonical_order.index(s) for s in stage_values]

        # Must be strictly increasing to enforce canonical order without skips
        if indices != sorted(indices):
            raise ValueError(
                "Stages must follow canonical order: research -> signal -> risk -> execution"
            )

        # Disallow skips (e.g., research->risk) in definition
        for i in range(len(indices) - 1):
            if (canonical_order[indices[i]], canonical_order[indices[i + 1]]) not in _ALLOWED_TRANSITIONS:
                raise ValueError(
                    f"Invalid stage sequence in definition: "
                    f"{canonical_order[indices[i]].value} -> {canonical_order[indices[i + 1]].value}"
                )
        return v

    def validate_transition(self, from_stage: PipelineStage, to_stage: PipelineStage) -> bool:
        return is_valid_transition(from_stage, to_stage)

    def emit_initial_event(self) -> PipelineTransitionEvent:
        if not self.stages:
            raise ValueError("Pipeline has no stages")
        first_stage = self.stages[0].stage
        return PipelineTransitionEvent(
            from_stage=None,
            to_stage=first_stage,
            state=PipelineState.RUNNING,
        )


def is_valid_transition(
    from_stage: PipelineStage, to_stage: PipelineStage
) -> bool:
    """O(1) transition validation."""
    return (from_stage, to_stage) in _ALLOWED_TRANSITIONS


def validate_pipeline_definition(data: dict) -> PipelineDefinition:
    """Convenience validator for raw dict input."""
    return PipelineDefinition(**data)