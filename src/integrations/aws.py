
import boto3
from typing import Dict

class AWSCostIntegration:
    def __init__(self, access_key: str, secret_key: str, region: str):
        self.client = boto3.client(
            'cost-explorer',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )

    def get_cost_and_usage(self, start_date: str, end_date: str) -> Dict:
        response = self.client.get_cost_and_usage(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Granularity='DAILY',
            Metrics=[
                'BlendedCost'
            ],
            Filter={
                'Dimension': [
                    {
                        'Name': 'ServiceCode',
                        'Values': [
                            'AWS::All'
                        ]
                    }
                ]
            }
        )
        return response['ResultsByTime'][0]['Groups'][0]['Metrics']['BlendedCost']

# src/api/endpoints/integrations.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict
from datetime import datetime, timedelta
from . import models, schemas, database
from .aws import AWSCostIntegration

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/aws_cost", response_model=schemas.AWSCostResponse)
def get_aws_cost(aws_credentials: schemas.AWSCredentials, db: Session = Depends(get_db)):
    integration = models.AWSIntegration(**aws_credentials.dict())
    db.add(integration)
    db.commit()
    aws_cost = AWSCostIntegration(
        access_key=integration.access_key,
        secret_key=integration.secret_key,
        region=integration.region
    ).get_cost_and_usage(
        start_date=(datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
        end_date=datetime.now().strftime('%Y-%m-%d')
    )
    return {
        "total_cost": sum(aws_cost.values())
    }