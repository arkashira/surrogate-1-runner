from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional
from root_cause_analysis import RootCauseAnalysis

app = FastAPI()
root_cause_analyzer = RootCauseAnalysis()

class IncidentData(BaseModel):
    incident_id: str
    incident_data: Dict

@app.post("/analyze_incident")
async def analyze_incident(incident_data: IncidentData):
    """
    Endpoint to analyze an incident and generate root cause insights.

    Args:
        incident_data (IncidentData): The incident data including incident ID and incident details.

    Returns:
        Dict: The root cause insights and recommendations.
    """
    try:
        report = root_cause_analyzer.analyze_incident(incident_data.incident_id, incident_data.incident_data)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get_incident_report/{incident_id}")
async def get_incident_report(incident_id: str):
    """
    Endpoint to retrieve the incident report for a given incident ID.

    Args:
        incident_id (str): The unique identifier for the incident.

    Returns:
        Optional[Dict]: The incident report if found, otherwise None.
    """
    report = root_cause_analyzer.get_incident_report(incident_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Incident report not found")
    return report