import os
from .utils.secrets import get_secret_value

def load_environment_config() -> dict:
    """
    Load configuration based on the current environment (Docker or Kubernetes).
    Returns a dictionary with configuration values.
    """
    config = {}

    # Detect environment type
    is_k8s = is_kubernetes_environment()
    config['env_type'] = 'kubernetes' if is_k8s else 'docker'

    # Load secrets from appropriate sources
    secrets = {
        'api_key': get_secret_value('SURROGATE_API_KEY'),
        'database_url': get_secret_value('DB_URL'),
        'model_path': get_secret_value('MODEL_PATH'),
        'dataset_repo': get_secret_value('DATASET_REPO'),
    }

    # Fallback to environment variables if secrets are missing
    for key, value in secrets.items():
        if value is None:
            env_var = f"{key.upper()}"
            secrets[key] = os.getenv(env_var)

    config.update(secrets)
    return config