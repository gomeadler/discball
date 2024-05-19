from constants import COLOR_RESET, COLOR_DICT
from data import import_players, increase_stat_by
from pandas import DataFrame
from random import randint


class Player:
    """A class representing a player during a game."""

    def __init__(self, player_id: int):
        # TODO: maybe make every attribute its own attribute instead of using the dataframe
        """Initializing a player instance.

        :param player_id: an integer representing the player's ID in the players Dataframe.
        """
        players = import_players()
        self.attributes = players.loc[player_id]
        self.id = player_id
        self.color = COLOR_DICT[players.loc[player_id, "Color"]]
        self.has_disc = False
        self.row = None
        self.column = None
        self.delay = False
        self.fatigue = 0
        self.on_field = False

    def reset_position(self, is_left: bool, during_a_set: bool = False):
        """
        Returning the player to his starting position in the beginning of a set,
        Or brings him to the Graveyard in case he fell.

        :param is_left: if the player is in the left team
        :param during_a_set: reset_position happens during a set only if the player fell.
               thus it brings him to the Graveyard, and delays him.
        :return: None
        """
        self.has_disc = False
        self.delay = False
        self.row = (self.id % 5) * 2
        if is_left:
            self.column = 1

            if during_a_set:
                self.column -= 1
                self.delay = True
        else:
            self.column = 20
            self.row += 1

            if during_a_set:
                self.column += 1
                self.delay = True

    def determine_blocks(self):
        """randomizes the number of blocks a certain player would advance.
        """
        # TODO: special qualities such as sprinter and slow starter

        if self.delay:
            self.delay = False
            return 0
        run_attempt = randint(1, self.attributes["speed"])
        if run_attempt > 66:
            advance_blocks = 3
        elif run_attempt > 33:
            advance_blocks = 2
        else:
            advance_blocks = 1
        return advance_blocks

    def advance(self, team_is_left: bool, table: DataFrame):
        threshold = 10 if team_is_left else 11
        direction = 1 if team_is_left else -1

        if self.column == threshold:
            increase_stat_by(table, self.id, "turns_in_touchdown_strip", 1)
        else:
            self.fatigue += 1
            distance = abs(self.column - threshold)
            blocks = self.determine_blocks()
            if distance < blocks:
                blocks = distance
            increase_stat_by(table, self.id, "distance_covered", blocks)
            self.column += blocks * direction
            if self.has_disc:
                increase_stat_by(table, self.id, "distance_carried", blocks)

    def format_name(self) -> str:
        """
        formats a player's name to match its Team's color.

        :return: string of ANSI escape code (of the Team's color), player's name and ANSI escape code (of a color reset)
        """
        return "".join([self.color, self.attributes["Name"], COLOR_RESET])

    def present_player(self, stats_table: DataFrame, top_stat_list: list):
        keys_list = list(stats_table.keys())
        first_index = keys_list.index("distance_covered")
        print(self.format_name())
        for player_stat in keys_list[first_index:]:
            if player_stat in top_stat_list:
                print(COLOR_DICT["purple"], end="")
            print("   ", player_stat, stats_table.loc[self.id, player_stat])
            print(COLOR_RESET, end="")
