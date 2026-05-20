import json

def test_generate_tip(client, app):
    # Seed a tip
    from app.models import Tip
    tip = Tip(content="Test tip", category="marketing")
    app.db.session.add(tip)
    app.db.session.commit()

    resp = client.get("/api/tips/generate?user_id=u1")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["tip_id"] == tip.id
    assert data["content"] == tip.content
    assert data["category"] == tip.category

def test_generate_missing_user(client):
    resp = client.get("/api/tips/generate")
    assert resp.status_code == 400
    assert resp.get_json()["message"] == "User ID is required"

def test_generate_no_tips(client):
    resp = client.get("/api/tips/generate?user_id=u1")
    assert resp.status_code == 404
    assert resp.get_json()["message"] == "No tips available"