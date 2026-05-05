# tests/unit/test_sla.py
import pytest
from src.lib.sla import classify_sla, compute_summary

def test_classify_sla_met():
    created = datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    resolved = datetime(2025, 1, 2, 0, 0, 0, tzinfo=timezone.utc)  # 24h
    assert classify_sla(created, resolved, status="closed") == "met_sla"

def test_classify_sla_breached_closed():
    created = datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    resolved = datetime(2025, 1, 4, 1, 0, 0, tzinfo=timezone.utc)  # 73h
    assert classify_sla(created, resolved, status="closed") == "breached"

def test_classify_sla_at_risk_open():
    now = datetime(2025, 1, 2, 12, 0, 0, tzinfo=timezone.utc)
    created = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)  # 24h old
    assert classify_sla(created, None, status="open", now=now) == "at_risk"

def test_classify_sla_breached_open():
    now = datetime(2025, 1, 3, 12, 0, 0, tzinfo=timezone.utc)
    created = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)  # 48h old
    assert classify_sla(created, None, status="open", now=now) == "breached"

def test_compute_summary_empty():
    summary = compute_summary([])
    assert summary == {"open": 0, "breached": 0, "at_risk": 0, "met_sla": 0, "avg_time_to_resolution_hours": None}

def test_compute_summary_mixed():
    rows = [
        {"created_at": datetime(2025,1,1,0,0,0,tzinfo=timezone.utc), "resolved_at": datetime(2025,1,2,0,0,0,tzinfo=timezone.utc), "status": "closed"},
        {"created_at": datetime(2025,1,1,0,0,0,tzinfo=timezone.utc), "resolved_at": None, "status": "open"},
    ]
    summary = compute_summary(rows)
    assert summary["met_sla"] == 1
    assert summary["open"] == 1
    assert summary["avg_time_to_resolution_hours"] == 24.0