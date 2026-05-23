from fastapi import Request
from fastapi.responses import JSONResponse
from audit_logger import AuditLogger

audit_logger = AuditLogger()

async def audit_logging_middleware(request: Request, call_next):
    user_ip = request.client.host
    service_type = request.headers.get("X-Service-Type", "Unknown")

    audit_logger.log_request(user_ip, service_type)

    response = await call_next(request)
    return response