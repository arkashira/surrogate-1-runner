from typing import List

from .client import Client
from .models import Anomaly


class Costs:
    """
    High‑level wrapper that exposes cost‑related endpoints.
    """

    def __init__(self, client: Client) -> None:
        self.client = client

    def get_cost_anomalies(self) -> List[Anomaly]:
        """
        Retrieve cost anomalies from the API.

        Returns
        -------
        List[Anomaly]
            A list of `Anomaly` objects.
        """
        raw = self.client.get("/v1/costs/anomalies")
        return [Anomaly.from_dict(item) for item in raw]