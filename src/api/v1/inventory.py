from fastapi import APIRouter
from src.aws_ingest import get_aws_resources

router = APIRouter()

@router.get("/inventory")
def get_inventory():
    data = get_aws_resources()
    return data