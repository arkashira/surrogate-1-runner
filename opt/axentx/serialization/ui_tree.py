"""JSON serialization utilities for Flutter UI component trees with full semantics support."""

from __future__ import annotations
import json
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Union
from enum import Enum

class UIComponentType(Enum):
    """Standardized UI component types for consistent serialization."""
    TEXT = "text"
    BUTTON = "button"
    IMAGE = "image"
    CONTAINER = "container"
    INPUT = "input"
    LIST_ITEM = "list_item"
    CUSTOM = "custom"
    SCAFFOLD = "scaffold"
    APP_BAR = "app_bar"
    COLUMN = "column"

@dataclass
class BoundingBox:
    """Represents the bounding box coordinates of a UI component."""
    x: float
    y: float
    width: float
    height: float

    def to_dict(self) -> Dict[str, float]:
        return {
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height
        }

@dataclass
class AccessibilityInfo:
    """Accessibility information for a UI component."""
    label: Optional[str] = None
    hint: Optional[str] = None
    value: Optional[str] = None
    is_enabled: bool = True
    is_focusable: bool = False
    screen_reader_text: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "isEnabled": self.is_enabled,
            "isFocusable": self.is_focusable
        }
        if self.label:
            result["label"] = self.label
        if self.hint:
            result["hint"] = self.hint
        if self.value:
            result["value"] = self.value
        if self.screen_reader_text:
            result["screenReaderText"] = self.screen_reader_text
        return result

@dataclass
class UIComponent:
    """A node in the Flutter Semantics/UI tree with full serialization support."""
    component_id: str
    component_type: Union[UIComponentType, str]
    bounds: BoundingBox
    accessibility: AccessibilityInfo
    children: List[UIComponent] = field(default_factory=list)
    properties: Dict[str, Any] = field(default_factory=dict)
    parent_id: Optional[str] = None
    depth: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert the component (including children) to a serializable dict."""
        data = {
            "id": self.component_id,
            "type": self.component_type.value if isinstance(self.component_type, UIComponentType) else self.component_type,
            "bounds": self.bounds.to_dict(),
            "accessibility": self.accessibility.to_dict(),
            "properties": self.properties,
            "depth": self.depth
        }
        if self.parent_id:
            data["parentId"] = self.parent_id
        if self.children:
            data["children"] = [child.to_dict() for child in self.children]
        return data

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> UIComponent:
        """Recreate a UIComponent (and its subtree) from a dict."""
        children_data = data.get("children", [])
        children = [UIComponent.from_dict(child) for child in children_data]

        try:
            component_type = UIComponentType(data["type"])
        except ValueError:
            component_type = data["type"]

        return UIComponent(
            component_id=data["id"],
            component_type=component_type,
            bounds=BoundingBox(**data["bounds"]),
            accessibility=AccessibilityInfo(**data.get("accessibility", {})),
            children=children,
            properties=data.get("properties", {}),
            parent_id=data.get("parentId"),
            depth=data.get("depth", 0)
        )

def serialize_ui_tree(root: UIComponent) -> str:
    """Serialize a UI component tree to a compact JSON string."""
    return json.dumps(
        root.to_dict(),
        ensure_ascii=False,
        separators=(",", ":")
    )

def deserialize_ui_tree(json_str: str) -> UIComponent:
    """Parse a JSON string back into a UIComponent tree."""
    data = json.loads(json_str)
    return UIComponent.from_dict(data)

__all__ = [
    "UIComponent",
    "UIComponentType",
    "BoundingBox",
    "AccessibilityInfo",
    "serialize_ui_tree",
    "deserialize_ui_tree",
]