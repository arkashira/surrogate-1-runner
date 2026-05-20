def store(self, log_id: str, content: bytes, ...) -> str:
    safe_id = hashlib.sha256(log_id.encode()).hexdigest()[:16]
    file_path = storage_path / f"{safe_id}.enc"
    # Returns file_path, but caller has log_id - not file_path!