import psutil
import platform
from typing import Dict, List, Optional, Tuple

# Game configuration mapping process names to display names and suggestions
GAME_CONFIG = {
    "Counter-Strike 2.exe": {
        "name": "CS2",
        "suggestions": [
            "Enable DLSS 3.0 for ray tracing",
            "Set resolution to 1920x1080 for competitive play",
            "Disable VSync to reduce input lag"
        ]
    },
    "FIFA 24.exe": {
        "name": "FIFA 24",
        "suggestions": [
            "Adjust field of view to 90 for better peripheral vision",
            "Enable 3D audio for directional awareness",
            "Set graphics preset to Performance"
        ]
    }
}

def detect_game() -> Optional[Dict[str, any]]:
    """
    Detect currently running game by scanning active processes.
    
    Returns:
        Dictionary containing game info or None if no supported game found
    """
    # Handle Windows-specific process detection
    if platform.system() == 'Windows':
        for proc in psutil.process_iter(['name']):
            try:
                proc_name = proc.info['name']
                if proc_name in GAME_CONFIG:
                    return {
                        "name": GAME_CONFIG[proc_name]["name"],
                        "suggestions": GAME_CONFIG[proc_name]["suggestions"]
                    }
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                # Skip processes that disappear during iteration
                continue
    
    # Return None for unsupported platforms or no matches
    return None

def get_running_games() -> List[str]:
    """Get list of currently running game processes."""
    if platform.system() == 'Windows':
        running_games = []
        for proc in psutil.process_iter(['name']):
            try:
                proc_name = proc.info['name']
                if proc_name in GAME_CONFIG:
                    running_games.append(proc_name)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        return running_games
    return []

# For direct CLI usage
if __name__ == "__main__":
    game_info = detect_game()
    if game_info:
        print(f"Running game: {game_info['name']}")
        print("Suggestions:")
        for suggestion in game_info['suggestions']:
            print(f"  - {suggestion}")
    else:
        print("No game detected")