import os

class InvoiceFormatDetector:
    def __init__(self, file_path):
        self.file_path = file_path

    def detect_format(self):
        _, file_extension = os.path.splitext(self.file_path)
        file_extension = file_extension.lower()

        if file_extension in ['.pdf']:
            return 'PDF'
        elif file_extension in ['.jpg', '.jpeg', '.png']:
            return 'IMAGE'
        else:
            return 'UNKNOWN'

# Example usage
if __name__ == "__main__":
    detector = InvoiceFormatDetector("example_invoice.pdf")
    print(detector.detect_format())  # Should output 'PDF'