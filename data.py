from pandas import DataFrame, read_excel
from numpy import random, clip
from names import get_first_name

NUM_OF_PLAYERS_IN_TEAM = 5
POINTS_FOR_WIN = 10
PATH = r"C:\Users\gomea\PycharmProjects\disc_game_pandas\players_excel.xlsx"


COLOR_RESET = '\033[0m'
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
BRIGHT_BLACK = "\033[90m"
BRIGHT_RED = "\033[91m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_YELLOW = "\033[93m"
BRIGHT_BLUE = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
BRIGHT_CYAN = "\033[96m"
BRIGHT_WHITE = "\033[97m"
ORANGE = "\033[38;5;202m"
PURPLE = "\033[38;5;129m"
PINK = "\033[38;5;213m"
LIME = "\033[38;5;154m"
TEAL = "\033[38;5;37m"
BROWN = "\033[38;5;124m"
GRAY = "\033[38;5;240m"


teams = [("Team A", RED), ("Team B", BLUE), ("Team C", GREEN), ("Team D", YELLOW),
         ("Team E", MAGENTA), ("Team F", ORANGE), ("Team G", GRAY), ("Team H", BROWN)]


def find_team_by_name(team_name: str) -> int:
    for index, team in enumerate(teams):
        if team[0] == team_name:
            return index

    raise ValueError("Team not found")


def get_color(team_name: str) -> str:
    color = WHITE
    for t in teams:
        if t[0] == team_name:
            color = t[1]
            return color
    if color == WHITE:
        raise ValueError("Team not found")


def random_gaussian_number(mean, std_dev, min_value, max_value) -> int:
    return int(clip(round(random.normal(mean, std_dev)), min_value, max_value))


def create_league() -> DataFrame:
    league_dict = {
        "ID": [i for i in range(len(teams))],
        "Color": [i[1] for i in teams],
        "Name": [i[0] for i in teams],
        "touchdowns": [0 for _ in teams],
        "conceded": [0 for _ in teams],
        "ratio": [0 for _ in teams],
        "points": [0 for _ in teams]
    }
    df = DataFrame(league_dict)
    df = df.astype(dtype={"ID": int, "Color": str, 'Name': str, "touchdowns": int,
                          "conceded": int, "ratio": int, "points": int})
    return df


def create_empty_stats_dict() -> DataFrame:
    stats_dict = {
        "ID": [i for i in range(NUM_OF_PLAYERS_IN_TEAM * len(teams))],
        "distance_covered": [0 for _ in range(NUM_OF_PLAYERS_IN_TEAM * len(teams))],
        "distance_carried": [0 for _ in range(NUM_OF_PLAYERS_IN_TEAM * len(teams))],
        "touchdowns": [0 for _ in range(NUM_OF_PLAYERS_IN_TEAM * len(teams))],
        "turns_in_touchdown_strip": [0 for _ in range(NUM_OF_PLAYERS_IN_TEAM * len(teams))],
        "creations": [0 for _ in range(NUM_OF_PLAYERS_IN_TEAM * len(teams))],
        "evasions": [0 for _ in range(NUM_OF_PLAYERS_IN_TEAM * len(teams))],
        "successful_shots": [0 for _ in range(NUM_OF_PLAYERS_IN_TEAM * len(teams))],
        "successful_takedowns": [0 for _ in range(NUM_OF_PLAYERS_IN_TEAM * len(teams))],
        "carrier_takedowns": [0 for _ in range(NUM_OF_PLAYERS_IN_TEAM * len(teams))],
        "hits_taken": [0 for _ in range(NUM_OF_PLAYERS_IN_TEAM * len(teams))],
        "balance_losses": [0 for _ in range(NUM_OF_PLAYERS_IN_TEAM * len(teams))],
        "drops_made": [0 for _ in range(NUM_OF_PLAYERS_IN_TEAM * len(teams))]
    }
    return DataFrame(stats_dict)


def create_match_team(team: str, players_table: DataFrame) -> DataFrame:
    new_table = players_table.query(f"Team == '{team}'")

    stats_dict = {
        "ID": [list(new_table["ID"])[i] for i in range(NUM_OF_PLAYERS_IN_TEAM)],
        "player": [list(new_table["Name"])[i] for i in range(NUM_OF_PLAYERS_IN_TEAM)],
        "distance_covered": [0 for _ in range(NUM_OF_PLAYERS_IN_TEAM)],
        "distance_carried": [0 for _ in range(NUM_OF_PLAYERS_IN_TEAM)],
        "touchdowns": [0 for _ in range(NUM_OF_PLAYERS_IN_TEAM)],
        "turns_in_touchdown_strip": [0 for _ in range(NUM_OF_PLAYERS_IN_TEAM)],
        "creations": [0 for _ in range(NUM_OF_PLAYERS_IN_TEAM)],
        "evasions": [0 for _ in range(NUM_OF_PLAYERS_IN_TEAM)],
        "successful_shots": [0 for _ in range(NUM_OF_PLAYERS_IN_TEAM)],
        "successful_takedowns": [0 for _ in range(NUM_OF_PLAYERS_IN_TEAM)],
        "carrier_takedowns": [0 for _ in range(NUM_OF_PLAYERS_IN_TEAM)],
        "hits_taken": [0 for _ in range(NUM_OF_PLAYERS_IN_TEAM)],
        "balance_losses": [0 for _ in range(NUM_OF_PLAYERS_IN_TEAM)],
        "drops_made": [0 for _ in range(NUM_OF_PLAYERS_IN_TEAM)],
    }
    return DataFrame(stats_dict)


def create_players(path) -> DataFrame:
    player_ability_dict = {
        "ID": [i for i in range(NUM_OF_PLAYERS_IN_TEAM * len(teams))],
        "Name": [get_first_name("Male") for _ in range(NUM_OF_PLAYERS_IN_TEAM * len(teams))],
        "Team": [teams[i][0] for i in range(len(teams)) for _ in range(NUM_OF_PLAYERS_IN_TEAM)],
        "Shirt number": [i + 1 for _ in range(len(teams)) for i in range(NUM_OF_PLAYERS_IN_TEAM)],
        "speed": [random_gaussian_number(60, 10, 0, 100) for _ in range(NUM_OF_PLAYERS_IN_TEAM * len(teams))],
        "agility": [random_gaussian_number(60, 10, 0, 100) for _ in range(NUM_OF_PLAYERS_IN_TEAM * len(teams))],
        "creating": [random_gaussian_number(60, 10, 0, 100) for _ in range(NUM_OF_PLAYERS_IN_TEAM * len(teams))],
        "shooting": [random_gaussian_number(60, 10, 0, 100) for _ in range(NUM_OF_PLAYERS_IN_TEAM * len(teams))],
        "stability": [random_gaussian_number(60, 10, 0, 100) for _ in range(NUM_OF_PLAYERS_IN_TEAM * len(teams))],
    }
    players_df = DataFrame(player_ability_dict)
    players_df.to_excel(path, index=False)
    return players_df


def import_players():
    return read_excel(PATH)


def clear_table(table_name: DataFrame):
    table_name.loc[:, :] = 0


def initiate_league_and_players():
    return create_league(), create_players(PATH), create_empty_stats_dict()


def increase_stat_by(table: DataFrame, player: int, stat: str, amount: int):
    """gets the key to a player, a stat to increase and the amount to increase it by"""
    table.loc[player, stat] += amount


def update_stats_table_from_another(source_table: DataFrame, receiving_table: DataFrame):
    source_table["ID"] = 0
    return receiving_table + source_table


def update_ratio(team_name: str, table: DataFrame):
    ratio = \
        (table.loc[table["Name"] == team_name, "touchdowns"] * 100 // table.loc[table["Name"] == team_name, "conceded"])
    table.loc[table["Name"] == team_name, "ratio"] = ratio


def update_league_table(left_team_name: str, right_team_name: str, match_summary: dict, table: DataFrame):
    left_won = True if match_summary["left score"] > match_summary["right score"] else False
    left_summary = {
        "touchdowns": match_summary["left score"],
        "conceded": match_summary["right score"],
        "points": match_summary["left score"]
    }
    right_summary = {
        "touchdowns": match_summary["right score"],
        "conceded": match_summary["left score"],
        "points": match_summary["right score"]
    }

    if left_won:
        left_summary["points"] += match_summary["left score"] - match_summary["right score"]
    else:
        right_summary["points"] += match_summary["right score"] - match_summary["left score"]

    for key, value in left_summary.items():
        table.loc[table["Name"] == left_team_name, key] += value
    for key, value in right_summary.items():
        table.loc[table["Name"] == right_team_name, key] += value
    for team in [left_team_name, right_team_name]:
        update_ratio(team, table)


def show_league(table: DataFrame):
    sorted_table = table.sort_values(by=["points"], ascending=False).loc[:, "Name":]
    sorted_ids = table.sort_values(by=["points"], ascending=False).loc[:, "ID"].to_list()
    sorted_table = sorted_table.to_string(index=False).split("\n")
    print_head = True
    for row in range(len(teams) + 1):
        if print_head:
            print(COLOR_RESET, " ", sorted_table[row])
            print_head = False
        else:
            print("".join([str(row) + "  ", teams[sorted_ids[row - 1]][1], sorted_table[row], COLOR_RESET]))

    print("\n")


def find_top_team(table: DataFrame) -> int:
    sorted_ids = table.sort_values(by=["points"], ascending=False).loc[:, "ID"].to_list()
    return sorted_ids[0]
