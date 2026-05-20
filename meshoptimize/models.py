from __future__ import annotations

from typing import List, Dict, Any
from pydantic import BaseModel, Field, validator


class MeshData(BaseModel):
    """Input mesh representation."""
    vertices: List[List[float]] = Field(..., description="List of [x, y, z] coordinates")
    faces: List[List[int]] = Field(..., description="List of triangle vertex indices")

    @validator("vertices")
    def vertices_must_be_3d(cls, v):
        if not all(len(coord) == 3 for coord in v):
            raise ValueError("Each vertex must have 3 coordinates")
        return v

    @validator("faces")
    def faces_must_have_three_vertices(cls, v):
        if not all(len(face) == 3 for face in v):
            raise ValueError("Each face must reference 3 vertices")
        return v


class OptimizedMesh(BaseModel):
    """Response from the /optimize endpoint."""
    optimized_vertices: List[List[float]]
    optimized_faces: List[List[int]]


class MeshDetails(BaseModel):
    """Response from the /mesh/{mesh_id} endpoint."""
    mesh_id: str
    vertices: List[List[float]]
    faces: List[List[int]]