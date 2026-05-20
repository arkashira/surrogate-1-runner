import logging
import traceback

class Emulator:
    def __init__(self):
        self.status = {'logs': [], 'errors': []}

    def get_status(self):
        return self.status

    def log(self, message):
        self.status['logs'].append(message)
        logging.info(message)

    def error(self, message, exception=None):
        error_message = message
        if exception:
            error_message += '\n' + traceback.format_exc()
        self.status['errors'].append(error_message)
        logging.error(error_message)