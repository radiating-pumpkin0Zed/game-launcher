import os

DEFAULT_GAMES_DIR = os.path.join(os.path.expanduser("~"), "games")
ENV_FILE = os.path.join(os.path.dirname(__file__), ".env")


def load_env_file() -> None:
    if not os.path.exists(ENV_FILE):
        return

    try:
        with open(ENV_FILE, "r") as env_file:
            for raw_line in env_file:
                line = raw_line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue

                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip().strip("\"'")
                os.environ.setdefault(key, value)
    except OSError:
        return


def get_games_dir() -> str:
    load_env_file()
    return os.environ.get("GAMES_DIR", DEFAULT_GAMES_DIR)

def get_games():
    games = []
    games_dir = get_games_dir()

    if not os.path.isdir(games_dir):
        return games

    for filename in os.listdir(games_dir):
        name, ext = os.path.splitext(filename)
        ext = ext.lower()

        if ext in (".lnk", ".url"):
            games.append({
                "name": name,
                "type": ext,
                "path": os.path.join(games_dir, filename),
            })

    games.sort(key=lambda g: g["name"].lower())
    return games

if __name__ == "__main__":
    for game in get_games():
        print(f"[{game['type']}] {game['name']}")
