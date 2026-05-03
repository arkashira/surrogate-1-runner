# Optional pre-computed file list to avoid HF API list_repo_files/load_dataset(streaming=True)
# If provided, workers will iterate local list and fetch via CDN (no auth/API calls during data load).
FILE_LIST="${FILE_LIST:-}"