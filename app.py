from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, ListView, ListItem, Label
from textual.containers import Horizontal, Vertical

from parser import get_games

class GameLauncher(App):

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            with Vertical(id="sidebar"):
                for game in get_games():
                    yield ListItem(Label(game["name"]))
            with Vertical(id="detail"):
                yield Label("Select a game to see detail")
        yield Footer()

if __name__ == "__main__":
    app = GameLauncher()
    app.run()
