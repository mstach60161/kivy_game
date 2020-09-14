from project.network import Network
import time


class Host:
    def __init__(self):
        self.network = Network()
        self.username = None
        self.teams_no = None
        self.players = None
        self.game_dict = None

    def create_game(self):
        self.network.connect()
        self.network.send("host" + '/' + self.username + '/' + self.teams_no)

    def send_and_collect_data(self):

        self.network.send_without_receiving("100.100")
        data = self.network.receive_pickle()

        return data

    def main(self):
        while True:

            start = input("if you want to start choose 0:")

            if not start:
                self.network.send("play")
                break
            else:
                self.players = self.network.send("wait")

            time.sleep(1)

    def send_players(self):
        self.network.send_without_receiving('wait')
        self.players = self.network.receive_pickle()

        return self.players

    def start_game(self):
        self.network.send("play")


if __name__ == "__main__":
    host = Host()
    host.main()
