import logging

def handle_error(e, context):
    logging.error(f"Error {context}: {str(e)}")
    # additional error handling logic here
    # e.g. send error report, notify developer, etc.
    return f"Error {context}: {str(e)}"