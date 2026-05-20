import os

# In production you would load this from a secrets manager or env var
GITLAB_TOKEN = os.getenv("GITLAB_TOKEN", "default-token")