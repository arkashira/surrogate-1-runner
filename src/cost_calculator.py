import time
import logging
from typing import Dict, Optional
from dataclasses import dataclass, field

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class CostRates:
    """Configurable cost rates for resources."""
    cpu_per_unit: float = 0.05
    memory_per_unit: float = 0.01
    storage_per_unit: float = 0.001
    network_per_unit: float = 0.0001


class CostCalculator:
    def __init__(self, cost_rates: Optional[CostRates] = None):
        """
        Initialize the CostCalculator.
        
        Args:
            cost_rates: Optional custom cost rates. Uses defaults if not provided.
        """
        self.cost_rates = cost_rates or CostRates()
        logger.info("CostCalculator initialized with rates: %s", self.cost_rates)

    def calculate_cost(self, deployment_preview: Dict) -> Dict:
        """
        Calculate the cost of the deployment preview.

        Args:
            deployment_preview (Dict): The deployment preview data.

        Returns:
            Dict: The cost breakdown per resource.

        Raises:
            ValueError: If deployment_preview is None or not a dictionary.
        """
        if not isinstance(deployment_preview, dict):
            raise ValueError("deployment_preview must be a dictionary")
        
        logger.info("Calculating cost for deployment preview: %s", deployment_preview)
        
        cost_breakdown = {}
        for resource, details in deployment_preview.items():
            try:
                cost = self._calculate_resource_cost(resource, details)
                cost_breakdown[resource] = round(cost, 2)  # Consistent rounding
            except Exception as e:
                logger.error(f"Error calculating cost for {resource}: {e}")
                cost_breakdown[resource] = 0.0
        
        return cost_breakdown

    def _calculate_resource_cost(self, resource: str, details: Dict) -> float:
        """
        Calculate the cost of a single resource.

        Args:
            resource (str): The resource type.
            details (Dict): The details of the resource.

        Returns:
            float: The cost of the resource.
        """
        if not isinstance(details, dict):
            logger.warning(f"Invalid details for resource {resource}: {details}")
            return 0.0

        if resource == "compute":
            cpu_cost = details.get("cpu", 0) * self.cost_rates.cpu_per_unit
            memory_cost = details.get("memory", 0) * self.cost_rates.memory_per_unit
            return cpu_cost + memory_cost
        elif resource == "storage":
            return details.get("size", 0) * self.cost_rates.storage_per_unit
        elif resource == "network":
            return details.get("bandwidth", 0) * self.cost_rates.network_per_unit
        else:
            logger.warning(f"Unknown resource type: {resource}")
            return 0.0

    def get_deployment_preview(self) -> Dict:
        """
        Get the deployment preview data.

        Returns:
            Dict: The deployment preview data.
        """
        # Placeholder for actual deployment preview data retrieval logic
        return {
            "compute": {"cpu": 2, "memory": 4},
            "storage": {"size": 100},
            "network": {"bandwidth": 10}
        }

    def display_cost_breakdown(self, cost_breakdown: Dict) -> None:
        """
        Display the cost breakdown.

        Args:
            cost_breakdown (Dict): The cost breakdown per resource.
        """
        print("Cost Breakdown:")
        total = 0.0
        for resource, cost in cost_breakdown.items():
            print(f"{resource}: ${cost:.2f}")
            total += cost
        print(f"Total: ${total:.2f}")

    def run(self) -> None:
        """
        Run the cost calculator.
        """
        start_time = time.time()
        try:
            deployment_preview = self.get_deployment_preview()
            cost_breakdown = self.calculate_cost(deployment_preview)
            self.display_cost_breakdown(cost_breakdown)
        except Exception as e:
            logger.error(f"Error during cost calculation: {e}")
            print(f"Error: {e}")
        finally:
            end_time = time.time()
            print(f"Cost calculation completed in {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    cost_calculator = CostCalculator()
    cost_calculator.run()