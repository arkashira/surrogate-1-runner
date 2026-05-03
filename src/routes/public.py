
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

-from src.schemas.public import PublicRequestResponse
+ from src.schemas.public import PublicRequestResponse
+ from src.models import Request as RequestModel, RequestAudit as RequestAuditModel

router = APIRouter()

def get_db():
    # assumed existing dependency
    ...

@router.get("/public/requests/{request_id}", response_model=PublicRequestResponse)
def get_public_request(request_id: str, db: Session = Depends(get_db)):
    req = db.query(RequestModel).filter(RequestModel.id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")

+ audits = (
+     db.query(RequestAuditModel)
+     .filter(RequestAuditModel.request_id == request_id)
+     .order_by(RequestAuditModel.created_at.asc())
+     .all()
+ )
+
+ # Build response-compatible object with audit trail
+ response_data = {
+     **{c.name: getattr(req, c.name) for c in req.__table__.columns},
+     "audit": [
+         {
+             "user": a.user,
+             "timestamp": a.created_at,
+             "previous_status": a.previous_status,
+             "new_status": a.new_status,
+             "note": a.note,
+         }
+         for a in audits
+     ],
+ }
+
- return req
+ return PublicRequestResponse.model_validate(response_data)