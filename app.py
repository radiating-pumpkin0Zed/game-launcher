from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, ListView, ListItem, Label
from textual.containers import Horizontal, Vertical
from textual.widgets import Static
from launcher import launch_game, load_data

from parser import get_games

class GameLauncher(App):

    CSS_PATH = "app.tcss"
    TITLE = "Game Launcher"
    DEFAULT_CSS = """
    ListView .list-view--cursor {
        background: #00ff99;
        color: #0d0d0d;
    }
    """

    def compose(self) -> ComposeResult:
        self.games = get_games()
        yield Static("⚡ GAME LAUNCHER", id="header")
        with Horizontal():
            with Vertical(id="sidebar"):
                yield ListView(
                        *[ListItem(Label(g["name"])) for g in self.games]
                )
            with Vertical(id="detail"):
                yield Static("Select a game to see details", id="detail-text")
        yield Footer()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        index = event.list_view.index
        game = self.games[index]
        self.query_one("#detail-text", Static).update(
                f"Name: {game['name']}\nType: {game['type']}\nPath: {game['path']}"
        )

    def on_key(self, event) -> None:
        if event.key == "enter":
            index = self.query_one(ListView).index
            if index is not None:
                game = self.games[index]
                launch_game(game)
            
    def get_css_variables(self) -> dict[str, str]:
        variables = super().get_css_variables()
        variables["accent"] = "#00ff99"
        variables["highlight"] = "#00ff99"
        return variables
    
    def on_list_view_selected(self, event: ListView.Selected) -> None:
        index = event.list_view.index
        game = self.games[index]
        data = load_data()
        last_played = data.get(game["name"], "Never")
        self.query_one("#detail-text", Static).update(
            f"Name:        {game['name']}\n"
            f"Type:        {game['type']}\n"
            f"Path:        {game['path']}\n"
            f"Last Played: {last_played}"
        )     

if __name__ == "__main__":
    app = GameLauncher()
    app.run()
