from random import choices
from math import dist
from pandas import DataFrame
from data import create_empty_stats_dict, increase_stat_by
from constants import COLOR_DICT
from player_class import Player
from team_class import Team


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


def determine_carrier_color(left_team: Team, right_team: Team):
    colors = [left_team.color, right_team.color]
    if COLOR_DICT["blue"] not in colors:
        return COLOR_DICT["cyan"]
    elif COLOR_DICT["magenta"] not in colors:
        return COLOR_DICT["purple"]
    else:
        return COLOR_DICT["lime"]


def creating_competition(left_team: Team, right_team: Team, game_table: DataFrame):
    eligible_players = \
        [player for player in left_team.players_list + right_team.players_list if player.column not in [0, 21]]
    creating_attributes = [player.attributes["creating"] for player in eligible_players]
    carrier = choose_player_by_probabilities(eligible_players, creating_attributes)
    carrier.has_disc = True
    increase_stat_by(game_table, carrier.id, "creations", 1)
    if carrier in left_team.players_list:
        return carrier, left_team
    else:
        return carrier, right_team


def prepare_match(left_team: Team, right_team: Team):
    game_stats_table = create_empty_stats_dict()
    left_team.is_left = True
    for team in [left_team, right_team]:
        team.reset_all_positions(False)

    match_state_dict = {
        "left team": left_team.name,
        "right team": right_team.name,
        "left score": 0,
        "right score": 0,
        "set": 0,
        "phase": 0,
        "turn": 0,
        "left color": left_team.color,
        "right color": right_team.color,
        "carrier color": determine_carrier_color(left_team, right_team)
    }
    print(f"{left_team.name} Vs {right_team.name}")
    return game_stats_table, match_state_dict
