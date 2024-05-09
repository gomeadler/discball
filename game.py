from general import creating_competition, prepare_match, reset_all_positions, print_top_performers
from turn import turn
from pandas import DataFrame, concat
from data import update_league_table, update_stats_table_from_match_table, POINTS_FOR_WIN, stats, league


def phase(match_state: dict, left_team_players_list: list, right_team_players_list: list,
          left_table: DataFrame, right_table: DataFrame, silent: bool):
    match_state["phase"] = 0
    while True:
        match_state["phase"] += 1
        current_carrier, current_running_team = creating_competition(left_team_players_list, right_team_players_list,
                                                                     left_table, right_table)
        result = turn(match_state, current_carrier, current_running_team,
                      left_team_players_list, right_team_players_list, left_table, right_table, silent)
        if result == "Touchdown":
            break


def game(left_team_name: str, right_team_name: str, silent: bool):
    left_team_table, left_team_players, right_team_table, right_team_players, state_dict = \
        prepare_match(left_team_name, right_team_name)
    while state_dict["left score"] < POINTS_FOR_WIN and state_dict["right score"] < POINTS_FOR_WIN:
        state_dict["set"] += 1
        for i, team in enumerate([left_team_players, right_team_players]):
            reset_all_positions(team, not i)
        phase(state_dict, left_team_players, right_team_players, left_team_table, right_team_table, silent)

    print(f"{left_team_name if state_dict['left score'] == POINTS_FOR_WIN else right_team_name} won! \n"
          f"the final score was {state_dict['left score']} : {state_dict['right score']}")
    for team_table in [left_team_table, right_team_table]:
        update_stats_table_from_match_table(team_table, stats)
    update_league_table(left_team_name, right_team_name, state_dict, league)
    if not silent:
        print_top_performers(concat([left_team_table, right_team_table]))


game("Team A", "Team E", False)
