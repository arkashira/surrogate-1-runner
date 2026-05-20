import datetime
import threading
from typing import Any, Dict

from fastapi import APIRouter, HTTPException, Request, status

# Re‑use the singleton instance created in analytics_service.py
from surrogate_1.services.analytics_service import analytics_service

router = APIRouter()


def _fire_and_forget(fn, *args, **kwargs) -> None:
    """
    Run ``fn`` in a daemon thread.  The caller does not wait for the
    function to finish and the thread will not prevent process shutdown.
    """
    thread = threading.Thread(target=fn, args=args, kwargs=kwargs, daemon=True)
    thread.start()


@router.post("/simulation/complete", tags=["Roth Simulation"])
async def complete_simulation(request: Request) -> Dict[str, Any]:
    """
    Endpoint called when a user finishes a Roth simulation.

    Expected JSON body:
    {
        "user_id": "string",          # required
        "simulation_id": "string",   # required
        "details": { ... }            # optional, free‑form simulation data
    }
    """
    payload = await request.json()
    user_id: str | None = payload.get("user_id")
    simulation_id: str | None = payload.get("simulation_id")
    details: dict = payload.get("details", {})

    # Basic validation – keep it lightweight; deeper validation belongs to the
    # domain layer (outside the scope of this ticket).
    if not user_id or not simulation_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing required fields: user_id, simulation_id",
        )

    # ----------------------------------------------------------------------
    # 1️⃣  Business logic placeholder
    # ----------------------------------------------------------------------
    # Here you would persist the simulation, update user state, etc.
    # For this task we assume the simulation has already been recorded.

    # ----------------------------------------------------------------------
    # 2️⃣  Build the analytics payload
    # ----------------------------------------------------------------------
    event_payload = {
        "user_id": user_id,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "simulation_id": simulation_id,
        "details": details,
    }

    # ----------------------------------------------------------------------
    # 3️⃣  Fire‑and‑forget the analytics call
    # ----------------------------------------------------------------------
    _fire_and_forget(
        analytics_service.track_roth_simulation_completed,
        **event_payload,
    )

    return {"status": "ok", "message": "Simulation recorded"}