"""
Utility module for loading and querying regulatory controls.
"""

import json
import pathlib
from typing import Dict, Set


def load_controls(control_file: pathlib.Path) -> Dict[str, Set[str]]:
    """
    Load controls from a JSON file.

    Returns a mapping from control name to a set of resource types that
    satisfy the control.
    """
    try:
        with control_file.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        raise ValueError(f"Invalid control file: {e}") from e

    controls = {}
    for ctrl in data.get("controls", []):
        name = ctrl.get("name")
        types = set(ctrl.get("resource_types", []))
        if name:
            controls[name] = types
    return controls


def get_controls_for_resource(
    resource_type: str, controls: Dict[str, Set[str]]
) -> Set[str]:
    """
    Return the set of controls that apply to a given resource type.
    """
    return {name for name, types in controls.items() if resource_type in types}