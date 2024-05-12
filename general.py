from random import choices
from math import dist
from data import teams, increase_stat_by, NUM_OF_PLAYERS_IN_TEAM, find_top_team, create_empty_stats_dict, \
    get_color, find_team_by_name
from pandas import DataFrame
from player_class import Player

# TODO: split game mechanics and field mechanics
# TODO: maybe also split preparing in summarizing a game


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
    game_stats_table = create_empty_stats_dict()
    combined_list = []
    for team in [left_team_name, right_team_name]:
        first_index = find_team_by_name(team) * 5
        combined_list.append([Player(first_index + i) for i in range(NUM_OF_PLAYERS_IN_TEAM)])
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
