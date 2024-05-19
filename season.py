from constants import TEAMS, COLORS, NUM_OF_PLAYERS_IN_TEAM
from game import game
from data import show_league, import_league, create_empty_stats_dict, update_stats_table_from_another
from summarizing import print_top_performers, print_top_team
from pandas import DataFrame
from team_class import Team
# from time import sleep


def create_team_objects_list(list_of_teams: list, list_of_colors: list) -> list:
    list_of_team_objects = []
    for team_index in range(len(list_of_teams)):
        team_name = list_of_teams[team_index]
        team_color = list_of_colors[team_index]
        player_indexes = [(i + (team_index * NUM_OF_PLAYERS_IN_TEAM)) for i in range(NUM_OF_PLAYERS_IN_TEAM)]
        list_of_team_objects.append(Team(team_index, team_name, team_color, player_indexes))
    return list_of_team_objects


def make_schedule(list_of_teams: list) -> list:
    num_of_teams = len(list_of_teams)
    if num_of_teams % 2 != 0:
        num_of_teams += 1
        list_of_teams.append(False)

    schedule = []
    for _ in range(num_of_teams - 1):
        mid = num_of_teams // 2
        first_half = list_of_teams[:mid]
        second_half = list_of_teams[mid:]
        second_half.reverse()

        matches = []
        for i in range(mid):
            if first_half[i] and second_half[i]:
                matches.append([first_half[i], second_half[i]])
        schedule.append(matches)

        list_of_teams.insert(1, list_of_teams.pop())

    away_schedule = []
    for home_round in schedule:
        current = []
        for match in home_round:
            current.append(match[::-1])
        away_schedule.append(current)
    schedule += away_schedule
    return schedule


def match_day(games_list: list, league_table: DataFrame, declare: dict) -> DataFrame:
    round_stats = create_empty_stats_dict()
    for match in games_list:
        game_stats = game(match[0], match[1], league_table, declare)
        round_stats = update_stats_table_from_another(game_stats, round_stats)
    if declare["round_summary"]:
        print_top_performers(round_stats)
    return round_stats


def season(original_list_of_teams: list, original_list_of_colors: list, declare: dict):
    """
    runs a simulation of a full season of disc_ball

    :param original_list_of_teams: a list with all the TEAMS names
    :param original_list_of_colors: a list with the corresponding COLORS
    :param declare: a dict with instructions to what should be presented and what's not
    :return:
    """

    league = import_league()
    season_stats = create_empty_stats_dict()
    teams_list = list(set(create_team_objects_list(original_list_of_teams, original_list_of_colors)))
    game_schedule = make_schedule(teams_list)
    for season_round in range(len(game_schedule)):
        print(f"Round {season_round + 1} \n")
        season_stats = \
            update_stats_table_from_another(match_day(game_schedule[season_round], league, declare), season_stats)
        show_league(league)
    if declare["season_top_team"]:
        print_top_team(league, season_stats)
    if declare["season_summary"]:
        print_top_performers(season_stats)


declare_dict = {
    "gameplay": False,
    "game_summary": False,
    "round_summary": False,
    "season_top_team": True,
    "season_summary": True
}

# A game for checking out stuff:
#  game("Team A", "Team B", create_league(), declare_dict)

# A season for checking out stuff:
season(TEAMS, COLORS, declare_dict)
