from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color, Canvas, Ellipse


colors = (
    (1, 0, 0),   # RED
    (0, 1, 0),   # GREEN
    (0, 0, 1),   # BLUE
    (1, 1, 0),   # YELLOW
    (1, 1, 1)    # WHITE
)

START_POSITION = (0, 0)
HOST_COLOR_ID = 0

# Do testow
positions = [(0, 0), (0, 100), (0, 200)]
positions2 = [(300, 60), (20, 450), (600, 200)]
positions3 = [(5, 4), (3, 8), (300, 300)]
pos = [positions, positions2, positions3]


def read_position(position):
    x, y = position.split('.')
    pos = (int(x), int(y))
    return pos


class GameLoopHost(GridLayout):
    def __init__(self, host, **kwargs):
        super(GameLoopHost, self).__init__(**kwargs)

        with self.canvas:
            self.background = Rectangle(pos=self.pos, size=(Window.width, Window.height), source='forest.jpg')

        self.host = host

        self.players_widgets = {}
        players = self.host.players
        self.players_widgets[self.host.username] = (Player(self.host.username, HOST_COLOR_ID, START_POSITION))

        for team in players:
            for player in players[team]:
                color_id = team
                self.players_widgets[player] = (Player(player, color_id, START_POSITION))

        for player_widget in self.players_widgets:
            self.add_widget(self.players_widgets[player_widget])

        Clock.schedule_interval(self.transfer_data, 1)

    def transfer_data(self, dt):
        positions = self.host.send_and_collect_data()

        self.players_widgets[self.host.username].update(read_position(positions[0]))

        for i in range(int(self.host.teams_no)):
            team_positions = positions[i + 1]

            for username in team_positions:
                position = team_positions[username]

                if position is None:
                    position = "0.0"

                self.players_widgets[username].update(read_position(position))


class GameLoopClient(GridLayout):
    def __init__(self, client, **kwargs):
        super(GameLoopClient, self).__init__(**kwargs)
        with self.canvas:
            self.background = Rectangle(pos=self.pos, size=(Window.width, Window.height), source='forest.jpg')

        self.client = client

        self.players_widgets = {}

        positions = self.client.send_and_collect_data()

        for player in positions:
            self.players_widgets[player] = (Player(player, 0, (0, 0)))

        for player_widget in self.players_widgets:
            self.add_widget(self.players_widgets[player_widget])

        Clock.schedule_interval(self.transfer_data, 1)

    def transfer_data(self, dt):

        data = self.client.send_and_collect_data()

        if not data:
            print("LOST CONNECTION")
        else:
            for username in data:
                position = data[username]
                if position is None:
                    position = "0.0"
                self.players_widgets[username].update(read_position(position))


class Player(Widget):
    def __init__(self, username, color, position, **kwargs):
        super(Player, self).__init__(**kwargs)

        self.username = username
        self.position = position
        self.color = colors[color]

        with self.canvas:
            Color(self.color[0], self.color[1], self.color[2])
            self.rect = Ellipse(group='a', pos=self.position, size=(50, 50))
            print(self.username, self.color)

    def update(self, position):
        self.position = position
        self.rect.pos = self.position


class GameLoopScreen(Screen):
    def __init__(self, host, **kwargs):
        super().__init__(**kwargs)

        self.name = "gameloop"
        self.add_widget(GameLoopHost(host))


class GameLoopClientScreen(Screen):
    def __init__(self, client, **kwargs):
        super().__init__(**kwargs)
        self.name = "gameloopclient"
        self.add_widget(GameLoopClient(client))

