from general import creating_competition, prepare_match
from summarizing import print_top_performers
from turn import turn
from pandas import DataFrame
from data import update_league_table, POINTS_FOR_WIN
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

    game_table, state_dict = prepare_match(left_team, right_team)
    silent = not(declare["gameplay"])

    while state_dict["left score"] < POINTS_FOR_WIN and state_dict["right score"] < POINTS_FOR_WIN:
        state_dict["set"] += 1
        for team in [left_team, right_team]:
            team.reset_all_positions(False)
        phase(state_dict, left_team, right_team, game_table, silent)

    print(f"{left_team.name if state_dict['left score'] == POINTS_FOR_WIN else right_team.name} won! \n"
          f"the final score was {state_dict['left score']} : {state_dict['right score']}")

    update_league_table(left_team.name, right_team.name, state_dict, league_table)
    left_team.is_left = False
    if declare["game_summary"]:
        print_top_performers(game_table)

    return game_table
