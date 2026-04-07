import subprocess
import json
import os
from datetime import datetime


def get_data_file() -> str:
    state_home = os.environ.get(
        "XDG_STATE_HOME",
        os.path.join(os.path.expanduser("~"), ".local", "state"),
    )
    data_dir = os.path.join(state_home, "game-launcher")
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, "data.json")

def load_data() -> dict:
    data_file = get_data_file()
    if not os.path.exists(data_file):
        return {}
    try:
        with open(data_file, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}

def save_last_played(game_name: str) -> None:
    data = load_data()
    data[game_name] = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(get_data_file(), "w") as f:
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
