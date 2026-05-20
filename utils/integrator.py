from typing import Dict
from services.integration_service import ITInfrastructureIntegrationService

def integrate_with_it_infrastructure(config: Dict) -> None:
    integration_service = ITInfrastructureIntegrationService()
    integration_service.integrate(config)