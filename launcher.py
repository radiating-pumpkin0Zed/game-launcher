import subprocess
import json
import os
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")

def load_data() -> dict:
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}

def save_last_played(game_name: str) -> None:
    data = load_data()
    data[game_name] = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def launch_game(game: dict) -> None:
    result = subprocess.run(
            ["wslpath", "-w", game["path"]],
            capture_output=True,
            text=True
    )
    if result.returncode != 0:
        return

    windows_path = result.stdout.strip()
    if not windows_path:
        return

    try:
        subprocess.Popen(
                ["cmd.exe", "/c", "start", "", windows_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
        )
    except OSError:
        return

    save_last_played(game["name"])
