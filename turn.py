from data import COLOR_RESET, increase_stat_by
from player_class import Player
from general import create_field
from pandas import DataFrame
from random import randint
from face_off import face_off
from os import system
from time import sleep


def declare_state(list_of_left_team_players, list_of_right_team_players, match_state: dict, carrier: Player):
    system("cls")
    len_left = len(match_state['left team']) // 2
    len_right = len(match_state['right team']) // 2
    print(f""
          f"{match_state['left team']} Vs. {match_state['right team']} \n"
          f"{' '*len_left}"
          f"{''.join([match_state['left color'], str(match_state['left score']), COLOR_RESET])}"
          f"{' '* len_left} : {' '*len_right}"
          f"{''.join([match_state['right color'], str(match_state['right score']), COLOR_RESET])}"
          f"{' '*len_right} \n"
          f"set : {match_state['set']}, phase: {match_state['phase']}, turn: {match_state['turn']}")
    print(f"{carrier.format_name()} currently holds the disc")
    create_field(list_of_left_team_players, list_of_right_team_players, match_state, (carrier.row, carrier.column))
    sleep(0.5)


def advance(player: Player) -> int:
    """randomizes the number of blocks a certain player would advance.
    """
    if player.delay:
        player.delay = False
        return 0
    run_attempt = randint(1, player.attributes["speed"])
    if run_attempt > 66:
        advance_blocks = 3
    elif run_attempt > 33:
        advance_blocks = 2
    else:
        advance_blocks = 1
    return advance_blocks


def advance_all(left_team_players_list: list, right_team_players_list: list,
                left_table: DataFrame, right_table: DataFrame):
    threshold = 10
    table = left_table
    for player in left_team_players_list:
        if player.column == threshold:
            increase_stat_by(table, player.attributes["Shirt number"] - 1, "turns_in_touchdown_strip", 1)
            continue
        blocks = advance(player)
        if player.column + blocks > threshold:
            blocks = abs(player.column - threshold)
        player.column += blocks
        increase_stat_by(table, player.attributes["Shirt number"] - 1, "distance_covered", blocks)
        if player.has_disc:
            increase_stat_by(table, player.attributes["Shirt number"] - 1, "distance_carried", blocks)
    threshold = 11
    table = right_table
    for player in right_team_players_list:
        if player.column == threshold:
            increase_stat_by(table, player.attributes["Shirt number"] - 1, "turns_in_touchdown_strip", 1)
            continue
        blocks = advance(player)
        if player.column - blocks < threshold:
            blocks = abs(player.column - threshold)
        player.column -= blocks
        increase_stat_by(table, player.attributes["Shirt number"] - 1, "distance_covered", blocks)
        if player.has_disc:
            increase_stat_by(table, player.attributes["Shirt number"] - 1, "distance_carried", blocks)


def check_touchdown(carrier: Player, match_state: dict, left_team_players_list: list,
                    left_table: DataFrame, right_table: DataFrame) -> bool:
    # determine variables
    if carrier in left_team_players_list:
        table = left_table
        threshold = 10
        score = "left score"
    else:
        table = right_table
        threshold = 11
        score = "right score"

    # check if there was a touchdown
    if carrier.column == threshold:
        match_state[score] += 1
        increase_stat_by(table, carrier.attributes["Shirt number"] - 1, "touchdowns", 1)
        return True
    else:
        return False


def turn(match_state: dict, carrier: Player, running_team: list, left_team_players_list: list,
         right_team_players_list: list, left_table: DataFrame, right_table: DataFrame, silent: bool) -> str:
    match_state["turn"] = 0
    shooting_team = left_team_players_list if running_team == right_team_players_list else right_team_players_list

    while True:
        # a loop that runs until a touchdown is scored, the carrier drops the disc or there were more than 10 turns
        match_state["turn"] += 1

        if not silent:
            declare_state(left_team_players_list, right_team_players_list, match_state, carrier)

        advance_all(left_team_players_list, right_team_players_list, left_table, right_table)

        if not silent:
            declare_state(left_team_players_list, right_team_players_list, match_state, carrier)

        there_was_a_drop_at_some_point = False
        taker = None
        for player in shooting_team:
            there_was_a_drop = face_off(player, running_team, left_team_players_list, left_table, right_table, silent)
            if there_was_a_drop:
                there_was_a_drop_at_some_point = True
                taker = player.format_name()

        if there_was_a_drop_at_some_point:
            if not silent:
                declare_state(left_team_players_list, right_team_players_list, match_state, carrier)
                print(f"{taker} has manage to take {carrier.format_name()} down!")
                sleep(3)
            return "Drop"

        if check_touchdown(carrier, match_state, left_team_players_list, left_table, right_table):
            if not silent:
                declare_state(left_team_players_list, right_team_players_list, match_state, carrier)
                print(f"{carrier.format_name()} scored a touchdown!")
                sleep(3)
            return "Touchdown"

        if match_state["turn"] > 9:
            if not silent:
                declare_state(left_team_players_list, right_team_players_list, match_state, carrier)
                print(f"Time! the disc is now free!")
                sleep(3)
            return "Time"