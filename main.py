# Replace existing get_request with corrected version
@app.get("/requests/{request_id}", response_model=schemas.RequestResponse)
def get_request(request_id: int, db: Session = Depends(get_db)):
    db_request = db.query(models.Request).filter(models.Request.id == request_id).first()
    if not db_request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    # Order timeline events chronologically
    timeline_events = sorted(
        db_request.timeline_events,
        key=lambda x: x.timestamp
    )
    
    return {
        "id": db_request.id,
        "status": db_request.status,
        "timeline_events": timeline_events,
        "status_transitions": db_request.status_transitions
    }