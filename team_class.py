from pandas import DataFrame
from data import COLOR_DICT
from player_class import Player


class Team:

    def __init__(self, team_id, name, color, list_of_player_indexes: list):
        self.team_id = team_id
        self.name = name
        self.color = COLOR_DICT[color]
        self.players_list = tuple([Player(i) for i in list_of_player_indexes])
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

    def update_players(self, list_of_player_indexes: list):
        self.players_list = tuple([Player(i) for i in list_of_player_indexes])
