import json
import sys
from typing import Dict, Any, Optional
from src.main.logger import logger

class Emulator:
    """Emulator for surrogate-1 dataset processing."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.status = {
            "running": False,
            "shard_id": None,
            "workers": 0,
            "status_endpoint": "/status"
        }
        logger.info("Emulator initialized with config: %s", json.dumps(config, indent=2))
    
    def validate_config(self) -> bool:
        """Validate emulator configuration."""
        required_keys = ["shard_id", "workers", "dataset_path"]
        
        for key in required_keys:
            if key not in self.config:
                logger.error(f"Missing required config key: {key}")
                raise ValueError(f"Configuration error: missing '{key}'")
        
        if not isinstance(self.config["workers"], int) or self.config["workers"] <= 0:
            logger.error("Invalid workers value: must be positive integer")
            raise ValueError("Configuration error: invalid 'workers' value")
        
        logger.info("Configuration validated successfully")
        return True
    
    def start(self):
        """Start the emulator."""
        if not self.validate_config():
            return
        
        self.status["running"] = True
        self.status["shard_id"] = self.config.get("shard_id")
        self.status["workers"] = self.config.get("workers", 1)
        
        logger.info("Emulator started with %d workers on shard %s", 
                   self.status["workers"], self.status["shard_id"])
    
    def stop(self):
        """Stop the emulator."""
        self.status["running"] = False
        logger.info("Emulator stopped")
    
    def get_status(self) -> Dict[str, Any]:
        """Return current emulator status."""
        return self.status.copy()
    
    def run(self):
        """Main run loop."""
        try:
            self.start()
            logger.info("Emulator running...")
            # Simulate work
            for i in range(10):
                logger.debug("Processing iteration %d", i)
                self.status["workers"] = self.config.get("workers", 1)
                logger.info("Workers active: %d", self.status["workers"])
        except Exception as e:
            logger.exception("Emulator failed: %s", str(e))
        finally:
            self.stop()


def main():
    """Entry point for emulator."""
    config = {
        "shard_id": "default",
        "workers": 1,
        "dataset_path": "/data/dataset"
    }
    
    try:
        emulator = Emulator(config)
        emulator.run()
    except Exception as e:
        logger.exception("Failed to start emulator: %s", str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()