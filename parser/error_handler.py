import logging
from typing import Any

logger = logging.getLogger(__name__)

class ErrorHandler:
    def __init__(self):
        self.recovered_data = []

    def handle_parsing_error(self, data: Any, error: Exception) -> Any:
        """
        Recover from parsing errors without losing data.
        Logs detailed error information for debugging.
        """
        logger.error(f"Parsing error encountered: {error}. Attempting recovery.")
        
        try:
            # Attempt to isolate the problematic part of the data
            if isinstance(data, dict):
                for key, value in data.items():
                    try:
                        # Simulate parsing (replace with actual parsing logic)
                        parsed_value = str(value)  # Example conversion
                        self.recovered_data.append({key: parsed_value})
                    except Exception as e:
                        logger.error(f"Failed to parse value for key '{key}': {e}")
            elif isinstance(data, list):
                for item in data:
                    try:
                        # Simulate parsing (replace with actual parsing logic)
                        parsed_item = str(item)  # Example conversion
                        self.recovered_data.append(parsed_item)
                    except Exception as e:
                        logger.error(f"Failed to parse item: {e}")
            else:
                logger.warning("Unsupported data type for error recovery.")
            
            return self.recovered_data
        
        except Exception as e:
            logger.critical(f"Error recovery failed: {e}")
            raise

    def log_error_details(self, error: Exception, data: Any):
        """
        Log detailed error information for debugging purposes.
        """
        logger.error(f"Error details: {error}")
        logger.error(f"Data at time of error: {data}")

# Test cases
def test_error_handler():
    handler = ErrorHandler()
    
    # Test with dictionary containing an unparsable value
    test_dict = {'valid_key': 'valid_value', 'error_key': object()}
    recovered_dict = handler.handle_parsing_error(test_dict, ValueError("Dictionary parsing error"))
    assert len(recovered_dict) == 1  # Only the valid key should be recovered
    
    # Test with list containing an unparsable item
    test_list = ['valid_item', object()]
    recovered_list = handler.handle_parsing_error(test_list, ValueError("List parsing error"))
    assert len(recovered_list) == 1  # Only the valid item should be recovered
    
    print("All tests passed.")

test_error_handler()