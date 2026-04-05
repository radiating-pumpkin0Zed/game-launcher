import os

GAMES_DIR = "/mnt/c/Users/Zedd/Desktop/games"

def get_games():
    games = []

    for filename in os.listdir(GAMES_DIR):
        name, ext = os.path.splitext(filename)
        ext = ext.lower()

        if ext in (".lnk", ".url"):
            games.append({
                "name": name,
                "type": ext,
                "path": os.path.join(GAMES_DIR, filename),
            })

    games.sort(key=lambda g: g["name"].lower())
    return games

if __name__ == "__main__":
    for game in get_games():
        print(f"[{game['type']}] {game['name']}")
