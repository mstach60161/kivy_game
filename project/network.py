import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.1.81"
        self.port = 5555
        self.addr = (self.server, self.port)

    def connect(self):
        try:
            self.client.connect(self.addr)
        except socket.error as error:
            print(error, '/n', "connect nie działa")

        return self.client.recv(2048).decode()

    def send(self, data):
        try:
            self.client.send(str.encode(data))
        except socket.error as error:
            print(error, '/n', "send nie działa")

        return self.client.recv(2048).decode()

    def close(self):
        self.client.close()

    def receive(self):
        return self.client.recv(2048).decode()

    def receive_pickle(self):
        return pickle.loads(self.client.recv(2048))  # czy tak jest dobrze

    def send_without_receiving(self, data):
        try:
            self.client.send(str.encode(data))
        except socket.error as error:
            print(error, '/n', "receive nie działa")


n = Network()
