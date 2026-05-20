import yaml
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

def load_config(config_path: str = "config.yaml") -> Optional[Dict[str, Any]]:
    """
    Load and validate configuration from a YAML file.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        Dictionary containing the configuration or None if invalid
    """
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {config_path}")
        return None
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML configuration: {e}")
        return None
    
    # Validate required fields
    required_fields = ['relay_endpoint', 'jwt_secret', 'chain_rpc_urls']
    missing_fields = [field for field in required_fields if field not in config]
    
    if missing_fields:
        logger.error(f"Missing required configuration fields: {missing_fields}")
        return None
    
    # Validate chain_rpc_urls is a dictionary
    if not isinstance(config['chain_rpc_urls'], dict):
        logger.error("chain_rpc_urls must be a dictionary")
        return None
    
    # Log successful loading
    logger.info("Configuration loaded successfully")
    return config