import chardet

def detect_encoding(text):
    """
    Detects the encoding of a given text.

    Args:
        text (str): The text to detect the encoding for.

    Returns:
        str: The detected encoding.
    """
    detector = chardet.UniversalDetector()
    detector.feed(text)
    detector.close()
    return detector.result['encoding']

def normalize_encoding(text, encoding):
    """
    Normalizes the encoding of a given text.

    Args:
        text (str): The text to normalize the encoding for.
        encoding (str): The detected encoding.

    Returns:
        str: The text with normalized encoding.
    """
    if encoding == 'utf-8':
        return text
    else:
        return text.encode('utf-8', errors='replace').decode('utf-8')

def main(text):
    """
    Main function to detect and normalize the encoding of a given text.

    Args:
        text (str): The text to detect and normalize the encoding for.

    Returns:
        str: The text with normalized encoding.
    """
    encoding = detect_encoding(text)
    return normalize_encoding(text, encoding)