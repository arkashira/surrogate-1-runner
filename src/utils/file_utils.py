import os

def is_supported_invoice_format(file_path):
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()
    return file_extension in ['.pdf', '.jpg', '.jpeg', '.png']

def get_invoice_file_type(file_path):
    if is_supported_invoice_format(file_path):
        return "Supported Invoice Format"
    else:
        return "Unsupported Format"

# Example usage
if __name__ == "__main__":
    print(get_invoice_file_type("invoice.jpg"))  # Should output 'Supported Invoice Format'
    print(get_invoice_file_type("document.txt"))  # Should output 'Unsupported Format'