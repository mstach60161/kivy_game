from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from project.client import Client
from project.gameloop import GameLoopClientScreen

client = None


class Menu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.name = "menu"

        self.client = client

        self.front = GridLayout()
        self.front.cols = 1

        self.namegrid = GridLayout()
        self.namegrid.cols = 2

        self.namegrid.add_widget(Label(text="Username:"))
        self.username = TextInput(multiline=False)
        self.namegrid.add_widget(self.username)

        self.front.add_widget(self.namegrid)

        self.submit = Button(text="Submit")
        self.submit.bind(on_press=self.check_data)
        self.front.add_widget(self.submit)

        self.add_widget(self.front)

    def check_data(self, instance):
        if self.username.text != "":
            self.client.username = self.username.text
            client_app.team.show_teams()
            client_app.screen_manager.current = 'teams'
            return

        self.username.text = ""


class Teams(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.name = 'teams'

        self.client = client

        self.teams = None

        self.front = GridLayout()
        self.front.cols = 1

    def show_teams(self):
        self.client.join_game()

        if not self.client.games:
            self.front.add_widget(Label(text="There is no game available"))
        else:
            i = 0

            for game in self.client.games:
                self.front.add_widget((Label(text="Number: {0}  Game ID: {1}  host: {2}  number of teams: {3}".format(i, game[0], game[1], game[2]))))
                i += 1

            self.grid = GridLayout()
            self.grid.cols = 2

            self.grid.add_widget(Label(text="Select game number:"))
            self.game = TextInput(multiline=False)
            self.grid.add_widget(self.game)

            self.grid.add_widget(Label(text="Select team number:"))
            self.team = TextInput(multiline=False)
            self.grid.add_widget(self.team)

            self.front.add_widget(self.grid)

            self.submit = Button(text="Submit")
            self.submit.bind(on_press=self.check_data)
            self.front.add_widget(self.submit)

            self.add_widget(self.front)

    def check_data(self, instance):
        if self.team.text.isnumeric() and self.game.text.isnumeric():
            if int(self.game.text) < len(self.client.games) and 0 < int(self.team.text) <= int(self.client.games[int(self.game.text)][2]):
                self.client.send_team(self.game.text, self.team.text)

                client_app.wait = Wait()
                client_app.screen_manager.add_widget(client_app.wait)
                client_app.screen_manager.current = 'wait'

                return

        self.game.text = ""
        self.team.text = ""


class Wait(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.name = 'wait'

        self.used = False

        self.client = client

        self.front = GridLayout()
        self.front.cols = 1

        self.label = Label(text="Wait for host to start the game")
        self.front.add_widget(self.label)
        self.button = Button(text="Get ready")
        self.button.bind(on_press=self.run_wait)
        self.front.add_widget(self.button)

        self.add_widget(self.front)

    def run_wait(self, instance):
        if not self.used:
            self.used = True
            self.client.main()
            self.start_game()

    def start_game(self):
        client_app.gameloop = GameLoopClientScreen(client)
        client_app.screen_manager.add_widget(client_app.gameloop)
        client_app.screen_manager.current = 'gameloopclient'


class ClientApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        self.menu = Menu()
        self.team = Teams()
        self.wait = None
        self.gameloop = None

        self.screen_manager.add_widget(self.menu)
        self.screen_manager.add_widget(self.team)

        return self.screen_manager


if __name__ == "__main__":
    client = Client()
    client_app = ClientApp()
    client_app.run()