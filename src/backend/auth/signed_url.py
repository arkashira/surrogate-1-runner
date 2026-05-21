import hmac
import hashlib
import base64
import time
from typing import Tuple

class SignedURLException(Exception):
    pass

def generate_signed_url(secret_key: str, endpoint: str, expiration_seconds: int = 30) -> Tuple[str, float]:
    """
    Generates a one-time signed URL valid for a specified duration.
    
    Args:
        secret_key (str): The secret key used for signing the URL.
        endpoint (str): The endpoint to which the URL will point.
        expiration_seconds (int): The duration in seconds for which the URL will be valid.
        
    Returns:
        Tuple[str, float]: A tuple containing the signed URL and its expiration timestamp.
    """
    # Calculate the expiration timestamp
    expiration_timestamp = time.time() + expiration_seconds
    
    # Create the message to sign
    message = f"{endpoint}:{expiration_timestamp}"
    
    # Sign the message using HMAC-SHA256
    signature = hmac.new(
        secret_key.encode('utf-8'),
        msg=message.encode('utf-8'),
        digestmod=hashlib.sha256
    ).digest()
    
    # Encode the signature in Base64
    encoded_signature = base64.b64encode(signature).decode('utf-8')
    
    # Construct the signed URL
    signed_url = f"{endpoint}?signature={encoded_signature}&expires={expiration_timestamp}"
    
    return signed_url, expiration_timestamp

def validate_signed_url(signed_url: str, secret_key: str) -> bool:
    """
    Validates a signed URL.
    
    Args:
        signed_url (str): The signed URL to validate.
        secret_key (str): The secret key used for signing the URL.
        
    Returns:
        bool: True if the URL is valid, False otherwise.
    """
    try:
        # Parse the signed URL
        url_parts = signed_url.split('?')
        endpoint = url_parts[0]
        query_string = url_parts[1]
        
        params = dict(param.split('=') for param in query_string.split('&'))
        signature = params.get('signature')
        expires = float(params.get('expires', '0'))
        
        # Check if the URL has expired
        if time.time() > expires:
            raise SignedURLException("URL has expired")
        
        # Recreate the message to sign
        message = f"{endpoint}:{expires}"
        
        # Sign the message using HMAC-SHA256
        expected_signature = hmac.new(
            secret_key.encode('utf-8'),
            msg=message.encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()
        
        # Encode the expected signature in Base64
        expected_encoded_signature = base64.b64encode(expected_signature).decode('utf-8')
        
        # Compare the signatures
        return hmac.compare_digest(signature, expected_encoded_signature)
    
    except Exception as e:
        raise SignedURLException(f"Validation failed: {str(e)}")

# Example usage
if __name__ == "__main__":
    secret_key = "your_secret_key_here"
    endpoint = "/api/container/exec"
    
    signed_url, expiration = generate_signed_url(secret_key, endpoint)
    print(f"Generated Signed URL: {signed_url}")
    print(f"Expiration Timestamp: {expiration}")
    
    is_valid = validate_signed_url(signed_url, secret_key)
    print(f"URL Valid: {is_valid}")