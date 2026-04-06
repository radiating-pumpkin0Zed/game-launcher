import subprocess
import json
import os
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")

def load_data() -> dict:
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

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
    windows_path = result.stdout.strip()
    subprocess.Popen(
            ["cmd.exe", "/c", "start", "", windows_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
    )
    save_last_played(game["name"])

