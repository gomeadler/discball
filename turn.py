from data import COLOR_RESET, increase_stat_by
from player_class import Player
from team_class import Team
from field_mechanics import create_field
from pandas import DataFrame
from face_off import face_off
from os import system
from time import sleep


def declare_state(left_team: Team, right_team: Team, match_state: dict, carrier: Player):
    system("cls")
    len_left = len(left_team.name) // 2
    len_right = len(right_team.name) // 2
    print(f""
          f"{left_team.name} Vs. {right_team.name} \n"
          f"{' '*len_left}"
          f"{''.join([left_team.color, str(match_state['left score']), COLOR_RESET])}"
          f"{' '* len_left} : {' '*len_right}"
          f"{''.join([right_team.color, str(match_state['right score']), COLOR_RESET])}"
          f"{' '*len_right} \n"
          f"set : {match_state['set']}, phase: {match_state['phase']}, turn: {match_state['turn']}")
    print(f"{carrier.format_name()} currently holds the disc")
    create_field(left_team, right_team, match_state, (carrier.row, carrier.column))
    sleep(0.5)


def check_touchdown(carrier: Player, match_state: dict, left_team: Team,
                    game_table: DataFrame) -> bool:
    # determine variables
    if carrier in left_team.players_list:
        threshold = 10
        score = "left score"
    else:
        threshold = 11
        score = "right score"

    # check if there was a touchdown
    if carrier.column == threshold:
        match_state[score] += 1
        increase_stat_by(game_table, carrier.id, "touchdowns", 1)
        return True
    else:
        return False


def turn(match_state: dict, carrier: Player, running_team: Team, left_team: Team,
         right_team: Team, game_table: DataFrame, silent: bool) -> str:
    match_state["turn"] = 0
    shooting_team = left_team if running_team == right_team else right_team

    while True:
        # a loop that runs until a touchdown is scored, the carrier drops the disc or there were more than 10 turns
        match_state["turn"] += 1

        if not silent:
            declare_state(left_team, right_team, match_state, carrier)

        for team in [left_team, right_team]:
            team.advance_all(game_table)

        if not silent:
            declare_state(left_team, right_team, match_state, carrier)

        there_was_a_drop_at_some_point = False
        taker = None
        for player in shooting_team.players_list:
            there_was_a_drop = face_off(player, running_team, left_team, game_table, silent)
            if there_was_a_drop:
                there_was_a_drop_at_some_point = True
                taker = player.format_name()

        if there_was_a_drop_at_some_point:
            if not silent:
                declare_state(left_team, right_team, match_state, carrier)
                print(f"{taker} has manage to take {carrier.format_name()} down!")
                sleep(3)
            return "Drop"

        if check_touchdown(carrier, match_state, left_team, game_table):
            if not silent:
                declare_state(left_team, right_team, match_state, carrier)
                print(f"{carrier.format_name()} scored a touchdown!")
                sleep(3)
            return "Touchdown"

        if match_state["turn"] > 9:
            if not silent:
                declare_state(left_team, right_team, match_state, carrier)
                print(f"Time! the disc is now free!")
                sleep(3)
            return "Time"
