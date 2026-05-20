import subprocess
from typing import Optional

class AppleScriptPasteHandler:
    """
    Handles paste operations using AppleScript.
    """

    def __init__(self):
        """
        Initializes the AppleScript paste handler.
        """
        self.applescript = """
        tell application "System Events"
            keystroke "v" using {command down}
        end tell
        """

    def paste(self) -> Optional[str]:
        """
        Attempts to paste using AppleScript.

        Returns:
            Optional[str]: The result of the paste operation, or None if it fails.
        """
        try:
            process = subprocess.Popen(
                ['osascript', '-e', self.applescript],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = process.communicate()

            if process.returncode != 0:
                raise RuntimeError(f"AppleScript error: {stderr.decode()}")

            return stdout.decode().strip()
        except Exception as e:
            print(f"AppleScript paste failed: {e}")
            return None


# /opt/axentx/surrogate-1/src/core/paste_handler.py
from typing import Optional
from .paste_handlers.applescript_paste import AppleScriptPasteHandler

class PasteHandler:
    """
    Manages a chain of paste handlers.
    """

    def __init__(self):
        """
        Initializes the paste handler chain.
        """
        self.handlers = [
            # Add AX direct paste handler here
            # Add CGEvent Cmd+V handler here
            AppleScriptPasteHandler()
        ]

    def paste(self) -> Optional[str]:
        """
        Attempts to paste using each handler in the chain.

        Returns:
            Optional[str]: The result of the paste operation, or None if all handlers fail.
        """
        for handler in self.handlers:
            result = handler.paste()
            if result is not None:
                return result
        return None


# Example usage:
if __name__ == "__main__":
    paste_handler = PasteHandler()
    result = paste_handler.paste()
    if result is not None:
        print(f"Paste successful: {result}")
    else:
        print("Paste failed")