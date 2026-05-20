import os
import shutil
import logging
import stat
from pathlib import Path
from typing import Optional
from fastapi import HTTPException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FileSystemConnector:
    def __init__(self, source_path: str, destination_path: str, permissions: int = 0o644):
        self.source_path = Path(source_path)
        self.destination_path = Path(destination_path)
        self.permissions = permissions

    def validate_source(self) -> bool:
        """Validate source file exists and is readable."""
        if not self.source_path.exists():
            raise FileNotFoundError(f"Source file '{self.source_path}' does not exist")
        if not os.access(self.source_path, os.R_OK):
            raise PermissionError(f"Source file '{self.source_path}' is not readable")
        return True

    def validate_destination(self) -> bool:
        """Validate destination directory exists and is writable."""
        dest_dir = self.destination_path.parent
        if not dest_dir.exists():
            raise FileNotFoundError(f"Destination directory '{dest_dir}' does not exist")
        if not os.access(dest_dir, os.W_OK):
            raise PermissionError(f"Destination directory '{dest_dir}' is not writable")
        return True

    def copy_file(self) -> dict:
        """Copy file from source to destination."""
        self.validate_source()
        self.validate_destination()
        
        shutil.copy2(self.source_path, self.destination_path)
        logger.info(f"Copied file from '{self.source_path}' to '{self.destination_path}'")
        
        return {
            "success": True,
            "operation": "copy",
            "source": str(self.source_path),
            "destination": str(self.destination_path)
        }

    def move_file(self) -> dict:
        """Move file from source to destination."""
        self.validate_source()
        self.validate_destination()
        
        shutil.move(str(self.source_path), str(self.destination_path))
        logger.info(f"Moved file from '{self.source_path}' to '{self.destination_path}'")
        
        return {
            "success": True,
            "operation": "move",
            "source": str(self.source_path),
            "destination": str(self.destination_path)
        }

    def set_permissions(self) -> dict:
        """Set permissions on destination file."""
        if not self.destination_path.exists():
            raise FileNotFoundError(f"Destination file '{self.destination_path}' does not exist")
        
        os.chmod(self.destination_path, self.permissions)
        logger.info(f"Set permissions for file '{self.destination_path}' to {oct(self.permissions)}")
        
        return {
            "success": True,
            "operation": "set_permissions",
            "path": str(self.destination_path),
            "permissions": oct(self.permissions)
        }

    def execute(self, operation: str) -> dict:
        """Execute the specified operation."""
        operations = {
            'copy': self.copy_file,
            'move': self.move_file,
            'set_permissions': self.set_permissions
        }
        
        if operation not in operations:
            raise ValueError(f"Unknown operation: {operation}")
        
        return operations[operation]()


# src/api/filesystem.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from connector.file_system import FileSystemConnector

router = APIRouter()

class FileOperationRequest(BaseModel):
    operation: str
    sourcePath: str
    destinationPath: str
    permissions: Optional[int] = 0o644

@router.post("/execute")
async def execute_file_operation(request: FileOperationRequest):
    """Execute a file system operation."""
    try:
        connector = FileSystemConnector(
            source_path=request.sourcePath,
            destination_path=request.destinationPath,
            permissions=request.permissions
        )
        result = connector.execute(request.operation)
        return {"success": True, "data": result}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))