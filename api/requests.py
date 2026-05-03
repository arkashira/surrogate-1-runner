--- a/api/requests.py
+++ b/api/requests.py
@@ -1,5 +1,6 @@
 from datetime import datetime
 from typing import Any, Dict, List, Optional
+from pydantic import BaseModel
 from fastapi import APIRouter, HTTPException, Request, Depends
 from starlette.responses import JSONResponse

@@ -8,6 +9,16 @@
 router = APIRouter()

+class PublicSLA(BaseModel):
+    target_resolution_hours: Optional[int]
+    status: str  # e.g., "on_track", "at_risk", "breached"
+    due_at: Optional[datetime]
+
+class PublicTimelineEvent(BaseModel):
+    timestamp: datetime
+    status: str
+    description: str
+
+class PublicRequest(BaseModel):
+    slug: str
+    title: str
+    status: str
+    timeline: List[PublicTimelineEvent]
+    sla: PublicSLA
+
+def _strip_internal(payload: Dict[str, Any]) -> Dict[str, Any]:
+    """Remove internal-only keys from a request payload."""
+    internal_keys = {
+        "id",
+        "assignee_id",
+        "assignee",
+        "internal_notes",
+        "team_tags",
+        "escalation_reason",
+        "created_by_user_id",
+        "created_by",
+        "updated_by_user_id",
+        "updated_by",
+        "tenant_id",
+        "workspace_id",
+        "permissions",
+        "edit_token",
+        "webhook_secret",
+        "internal_priority",
+        "raw_payload",
+        "processing_trace",
+    }
+    return {k: v for k, v in payload.items() if k not in internal_keys}
+
+def record_request_view(request_id: str, viewer_ip: Optional[str] = None, user_agent: Optional[str] = None) -> None:
+    """Record a public view event for audit/analytics."""
+    # Lightweight fire-and-forget; replace with real event bus/DB as needed.
+    # Example: write to a view_events table or emit to Kafka/Redis stream.
+    try:
+        # Placeholder: log or enqueue
+        # logger.info("public_view", extra={"request_id": request_id, "ip": viewer_ip, "ua": user_agent})
+        pass
+    except Exception:
+        # Never fail the response because of analytics
+        pass
+
+def build_public_request(raw: Dict[str, Any]) -> PublicRequest:
+    """Build a PublicRequest from raw DB row, stripping internals and mapping fields."""
+    safe = _strip_internal(raw)
+
+    # Map timeline if present; accept raw list of dicts with timestamp/status/description
+    raw_timeline = safe.get("timeline", [])
+    timeline: List[PublicTimelineEvent] = []
+    for item in raw_timeline:
+        if isinstance(item, dict):
+            timeline.append(
+                PublicTimelineEvent(
+                    timestamp=item.get("timestamp", item.get("created_at", datetime.utcnow())),
+                    status=item.get("status", "unknown"),
+                    description=item.get("description", ""),
+                )
+            )
+
+    # Map SLA
+    raw_sla = safe.get("sla", {})
+    sla = PublicSLA(
+        target_resolution_hours=raw_sla.get("target_resolution_hours"),
+        status=raw_sla.get("status", "unknown"),
+        due_at=raw_sla.get("due_at"),
+    )
+
+    return PublicRequest(
+        slug=safe.get("slug") or safe.get("public_slug") or str(safe.get("id", "")),
+        title=safe.get("title", ""),
+        status=safe.get("status", "unknown"),
+        timeline=timeline,
+        sla=sla,
+    )

 @router.get("/public/requests/{slug}", response_model=PublicRequest)
 async def get_public_request(
     slug: str,
     request: Request,
 ) -> PublicRequest:
     """
     Public status page for a request.
     Returns: title, status, timeline, and SLA info.
     Does not expose internal-only fields or edit controls.
     Records a view event.
     """
     # Fetch request from DB/service (placeholder)
     # Replace `fetch_raw_request_by_slug` with your actual data access.
     raw = await fetch_raw_request_by_slug(slug)
     if not raw:
         raise HTTPException(status_code=404, detail="Request not found")

+    # Record public view (non-blocking best-effort)
+    client_ip = request.client.host if request.client else None
+    user_agent = request.headers.get("user-agent")
+    record_request_view(request_id=str(raw.get("id", slug)), viewer_ip=client_ip, user_agent=user_agent)
+
+    # Build and return public-safe representation
+    public_payload = build_public_request(raw)
     return public_payload

# Existing helper (example) — adapt to your actual data layer
 async def fetch_raw_request_by_slug(slug: str) -> Optional[Dict[str, Any]]:
     # Placeholder: query your DB/cache and return raw row
     # Example: return await db.fetch_one("SELECT * FROM requests WHERE slug = $1", slug)
     return None