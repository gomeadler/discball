from data import import_players, COLOR_RESET, COLOR_DICT, get_color
from pandas import DataFrame


class Player:
    """A class representing a player during a game."""

    def __init__(self, player_id: int):
        """Initializing a player instance.

        :param player_id: an integer representing the player's ID in the players Dataframe.
        """
        players = import_players()
        self.attributes = players.loc[player_id]
        self.id = player_id
        self.has_disc = False
        self.row = None
        self.column = None
        self.delay = False

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

    def format_name(self) -> str:
        """
        formats a player's name to match its Team's color.

        :return: string of ANSI escape code (of the Team's color), player's name and ANSI escape code (of a color reset)
        """
        color = get_color(self.attributes["Team"])
        return "".join([color, self.attributes["Name"], COLOR_RESET])

    def present_player(self, stats_table: DataFrame, top_stat_list: list):
        keys_list = list(stats_table.keys())
        first_index = keys_list.index("distance_covered")
        print(self.format_name())
        for player_stat in keys_list[first_index:]:
            if player_stat in top_stat_list:
                print(COLOR_DICT["purple"], end="")
            print("   ", player_stat, stats_table.loc[self.id, player_stat])
            print(COLOR_RESET, end="")
