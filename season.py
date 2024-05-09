from game import game
from data import show_league, teams, league, stats
from general import print_top_performers, print_top_team


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


def match_day(games_list: list, silent: bool = True):
    for match in games_list:
        game(match[0], match[1], silent)


def season(list_of_teams: list, print_summary: bool = False, silent: bool = True):
    game_schedule = make_schedule(list(set([team[0] for team in list_of_teams])))
    for season_round in range(len(game_schedule)):
        print(f"Round {season_round + 1} \n")
        match_day(game_schedule[season_round], silent)
        show_league(league)
    if print_summary:
        print_top_team(league, stats)
        print_top_performers(stats)


season(teams, True, False)
