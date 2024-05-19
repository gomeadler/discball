from pandas import DataFrame
from constants import COLOR_DICT, NUM_OF_PLAYERS_IN_LINE_UP
from player_class import Player


class Team:

    def __init__(self, team_id, name, color, list_of_player_indexes: list):
        self.team_id = team_id
        self.name = name
        self.color = COLOR_DICT[color]
        self.id_list = list_of_player_indexes
        self.roster = [Player(i) for i in self.id_list]
        self.line_up = [self.roster[i] for i in range(NUM_OF_PLAYERS_IN_LINE_UP)]
        self.bench_players = []
        self.is_left = False

    def reset_all_positions(self, during_a_set: bool):
        self.update_line_up()
        for i, player in enumerate(self.line_up):
            player.position = i
            player.reset_position(self.is_left, during_a_set)

    def get_positions(self):
        positions = []
        for player in self.line_up:
            positions.append(tuple([player.row, player.column]))
            if player.column not in range(22):
                raise ValueError(f"{player.format_name()} is in an invalid position. "
                                 f"row: {player.row}, col: {player.column}")
        return positions

    def advance_all(self, table: DataFrame):
        for player in self.line_up:
            player.advance(self.is_left, table)

    def update_players(self):
        self.roster = [Player(i) for i in self.id_list]

    def update_line_up(self):
        self.line_up = []
        self.bench_players = []
        for i, player in enumerate(self.roster):
            if i < NUM_OF_PLAYERS_IN_LINE_UP:
                self.line_up.append(player)
                player.on_field = True
            else:
                self.bench_players.append(player)
                player.on_field = False
                player.position = None

    def switch_places(self, first_player: Player, second_player: Player):
        first_index = self.id_list.index(first_player.id)
        second_index = self.id_list.index(second_player.id)
        self.id_list[first_index], self.id_list[second_index] = self.id_list[second_index], self.id_list[first_index]
        self.roster[first_index], self.roster[second_index] = self.roster[second_index], self.roster[first_index]
        self.update_line_up()

    def substitute(self, outgoing_player: Player, incoming_player: Player):
        incoming_player.row = outgoing_player.row
        outgoing_player.row = None
        self.switch_places(outgoing_player, incoming_player)


# t = Team(0, "a", "red", [0, 1, 2, 3, 4, 5, 8, 36])
# for player in t.roster:
#     print(player.format_name(), player.on_field)
# t.switch_places(t.roster[2], t.roster[5])
# t.switch_places(t.roster[1], t.roster[6])
# for player in t.roster:
#     print(player.format_name(), player.on_field)
