class Game:
    def __init__(self, game_id, host_name, teams_number):
        self.game_id = game_id
        self.host_name = host_name
        self.teams_number = teams_number
        self.ready = False
        self.positions = {0: None}   # host position

        print('number of teams:', teams_number)

        for i in range(teams_number):
            self.positions[i+1] = {}
        print('dict', self.positions)

    def start_game(self):
        self.ready = True

    def get_id(self):
        return self.game_id

    def get_host_name(self):
        return self.host_name

    def get_teams_number(self):
        return self.teams_number

    def get_positions(self):
        return self.positions

    def get_team_positions(self, team_id):
        return self.positions[team_id]

    def get_players(self):
        players = {}

        if len(self.positions) <= 1:
            return players

        for team in (list(self.positions.keys())[1:]):
            players[team] = []
            for player in list(self.positions[team].keys()):
                players[team].append(player)
        return players

    def get_team_players(self, team_id):
        return self.get_players()[team_id]

    def available(self):
        return not self.ready

    def set_host_position(self, position):
        self.positions[0] = position

    def set_position(self, team_id, player, position=None):
        self.positions[team_id][player] = position

    def add_player(self, team_id, player):
        self.positions[team_id][player] = "0.0"

    def delete_player(self, team_id, player):
        if player in self.positions[team_id]:
            del self.positions[team_id][player]
