from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Request
import os
import yaml
import datetime
from typing import Optional

router = APIRouter()

# Dummy authentication dependency
def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    token = auth_header.split(" ", 1)[1]
    # In a real system, validate the token and fetch the user.
    # Here we simply use the token string as a placeholder username.
    username = token
    return username

@router.post("/submit_template")
async def submit_template(
    file: UploadFile = File(...),
    current_user: str = Depends(get_current_user),
):
    """
    Endpoint to receive a template submission.
    Expects a YAML file upload.
    Saves the file under templates/community/<username>_<timestamp>.yaml
    """
    try:
        content = await file.read()
        # Validate YAML
        yaml.safe_load(content)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid YAML: {e}")

    # Ensure directory exists
    base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates", "community")
    os.makedirs(base_dir, exist_ok=True)

    timestamp = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    safe_username = "".join(c for c in current_user if c.isalnum() or c in ("-", "_")).lower()
    filename = f"{safe_username}_{timestamp}.yaml"
    file_path = os.path.join(base_dir, filename)

    with open(file_path, "wb") as f:
        f.write(content)

    return {"detail": "Template submitted successfully", "path": f"templates/community/{filename}"}