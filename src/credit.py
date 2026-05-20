from enum import Enum
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class CreditPool(Enum):
    """Enum to track which credit pool was used."""
    MONTHLY = "monthly"
    BULK = "bulk"
    NONE = "none"


class CreditSystem:
    """
    Manages monthly and bulk credit pools for job execution.
    
    Attributes:
        monthly_credits: Recurring monthly allocation
        bulk_credits: One-time purchased credits
    """
    
    def __init__(self, monthly_credits: int, bulk_credits: int):
        if monthly_credits < 0 or bulk_credits < 0:
            raise ValueError("Credit amounts cannot be negative")
        
        self._monthly_credits = monthly_credits
        self._bulk_credits = bulk_credits
    
    @property
    def monthly_credits(self) -> int:
        return self._monthly_credits
    
    @property
    def bulk_credits(self) -> int:
        return self._bulk_credits
    
    @property
    def total_credits(self) -> int:
        return self._monthly_credits + self._bulk_credits
    
    def deduct_credits(self, amount: int) -> Tuple[bool, CreditPool, str]:
        """
        Attempt to deduct credits from available pools.
        
        Args:
            amount: Number of credits to deduct
            
        Returns:
            Tuple of (success: bool, pool_used: CreditPool, message: str)
        """
        # Input validation
        if amount <= 0:
            return (False, CreditPool.NONE, "Amount must be positive")
        
        if amount > self.total_credits:
            return (False, CreditPool.NONE, 
                    f"Insufficient credits. Requested: {amount}, Available: {self.total_credits}")
        
        # Priority: monthly first, then bulk
        if self._monthly_credits >= amount:
            self._monthly_credits -= amount
            logger.info(f"Deducted {amount} from MONTHLY pool. Remaining: {self._monthly_credits}")
            return (True, CreditPool.MONTHLY, 
                    f"Successfully deducted {amount} credits from monthly pool")
        
        elif self._bulk_credits >= amount:
            self._bulk_credits -= amount
            logger.info(f"Deducted{amount} from BULK pool. Remaining: {self._bulk_credits}")
            return (True, CreditPool.BULK, 
                    f"Successfully deducted {amount} credits from bulk pool")
        
        # Fallback (shouldn't reach here given earlier check)
        return (False, CreditPool.NONE, "Both credit pools exhausted")
    
    def get_status(self) -> dict:
        """Return current credit status."""
        return {
            "monthly_credits": self._monthly_credits,
            "bulk_credits": self._bulk_credits,
            "total": self.total_credits,
            "pools_exhausted": {
                "monthly": self._monthly_credits == 0,
                "bulk": self._bulk_credits == 0
            }
        }


def get_credit_system(config: Optional[dict] = None) -> CreditSystem:
    """
    Factory function to create CreditSystem instance.
    
    Args:
        config: Optional configuration dict. If None, uses defaults.
        
    Returns:
        Configured CreditSystem instance
    """
    # Default values (should be loaded from config/database in production)
    defaults = {
        "monthly_credits": 100,
        "bulk_credits": 500
    }
    
    if config:
        defaults.update(config)
    
    return CreditSystem(
        monthly_credits=defaults["monthly_credits"],
        bulk_credits=defaults["bulk_credits"]
    )


def main():
    """Demonstrate credit system usage."""
    # Initialize with default or custom config
    credit_system = get_credit_system()
    
    print("=== Initial Status ===")
    print(f"Monthly: {credit_system.monthly_credits}")
    print(f"Bulk: {credit_system.bulk_credits}")
    print(f"Total: {credit_system.total_credits}\n")
    
    # Test deductions
    test_amounts = [10, 50, 200, 1000]
    
    print("=== Running Deduction Tests ===")
    for amount in test_amounts:
        success, pool, message = credit_system.deduct_credits(amount)
        print(f"Request: {amount} | Success: {success} | Pool: {pool.value} | {message}")
    
    print("\n=== Final Status ===")
    print(credit_system.get_status())


if __name__ == "__main__":
    main()