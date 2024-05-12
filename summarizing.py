from pandas import DataFrame
from data import teams, NUM_OF_PLAYERS_IN_TEAM, find_top_team
from player_class import Player


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
