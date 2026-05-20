import os

class ComplianceChecker:
    """
    Simple compliance checker for AI model artifacts.
    Checks for banned keywords in the first 1MB of the file
    and enforces a maximum file size.
    """

    def __init__(self, banned_keywords=None, size_limit_bytes=None):
        """
        :param banned_keywords: list of strings to search for in binary data
        :param size_limit_bytes: maximum allowed file size in bytes
        """
        self.banned_keywords = banned_keywords or ["banned", "illegal"]
        self.size_limit_bytes = size_limit_bytes or 1 * 1024 * 1024 * 1024  # 1GB

    def check_artifact(self, artifact_path):
        """
        Analyze a single artifact and return a list of violation messages.
        :param artifact_path: path to the artifact file
        :return: list of strings describing violations
        """
        violations = []

        # Size check
        try:
            size = os.path.getsize(artifact_path)
            if size > self.size_limit_bytes:
                violations.append(
                    f"File size {size} exceeds limit {self.size_limit_bytes}"
                )
        except OSError as e:
            violations.append(f"Error accessing file: {e}")

        # Content check (first 1MB)
        try:
            with open(artifact_path, "rb") as f:
                data = f.read(1024 * 1024)  # read first 1MB
                for kw in self.banned_keywords:
                    if kw.encode() in data:
                        violations.append(f"Contains banned keyword: {kw}")
        except Exception as e:
            violations.append(f"Error reading file: {e}")

        return violations