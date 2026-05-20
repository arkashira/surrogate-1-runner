"""
API endpoint for uploading Terraform/Helm configuration files.
The uploaded file is saved temporarily, parsed to extract
compliance-relevant resources, and the results are returned
as a JSON list.
"""

import os
import uuid
import shutil
from pathlib import Path
from typing import List, Dict, Optional
from fastapi import APIRouter, File, UploadFile, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from werkzeug.utils import secure_filename

# Configuration constants
ALLOWED_EXTENSIONS = {'tf', 'yaml', 'yml', 'hcl'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

# Dependency that ensures the upload directory exists
def get_upload_dir() -> Path:
    upload_dir = Path("/tmp/surrogate_uploads")
    upload_dir.mkdir(parents=True, exist_ok=True)
    return upload_dir

def allowed_file(filename: str) -> bool:
    """Check if the file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_compliance_resources(file_path: Path) -> List[Dict]:
    """
    Extract compliance-relevant resources from configuration files.
    In a real implementation, this would use proper parsers for Terraform/Helm.
    """
    resources = []

    try:
        with file_path.open("r", encoding="utf-8") as f:
            content = f.read()

            # Simple pattern matching for demonstration
            # In production, use proper parsers like terraform-py or helm libraries
            if file_path.suffix.lower() in ('.tf', '.hcl'):
                # Terraform resource extraction logic
                pass
            elif file_path.suffix.lower() in ('.yaml', '.yml'):
                # Helm/Helmfile resource extraction logic
                pass

            # Mock response structure for demonstration
            mock_resources = [
                {
                    "id": "aws_s3_bucket.example",
                    "type": "aws_s3_bucket",
                    "compliance_tags": ["data-encryption", "access-control"],
                    "description": "Example S3 bucket with encryption enabled",
                    "compliance_status": "compliant"
                },
                {
                    "id": "aws_iam_role.admin",
                    "type": "aws_iam_role",
                    "compliance_tags": ["least-privilege", "audit-logging"],
                    "description": "Admin role with minimal permissions",
                    "compliance_status": "non-compliant"
                }
            ]

            return mock_resources

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to parse configuration: {str(exc)}",
        )

router = APIRouter(prefix="/api")

@router.post("/upload",
            response_class=JSONResponse,
            response_model=Dict[str, Optional[List[Dict]]],
            status_code=status.HTTP_200_OK)
async def upload_config(
    file: UploadFile = File(...),
    upload_dir: Path = Depends(get_upload_dir),
) -> Dict[str, Optional[List[Dict]]]:
    """
    Accept a single file upload, store it temporarily,
    extract compliance-relevant resources, and return them.
    """
    # Validate file presence
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file provided"
        )

    # Validate file extension
    if not allowed_file(file.filename):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported file type. Allowed types: .tf, .yaml, .yml, .hcl"
        )

    # Validate file size
    if len(await file.read()) > MAX_CONTENT_LENGTH:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Maximum size is {MAX_CONTENT_LENGTH/1024/1024}MB"
        )
    await file.seek(0)  # Reset file pointer after size check

    # Generate a unique temporary filename
    filename = secure_filename(file.filename)
    temp_name = f"{uuid.uuid4()}_{filename}"
    temp_path = upload_dir / temp_name

    try:
        # Write the uploaded file to disk
        with temp_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Extract resources
        resources = extract_compliance_resources(temp_path)

        return {
            "message": "Configuration uploaded and processed successfully",
            "resources": resources
        }
    finally:
        # Clean up the temporary file
        if temp_path.exists():
            temp_path.unlink()