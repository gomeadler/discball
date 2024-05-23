from pandas import DataFrame
from constants import COLOR_DICT, COLOR_RESET, NUM_OF_PLAYERS_IN_LINE_UP
from player_class import Player
from data import find_top_players
# from data import create_empty_stats_dict


class Team:
    def __init__(self, team_id, name, color, list_of_player_indexes: list):
        self.team_id = team_id
        self.name = name
        self.color = COLOR_DICT[color]
        self.id_list = list_of_player_indexes
        self.roster = [Player(i) for i in self.id_list]
        self.line_up = [self.roster[i] for i in range(NUM_OF_PLAYERS_IN_LINE_UP)]
        self.default_starting_roster_ids = self.id_list
        self.bench_players = []
        self.is_left = False
        self.substitute_flag = False
        self.update_line_up()

    def format_team_name(self):
        return self.color + self.name + COLOR_RESET

    def display_roster(self):
        print(self.color + self.name + COLOR_RESET)
        for player in self.roster:
            print(player.format_name())

    def present_team(self, stats_table: DataFrame):
        print(self.format_team_name())
        top_players, arranged_stats = find_top_players(stats_table.iloc[self.id_list])
        i = 0
        for player in self.roster:
            if player.id in top_players:
                player.present_player(stats_table, arranged_stats[i])
                i += 1
            else:
                player.present_player(stats_table, [])
        print("\n")

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
        # TODO: is this needed?
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

    def update_roster_and_line_up_to_default(self):
        # TODO: might not be the most efficient
        temp = []
        for searched_id in self.default_starting_roster_ids:
            for i, player in enumerate(self.roster):
                if player.id == searched_id:
                    temp.append(player)
                    self.roster = self.roster[:i] + self.roster[i+1:] + [player]
                    break
        self.roster = temp
        self.update_line_up()

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

    def trade_in_player(self, arriving_player: Player):
        self.id_list.append(arriving_player.id)
        self.roster.append(arriving_player)
        self.update_line_up()

    def trade_out_player(self, departing_player_id: int):
        self.id_list.remove(departing_player_id)
        for player in self.roster:
            if player.id == departing_player_id:
                self.roster.remove(player)
                self.update_line_up()
                return


# t = Team(0, "checking", "red", [0, 1, 2, 3, 4, 5, 8, 36])
# t.display_roster()
# t.trade_in_player(Player(18))
# t.trade_out_player(4)
# t.display_roster()
