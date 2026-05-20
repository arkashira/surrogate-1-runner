from __future__ import annotations

from typing import Any, List

from . import database as db


class Template:
    """
    Domain object representing a workflow template.

    A template consists of:
      * a unique ``name`` (primary key)
      * a free‑form ``description``
      * an ordered list of ``steps`` – each step can be any JSON‑serialisable object
    """

    def __init__(self, name: str, description: str, steps: List[Any] | None = None):
        self.name = name
        self.description = description
        self.steps: List[Any] = steps if steps is not None else []

    @classmethod
    def create(cls, name: str, description: str) -> Template:
        """Create a brand‑new template. Raises if the name already exists."""
        if db.get_template(name) is not None:
            raise ValueError(f"A template with name '{name}' already exists.")
        tmpl = cls(name, description, [])
        db.save_template(name, description, [])
        return tmpl

    @classmethod
    def load(cls, name: str) -> Template:
        """Load an existing template from the database. Raises if not found."""
        record = db.get_template(name)
        if record is None:
            raise ValueError(f"Template '{name}' does not exist.")
        return cls(record["name"], record["description"], record["steps"])

    def add_step(self, step: Any) -> None:
        """Append a step to the template and persist the change."""
        self.steps.append(step)
        db.add_step(self.name, step)

    def remove_step(self, index: int) -> None:
        """Remove a step by its index and persist the change."""
        if not (0 <= index < len(self.steps)):
            raise IndexError("Step index out of range.")
        del self.steps[index]
        db.remove_step(self.name, index)

    def save(self) -> None:
        """Persist the current in‑memory state (useful after bulk edits)."""
        db.save_template(self.name, self.description, self.steps)

    def __repr__(self) -> str:
        return (
            f"Template(name={self.name!r}, description={self.description!r}, "
            f"steps={self.steps!r})"
        )