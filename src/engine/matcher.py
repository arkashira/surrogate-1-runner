from typing import List, Optional
import random

class Matcher:
    def __init__(self, native_speakers: List[str]):
        self.native_speakers = native_speakers

    def find_match(self) -> Optional[str]:
        available_speakers = [speaker for speaker in self.native_speakers if self._is_available(speaker)]
        if not available_speakers:
            return None
        return random.choice(available_speakers)

    def _is_available(self, speaker: str) -> bool:
        # Placeholder logic for checking availability
        # In a real scenario, this could check a database or API endpoint
        return True  # Assume all speakers are always available for simplicity

def main():
    native_speakers = ["Alice", "Bob", "Charlie"]
    matcher = Matcher(native_speakers)
    matched_speaker = matcher.find_match()
    print(f"Matched with: {matched_speaker}")

if __name__ == "__main__":
    main()