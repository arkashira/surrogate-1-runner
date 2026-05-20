
"""
Minimal REST‑style view for template CRUD.
Assumes a simple in‑memory store for demo purposes.
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List

from django.http import (
    HttpResponse, HttpResponseBadRequest,
    HttpResponseNotAllowed, HttpResponseNotFound,
    JsonResponse,
)
from django.views.decorators.http import require_http_methods

# In‑memory store: id -> dict(name, content, version, history)
TEMPLATES: Dict[str, Dict] = {}


def _trim_history(history: List[Dict]) -> List[Dict]:
    """Keep only the last 30 days of history."""
    cutoff = datetime.utcnow() - timedelta(days=30)
    return [
        h for h in history
        if datetime.fromisoformat(h["timestamp"]) >= cutoff
    ]


@require_http_methods(["GET"])
def get_template(request, template_id: str) -> JsonResponse:
    tmpl = TEMPLATES.get(template_id)
    if not tmpl:
        return HttpResponseNotFound("Template not found")

    return JsonResponse(
        {
            "id": template_id,
            "name": tmpl["name"],
            "content": tmpl["content"],
            "version": tmpl["version"],
        }
    )


@require_http_methods(["POST"])
def save_template(request, template_id: str) -> JsonResponse:
    if template_id not in TEMPLATES:
        return HttpResponseNotFound("Template not found")

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    tmpl = TEMPLATES[template_id]

    # Optimistic concurrency
    if data.get("version") != tmpl["version"]:
        return JsonResponse(
            {"error": "Version conflict"}, status=409
        )

    # Archive current state
    tmpl["history"].append(
        {"timestamp": datetime.utcnow().isoformat(), "content": tmpl["content"]}
    )
    tmpl["history"] = _trim_history(tmpl["history"])

    # Apply changes
    tmpl["content"] = data["content"]
    tmpl["name"] = data.get("name", tmpl["name"])
    tmpl["version"] += 1

    return JsonResponse({"version": tmpl["version"]})