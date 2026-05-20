
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from axentx.services.alert_service import AlertService

router = APIRouter()
alert_service = AlertService()

@router.post("/test-alert")
async def test_alert():
    try:
        response = await alert_service.send_test_alert()
        return JSONResponse(content={"message": "Test alert sent successfully"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))