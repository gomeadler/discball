from random import choices
from math import dist
from pandas import DataFrame
from data import NUM_OF_PLAYERS_IN_TEAM, create_empty_stats_dict, get_color, find_team_by_name, increase_stat_by
from player_class import Player


def reset_all_positions(team: list, team_is_left: bool):
    for player in team:
        player.reset_position(team_is_left, False)


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
