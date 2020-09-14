import socket
from _thread import *
import pickle
import time

from project.game import *

server = "192.168.1.81"
port = 5555

games_id = set()
games = {}


def get_free_id():
    free_id = 0

    while free_id in games_id:
        free_id += 1

    games_id.add(free_id)
    return free_id


def host_thread(conn, game):
    while game.available():
        data = conn.recv(2048).decode("utf-8")
        if not data:
            print("Disconnected")
            break
        else:
            if data == "play":
                game.start_game()
            else:
                players = game.get_players()
                print(players)
                conn.sendall(pickle.dumps(players))

        time.sleep(2)

    data = "start"
    conn.send(str.encode(data))

    while True:
        try:
            data = conn.recv(2048).decode("utf-8")

            if not data:
                print("Disconnected")
                break
            else:
                print("host position: ", data)
                game.set_host_position(data)

                positions = game.get_positions()
                conn.sendall(pickle.dumps(positions))

        except:
            break

    print("Lost connection")
    conn.close()


def player_thread(conn, game, username, team_id):
    print(game.positions)
    game.set_position(team_id, username)

    while game.available():     # DO ROBOTY
        data = "waiting"
        conn.send(str.encode(data))
        time.sleep(1)

    data = "start"
    conn.send(str.encode(data))

    while True:
        try:
            data = conn.recv(2048).decode("utf-8")

            if not data:
                print("Disconnected")
                break
            else:
                print(username, "position: ", data)
                game.set_position(team_id, username, data)

                positions = game.get_team_positions(team_id)
                conn.sendall(pickle.dumps(positions))
        except:
            break

    print("Lost connection")
    conn.close()


def find_game(conn):
    while True:
        message = ""

        for game in games.values():
            if game.available():
                game_info = str(game.get_id()) + '/'
                game_info += game.get_host_name() + '/'
                game_info += str(game.get_teams_number())
                message += game_info + '\n'

        if len(message) == 0:
            message = "busy"
            conn.send(str.encode(message))
            time.sleep(3)
        else:
            conn.send(str.encode(message))
            response = conn.recv(2048).decode()
            game_id, team_id = response.split('/')
            game_id, team_id = int(game_id), int(team_id)
            if games[game_id].available():
                return game_id, team_id


def threaded_client(conn):
    message = "Connected"
    conn.send(str.encode(message))

    data = conn.recv(2048).decode()

    # if host, number = number of teams else 0
    role, username, number = data.split('/')

    if role == "host":
        free_id = get_free_id()
        games[free_id] = Game(free_id, username, int(number))
        message = "Connect"
        conn.send(str.encode(message))
        host_thread(conn, games[free_id])


    elif role == "player":
        game_id, team_id = find_game(conn)
        message = "Connect"
        conn.send(str.encode(message))
        player_thread(conn, games[game_id], username, team_id)


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((server, port))
    except socket.error as e:
        str(e)

    s.listen()  #
    print("Server started")

    while True:
        conn, addr = s.accept()
        print("Connected to:", addr)
        start_new_thread(threaded_client, (conn,))


