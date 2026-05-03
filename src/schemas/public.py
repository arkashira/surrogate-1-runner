
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

+ class RequestAuditEntry(BaseModel):
+     user: str
+     timestamp: datetime
+     previous_status: str
+     new_status: str
+     note: Optional[str] = None
+
+     class Config:
+         from_attributes = True

 class PublicRequestBase(BaseModel):
     id: str
     title: str
     status: str
     created_at: datetime
     updated_at: datetime

-class PublicRequestResponse(PublicRequestBase):
+ class PublicRequestResponse(PublicRequestBase):
+     audit: List[RequestAuditEntry] = []
+
+     class Config:
+         from_attributes = True