from pandas import DataFrame
from constants import COLOR_DICT, NUM_OF_PLAYERS_IN_LINE_UP
from player_class import Player


class Team:

    def __init__(self, team_id, name, color, list_of_player_indexes: list):
        self.team_id = team_id
        self.name = name
        self.color = COLOR_DICT[color]
        self.id_list = list_of_player_indexes
        self.players_list = tuple([Player(i) for i in self.id_list])
        self.roster = tuple([Player(i) for i in self.id_list])
        self.line_up = tuple(self.roster[i] for i in range(NUM_OF_PLAYERS_IN_LINE_UP))
        self.is_left = False

    def reset_all_positions(self, during_a_set: bool):
        for player in self.players_list:
            player.reset_position(self.is_left, during_a_set)

    def get_positions(self):
        positions = []
        for player in self.players_list:
            positions.append(tuple([player.row, player.column]))
            if player.column not in range(22):
                raise ValueError(f"{player.format_name()} is in an invalid position. "
                                 f"row: {player.row}, col: {player.column}")
        return positions

    def advance_all(self, table: DataFrame):
        for player in self.players_list:
            player.advance(self.is_left, table)

    def update_players(self):
        self.players_list = tuple([Player(i) for i in self.id_list])

    def update_line_up(self):
        self.line_up = tuple(self.roster[i] for i in range(NUM_OF_PLAYERS_IN_LINE_UP))

    def switch_places(self, first_player: Player, second_player: Player):
        first_index = self.id_list.index(first_player.id)
        second_index = self.id_list.index(second_player.id)
        self.id_list[first_index], self.id_list[second_index] = self.id_list[second_index], self.id_list[first_index]
        self.update_line_up()
