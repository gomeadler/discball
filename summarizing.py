from pandas import DataFrame
from constants import NUM_OF_PLAYERS_IN_TEAM
from player_class import Player
from team_class import Team
from typing import List


def find_top_team_id(table: DataFrame) -> int:
    sorted_ids = table.sort_values(by=["points"], ascending=False).loc[:, "ID"].to_list()
    return sorted_ids[0]


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


def print_top_team(team_objects: List[Team], league_table: DataFrame, stats_table: DataFrame):
    top_team = team_objects[find_top_team_id(league_table)]
    print(f"{top_team.format_team_name()} have won the league!\n"
          f"Congrats to their excellent players:")
    top_team.present_team(stats_table)
    print("\n")
