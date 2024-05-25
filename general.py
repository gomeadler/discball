from random import choices
from math import dist
from pandas import DataFrame
from data import create_empty_stats_dict, increase_stat_by, update_league_table, update_averages
from constants import COLOR_DICT
from player_class import Player
from team_class import Team
from constants import POINTS_FOR_WIN


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
        [player for player in left_team.line_up + right_team.line_up if player.column not in [0, 21]]
    creating_attributes = [player.creating for player in eligible_players]
    carrier = choose_player_by_probabilities(eligible_players, creating_attributes)
    carrier.has_disc = True
    increase_stat_by(game_table, carrier.id, "creations", 1)
    if carrier in left_team.line_up:
        return carrier, left_team
    else:
        return carrier, right_team


def assess_performance(player: Player, stats_table: DataFrame):
    player_stats = stats_table.loc[player.id]

    if player_stats["sets_played"]:
        # offence score
        offence_score = 0.0
        offence_score += 10 * player_stats["touchdowns"]
        offence_score += player_stats["creations"] - player_stats["touchdowns"] - player_stats["drops_made"]
        offence_score += player_stats["distance_carried"] / 4
        offence_score += player_stats["carrier_evasions"] / 2
        offence_score -= player_stats["drops_made"] / 2
        if offence_score < 0:
            offence_score = 0.0
        offence_score /= player_stats["sets_played"]

        # defence score
        defence_score = 0.0
        defence_score += 10 * player_stats["last_ditch_takedowns"]
        defence_score += 7 * (player_stats["carrier_takedowns"] - player_stats["last_ditch_takedowns"])
        defence_score += 3 * (player_stats["successful_takedowns"] - player_stats["carrier_takedowns"])
        defence_score += player_stats["last_ditch_hits"] - player_stats["last_ditch_takedowns"]
        defence_score += (player_stats["successful_shots"]
                          - player_stats["successful_takedowns"]
                          - player_stats["last_ditch_hits"]) / 2
        defence_score /= player_stats["sets_played"]
        defence_score *= 1.5

        # total score
        total_score = (offence_score + defence_score + max(offence_score, defence_score))
        if total_score < 5:
            total_score = float(int(total_score))
        elif total_score <= 7.5:
            total_score = int(total_score * 2) / 2
        elif total_score <= 12:
            temp = int((total_score % 7.5) + 1) / 5
            total_score = 7.5 + temp
        else:
            temp = int((total_score % 12) + 1) / 10
            total_score = 8.5 + temp
            if total_score >= 10:
                total_score = 10.0
        # print(offence_score, defence_score, total_score)

        return offence_score, defence_score, total_score

    else:
        return -1, -1, -1


def prepare_match(left_team: Team, right_team: Team):
    game_stats_table = create_empty_stats_dict()
    left_team.is_left = True
    for team in [left_team, right_team]:
        team.reset_all_positions(False)
        team.substitute_flag = True

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


def conclude_match(left_team: Team, right_team: Team, state_dict: dict, league_table: DataFrame, game_table: DataFrame):
    left_team.is_left = False
    for team in [left_team, right_team]:
        team.can_substitute = False
        team.update_roster_and_line_up_to_default()
        for player in team.roster:
            if game_table.loc[player.id, "sets_played"]:
                offence_score, defence_score, rating = assess_performance(player, game_table)
                if offence_score > 0:
                    game_table.loc[player.id, "offence_scores_list"].append(offence_score)
                if defence_score > 0:
                    game_table.loc[player.id, "defence_scores_list"].append(defence_score)
                game_table.loc[player.id, "rating_list"].append(rating)
                update_averages(player.id, game_table, False)

    print(f"{left_team.name if state_dict['left score'] == POINTS_FOR_WIN else right_team.name} won! \n"
          f"the final score was {state_dict['left score']} : {state_dict['right score']}")

    update_league_table(left_team.name, right_team.name, state_dict, league_table)
