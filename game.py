import random

from general import creating_competition, prepare_match, conclude_match
from summarizing import print_top_performers
from turn import turn
from pandas import DataFrame
from constants import POINTS_FOR_WIN
from team_class import Team


def phase(match_state: dict, left_team: Team, right_team: Team,
          game_table: DataFrame, silent: bool):
    match_state["phase"] = 0
    while True:
        match_state["phase"] += 1
        current_carrier, current_running_team = creating_competition(left_team, right_team, game_table)
        result = turn(match_state, current_carrier, current_running_team, left_team, right_team, game_table, silent)
        if result == "Touchdown":
            break


def game(left_team: Team, right_team: Team, league_table: DataFrame, declare: dict) -> DataFrame:
    # TODO: check if there was already a substitute and then decide if to do the substitution or not

    # preparing the match
    game_table, state_dict = prepare_match(left_team, right_team)
    silent = not(declare["gameplay"])

    # match loop
    while state_dict["left score"] < POINTS_FOR_WIN and state_dict["right score"] < POINTS_FOR_WIN:
        # preparing set
        state_dict["set"] += 1
        for team in [left_team, right_team]:
            team.reset_all_positions(False)

        # set loop
        phase(state_dict, left_team, right_team, game_table, silent)

        # substitutions
        if state_dict["left score"] != 0 and state_dict["left score"] % 3 == 0:
            outgoing_player = left_team.line_up[random.randint(0, 4)]
            incoming_player = left_team.bench_players[(state_dict["left score"] // 3) - 1]
            left_team.substitute(outgoing_player, incoming_player)
            if not silent:
                print(f"{outgoing_player.format_name()} was replaced by {incoming_player.format_name()}")
        if state_dict["right score"] != 0 and state_dict["right score"] % 3 == 0:
            outgoing_player = right_team.line_up[random.randint(0, 4)]
            incoming_player = right_team.bench_players[(state_dict["left score"] // 3) - 1]
            right_team.substitute(outgoing_player, incoming_player)
            if not silent:
                print(f"{outgoing_player.format_name()} was replaced by {incoming_player.format_name()}")

    # match conclusion
    conclude_match(left_team, right_team, state_dict, league_table)
    if declare["game_summary"]:
        print_top_performers(game_table)

    return game_table
