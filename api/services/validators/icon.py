class IconValidator:
    """Validates app icons against App Store requirements."""

    REQUIRED_SIZE = (1024, 1024)
    SUPPORTED_FORMATS = {'PNG', 'JPEG', 'JPG'}

    def __init__(self):
        self.errors = []
        self.warnings = []

    def validate(self, file_path: str) -> Dict:
        """
        Validate an icon file.

        Args:
            file_path: Path to the icon file

        Returns:
            Dict with validation results
        """
        self.errors = []
        self.warnings = []

        if not os.path.exists(file_path):
            self.errors.append(f"File not found: {file_path}")
            return self._result()

        self._validate_format(file_path)
        self._validate_dimensions(file_path)
        self._validate_transparency(file_path)

        return self._result()

    def _validate_format(self, file_path: str) -> None:
        """Check if file format is supported."""
        ext = os.path.splitext(file_path)[1].upper().replace('.', '')
        if ext not in self.SUPPORTED_FORMATS:
            self.errors.append(
                f"Unsupported format: {ext}. Supported: {', '.join(self.SUPPORTED_FORMATS)}"
            )

    def _validate_dimensions(self, file_path: str) -> None:
        """Check if dimensions match required App Store size."""
        try:
            with Image.open(file_path) as img:
                width, height = img.size

                if (width, height) != self.REQUIRED_SIZE:
                    self.errors.append(
                        f"Invalid dimensions: {width}x{height}. "
                        f"App Store requires: {self.REQUIRED_SIZE[0]}x{self.REQUIRED_SIZE[1]}"
                    )
                elif width != height:
                    self.errors.append(
                        f"Icon must be square. Got: {width}x{height}"
                    )
        except Exception as e:
            self.errors.append(f"Failed to read image: {str(e)}")

    def _validate_transparency(self, file_path: str) -> None:
        """Check transparency support based on format."""
        ext = os.path.splitext(file_path)[1].upper().replace('.', '')

        if ext in ('JPEG', 'JPG'):
            self.warnings.append(
                "JPEG does not support transparency. Consider using PNG for icons."
            )

    def _result(self) -> Dict:
        """Return validation result."""
        return {
            'valid': len(self.errors) == 0,
            'errors': self.errors,
            'warnings': self.warnings,
        }