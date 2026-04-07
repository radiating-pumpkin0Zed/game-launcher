from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Footer, Input, Label, ListItem, ListView, Static
from launcher import launch_game, load_data

from parser import get_games

class GameLauncher(App):

    CSS_PATH = "app.tcss"
    TITLE = "Game Launcher"
    BINDINGS = [
        ("enter", "launch", "Launch Game"),
        ("escape", "quit", "Quit"),
    ]
    DEFAULT_CSS = """
    ListView .list-view--cursor {
        background: #00ff99;
        color: #0d0d0d;
    }
    """

    def on_mount(self) -> None:
        self.query_one(Input).focus()
        self._refresh_list()

    def compose(self) -> ComposeResult:
        self.games = get_games()
        self.filtered_games = self.games.copy()
        yield Static("⚡ GAME LAUNCHER", id="header")
        with Horizontal():
            with Vertical(id="sidebar"):
                yield Input(placeholder="🔍 Search games...", id="search")
                yield ListView()
            with Vertical(id="detail"):
                yield Static("Select a game to see details", id="detail-text")
        yield Footer()

    def action_launch(self) -> None:
        game = self._get_selected_game()
        if game is None:
            return

        launch_game(game)
        self._update_detail(game)

    def get_css_variables(self) -> dict[str, str]:
        variables = super().get_css_variables()
        variables["accent"] = "#00ff99"
        variables["highlight"] = "#00ff99"
        return variables

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        index = event.list_view.index
        if index is None or index >= len(self.filtered_games):
            return

        self._update_detail(self.filtered_games[index])

    def on_input_changed(self, event: Input.Changed) -> None:
        query = event.value.strip().lower()
        self.filtered_games = [g for g in self.games if query in g["name"].lower()]
        self._refresh_list()

    def _get_selected_game(self) -> dict | None:
        list_view = self.query_one(ListView)
        index = list_view.index
        if index is None or index >= len(self.filtered_games):
            return None
        return self.filtered_games[index]

    def _refresh_list(self) -> None:
        list_view = self.query_one(ListView)
        list_view.clear()

        for game in self.filtered_games:
            list_view.append(ListItem(Label(game["name"])))

        if self.filtered_games:
            list_view.index = 0
            self._update_detail(self.filtered_games[0])
        else:
            self.query_one("#detail-text", Static).update("No games found.")

    def _update_detail(self, game: dict) -> None:
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
