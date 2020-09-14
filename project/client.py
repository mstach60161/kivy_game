from project.network import Network
from random import randint


class Client:
    def __init__(self):
        self.network = Network()
        self.username = None
        self.games = []
        self.positions = None
        self.team_id = None
        self.position = (randint(100, 700), randint(100, 500))

    def send_team(self, game, choice):
        game = int(game)
        self.team_id = int(choice)

        self.network.send(self.games[game][0] + '/' + choice)

    def move_client(self):
        x = randint(-10, 10)
        y = randint(-10, 10)
        while not (0 <= self.position[1] + x <= 600 and 0 <= self.position[0] + y <= 800):
            x = randint(-10, 10)
            y = randint(-10, 10)
        self.position = (self.position[0] + x, self.position[1] + y)
        return str(self.position[0]) + '.' + str(self.position[1])


    def join_game(self):
        self.network.connect()

        message = self.network.send('player' + '/' + self.username + '/' + '0')

        while True:
            if message == 'busy':
                message = self.network.receive()
            else:
                break

        message = message.split('\n')

        for game in message:
            self.games.append(game.split('/'))

        self.games = self.games[:-1]

    def send_and_collect_data(self):

        self.network.send_without_receiving(self.move_client())

        data = self.network.receive_pickle()

        if data:
            self.positions = data

        return data

    def main(self):

        while True:
            order = self.network.receive()
            if order == "start":
                break


if __name__ == "__main__":
    client = Client()
    client.main()

