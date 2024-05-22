from pandas import DataFrame
from player_class import Player
from team_class import Team
from typing import List
from data import find_top_players


def find_top_team(league_table: DataFrame, teams_list: List[Team]):
    sorted_ids = league_table.sort_values(by=["points"], ascending=False).loc[:, "ID"].to_list()
    top_team_id = sorted_ids[0]
    for team in teams_list:
        if team.team_id == top_team_id:
            return team
    raise ValueError("couldn't find the top team")


def print_top_performers(stats_table: DataFrame):
    print("the top performers at each stat were:")
    top_players, arranged_stats = find_top_players(stats_table)
    for i, player_index in enumerate(top_players):
        top = Player(player_index)
        top.present_player(stats_table, arranged_stats[i])


def print_top_team(team_objects: List[Team], league_table: DataFrame, stats_table: DataFrame):
    top_team = find_top_team(league_table, team_objects)
    print(f"{top_team.format_team_name()} have won the league!\n"
          f"Congrats to their excellent players:")
    top_team.present_team(stats_table)
