from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from project.host import Host
from project.gameloop import GameLoopScreen

host = None


class Menu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.name = "menu"

        self.host = host

        self.front = GridLayout()
        self.front.cols = 1

        self.namegrid = GridLayout()
        self.namegrid.cols = 2

        self.namegrid.add_widget(Label(text="Username:"))
        self.username = TextInput(multiline=False)
        self.namegrid.add_widget(self.username)

        self.teams_no_grid = GridLayout()
        self.teams_no_grid.cols = 2

        self.teams_no_grid.add_widget(Label(text="Teams number:"))
        self.teams_no = TextInput(multiline=False)
        self.teams_no_grid.add_widget(self.teams_no)

        self.front.add_widget(self.namegrid)
        self.front.add_widget(self.teams_no_grid)

        self.submit = Button(text="Submit")
        self.submit.bind(on_press=self.check_data)
        self.front.add_widget(self.submit)

        self.add_widget(self.front)

    def check_data(self, instance):
        if self.teams_no.text.isnumeric():
            if int(self.teams_no.text) > 0 and self.username.text != "":
                self.host.username = self.username.text
                self.host.teams_no = self.teams_no.text

                host_app.screen_manager.current = 'conn'
                self.host.create_game()
                host_app.start.run_start()
                host_app.screen_manager.current = "start"

                return

        self.teams_no.text = ""
        self.username.text = ""


class Connecting(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.name = 'conn'

        self.host = host

        self.front = GridLayout()
        self.front.cols = 1
        self.front.add_widget(Label(text='Connecting...'))

        self.add_widget(self.front)


class Start(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.name = 'start'

        self.numbers = None

        self.host = host
        self.front = GridLayout()
        self.front.cols = 1

        self.grids = []

    def run_start(self):
        for i in range(int(host.teams_no)):
            grid = GridLayout()
            grid.cols = 1
            grid.add_widget(Label(text="Team number {0}".format(i+1)))
            self.grids.append(grid)

            self.front.add_widget(grid)

        self.numbers = [0] * int(host.teams_no)

        self.buttons = GridLayout()
        self.buttons.cols = 2

        self.update = Button(text="Update")
        self.update.bind(on_press=self.update_players)
        self.buttons.add_widget(self.update)

        self.start = Button(text="Start")
        self.start.bind(on_press=self.start_game)
        self.buttons.add_widget(self.start)

        self.front.add_widget(self.buttons)

        self.add_widget(self.front)

    def start_game(self, instance):
        host.start_game()
        host_app.game_loop = GameLoopScreen(host)
        host_app.screen_manager.add_widget(host_app.game_loop)

        host_app.screen_manager.current = "gameloop"

    def update_players(self, instance):
        players = self.host.send_players()

        for no, team in enumerate(players):
            i = 0
            for no2, player in enumerate(players[team]):
                if no2 >= self.numbers[no]:
                    self.grids[team - 1].add_widget(Label(text="{0}.{1}".format(no2, player)))
                    self.numbers[no] += 1



class HostApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        self.menu = Menu()
        self.conn = Connecting()
        self.start = Start()
        self.game_loop = None

        self.screen_manager.add_widget(self.menu)
        self.screen_manager.add_widget(self.conn)
        self.screen_manager.add_widget(self.start)

        return self.screen_manager


if __name__ == "__main__":
    host = Host()
    host_app = HostApp()
    host_app.run()

