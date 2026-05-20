from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from .. import crud, models, schemas
from ..database import get_db
from ..templates import templates

router = APIRouter()

@router.get("/c/{public_id}", response_class=HTMLResponse)
async def public_credential_page(
    public_id: str, 
    request: Request, 
    db: Session = Depends(get_db)
):
    credential = crud.get_credential_by_public_id(db, public_id=public_id)
    if not credential or not credential.holder.opt_in:
        raise HTTPException(status_code=404, detail="Credential not found")
    
    return templates.TemplateResponse(
        "credential_public.html",
        {
            "request": request, 
            "credential": credential,
            "badge_link": f"/c/{public_id}"
        }
    )