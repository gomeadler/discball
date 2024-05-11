from random import choices
from math import dist
from data import teams, create_match_team, increase_stat_by, COLOR_RESET, CYAN, PURPLE, WHITE, \
    NUM_OF_PLAYERS_IN_TEAM, find_top_team, create_empty_stats_dict, get_color, import_players
from pandas import DataFrame
from player_class import Player


def create_block(line_color: str, dot_color: str = None) -> str:
    if dot_color is None:
        return f"{line_color}| |{COLOR_RESET}"
    elif dot_color in str(list(range(22))):
        if int(dot_color) > 10:
            dot_color = str(21 - int(dot_color))
        if dot_color == str(10):
            dot_color = "v"
        return f"{line_color}|{dot_color}|{COLOR_RESET}"
    else:
        return f"{line_color}|{dot_color}*{line_color}|{COLOR_RESET}"


def get_positions(team: list) -> list:
    positions = []
    for player in team:
        positions.append(tuple([player.row, player.column]))
        if player.column not in range(22):
            raise ValueError(f"{player.format_name()} is in an invalid position. "
                             f"row: {player.row}, col: {player.column}")
    return positions


def create_field(left_team: list, right_team: list, match_state: dict, carrier_position: tuple):
    # TODO: check if a blue team plays and change dot color of the carrier accordingly

    left_positions = get_positions(left_team)
    right_positions = get_positions(right_team)
    field_str = ""
    header = ""
    for num in range(22):
        # special columns
        if num == 0 or num == 21:
            header += create_block(PURPLE, str(num))
        elif num == 10 or num == 11:
            header += create_block(CYAN, str(num))
        else:
            header += create_block(WHITE, str(num))  # Default color for other columns
    header += "\n"
    field_str += header

    for row in range(10):
        row_str = ""
        for col in range(22):
            dot = None
            if (row, col) == carrier_position:
                dot = CYAN
            elif (row, col) in left_positions:
                dot = match_state["left color"]
            elif (row, col) in right_positions:
                dot = match_state["right color"]

            # special columns
            if col == 0 or col == 21:
                row_str += create_block(PURPLE, dot)
            elif col == 10 or col == 11:
                row_str += create_block(CYAN, dot)
            else:
                row_str += create_block(WHITE, dot)  # Default color for other columns
        row_str += "\n"
        field_str += row_str
    print(field_str)


def choose_player_by_probabilities(options: list, probabilities: list) -> Player:
    try:
        result = choices(options, weights=probabilities)[0]
    except IndexError:
        print(f"options were {options}, probs were {probabilities}")
        raise IndexError
    return result


def calculate_distance(player1: Player, player2: Player) -> float:
    result = dist((player1.row, player1.column), (player2.row, player2.column))
    if result == 0:
        print(f"tried to calculate the distance between {player1.format_name()} and {player2.format_name()}. "
              f"rows were {player1.row, player2.row}, columns were {player1.column, player2.column}")
        raise ZeroDivisionError
    else:
        return result


def creating_competition(team1: list, team2: list, game_table: DataFrame):
    eligible_players = [player for player in team1 + team2 if player.column not in [0, 21]]
    creating_attributes = [player.attributes["creating"] for player in eligible_players]
    carrier = choose_player_by_probabilities(eligible_players, creating_attributes)
    carrier.has_disc = True
    increase_stat_by(game_table, carrier.id, "creations", 1)
    if carrier in team1:
        return carrier, team1
    else:
        return carrier, team2


def reset_all_positions(team: list, team_is_left: bool):
    for player in team:
        player.reset_position(team_is_left, False)


def prepare_match(left_team_name, right_team_name):
    # TODO: maybe remove left team and right team

    players = import_players()
    left_team = create_match_team(left_team_name, players)
    right_team = create_match_team(right_team_name, players)

    #
    game_stats_table = create_empty_stats_dict()
    combined_list = []
    for team in (left_team, right_team):
        id_list = list(team["ID"])
        combined_list.append([Player(id_list[i]) for i in range(NUM_OF_PLAYERS_IN_TEAM)])
    for i, team in enumerate(combined_list):
        reset_all_positions(team, not i)

    match_state_dict = {
        "left team": left_team_name,
        "right team": right_team_name,
        "left score": 0,
        "right score": 0,
        "set": 0,
        "phase": 0,
        "turn": 0,
        "left color": get_color(left_team_name),
        "right color": get_color(right_team_name)
    }
    print(f"{left_team_name} Vs {right_team_name}")
    return game_stats_table, combined_list[0], combined_list[1], match_state_dict


def find_top_players(stats_table: DataFrame):
    keys_list = list(stats_table.keys())
    first_index = keys_list.index("distance_covered")
    top_players_list = []
    arranged_stats = []
    for stat in keys_list[first_index:]:
        sorted_table = stats_table.sort_values(by=[stat], ascending=False)
        top_index = int(sorted_table["ID"].iloc[0])
        if top_index in top_players_list:
            arranged_stats[top_players_list.index(top_index)].append(stat)
        else:
            top_players_list.append(top_index)
            arranged_stats.append([stat])

    return top_players_list, arranged_stats


def print_top_performers(stats_table: DataFrame):
    print("the top performers at each stat were:")
    top_players, arranged_stats = find_top_players(stats_table)
    for i, player_index in enumerate(top_players):
        top = Player(player_index)
        top.present_player(stats_table, arranged_stats[i])


def print_top_team(league_table: DataFrame, stats_table: DataFrame):
    top_team = find_top_team(league_table)
    print(f"{teams[top_team][0]} have won the league!\n"
          f"Congrats to their excellent players:")
    first_player_index = top_team * NUM_OF_PLAYERS_IN_TEAM

    top_players, arranged_stats = \
        find_top_players(stats_table.loc[first_player_index: first_player_index + NUM_OF_PLAYERS_IN_TEAM - 1])

    for player_id in range(first_player_index, first_player_index + NUM_OF_PLAYERS_IN_TEAM):
        if player_id in top_players:
            i = top_players.index(player_id)
            player = Player(player_id)
            player.present_player(stats_table, arranged_stats[i])
        else:
            player = Player(player_id)
            player.present_player(stats_table, [])
    print("\n")
