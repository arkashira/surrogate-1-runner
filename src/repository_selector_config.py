GITHUB_API_URL = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")

# Configuration for the repository selector feature
REPOSITORY_SELECTOR_CONFIG = {
    "max_repositories": 10,
    "refresh_interval": 3600,  # Refresh interval in seconds
    "dashboard_endpoint": "/dashboard/connected-repositories"
}