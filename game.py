from general import creating_competition, prepare_match, reset_all_positions
from summarizing import print_top_performers
from turn import turn
from pandas import DataFrame
from data import update_league_table, POINTS_FOR_WIN


def phase(match_state: dict, left_team_players_list: list, right_team_players_list: list,
          game_table: DataFrame, silent: bool):
    match_state["phase"] = 0
    while True:
        match_state["phase"] += 1
        current_carrier, current_running_team = creating_competition(left_team_players_list, right_team_players_list,
                                                                     game_table)
        result = turn(match_state, current_carrier, current_running_team,
                      left_team_players_list, right_team_players_list, game_table, silent)
        if result == "Touchdown":
            break


def game(left_team_name: str, right_team_name: str, league_table: DataFrame, declare: dict) -> DataFrame:

    game_table, left_team_players, right_team_players, state_dict = prepare_match(left_team_name, right_team_name)

    silent = not(declare["gameplay"])

    while state_dict["left score"] < POINTS_FOR_WIN and state_dict["right score"] < POINTS_FOR_WIN:
        state_dict["set"] += 1
        for i, team in enumerate([left_team_players, right_team_players]):
            reset_all_positions(team, not i)
        phase(state_dict, left_team_players, right_team_players, game_table, silent)

    print(f"{left_team_name if state_dict['left score'] == POINTS_FOR_WIN else right_team_name} won! \n"
          f"the final score was {state_dict['left score']} : {state_dict['right score']}")

    update_league_table(left_team_name, right_team_name, state_dict, league_table)
    if declare["game_summary"]:
        print_top_performers(game_table)

    return game_table
