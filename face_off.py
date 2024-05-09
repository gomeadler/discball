from pandas import DataFrame
from player_class import Player
from data import increase_stat_by
from general import choose_player_by_probabilities, calculate_distance
from random import randint
from typing import Union
from time import sleep


def choose_target(shooter: Player, running_team: list) -> Union[Player, None]:
    eligible_players = [player for player in running_team if player.column not in [0, 21]]
    probabilities = []
    if len(eligible_players) == 0:
        return None
    for rival in eligible_players:
        distance = calculate_distance(shooter, rival)
        try:
            probabilities.append(5 / distance if rival.has_disc else 1 / distance)
        except ZeroDivisionError:
            print(f"{shooter.format_name()} tried to shoot {rival.format_name()} "
                  f"but the distance calculated was {distance}")
    return choose_player_by_probabilities(eligible_players, probabilities)


def determine_retreat(target_balance: int, shot_quality: float) -> int:
    balance_attempt = randint(1, target_balance) // 3
    if balance_attempt > shot_quality:
        blocks = 2
    elif balance_attempt == shot_quality:
        blocks = 5
    else:
        blocks = 10
    return blocks


def take_down(target_player: Player, shooter: Player, target_is_left: bool,
              target_table: DataFrame, shooter_table: DataFrame):

    increase_stat_by(target_table, target_player.attributes["Shirt number"] - 1, "balance_losses", 1)
    increase_stat_by(shooter_table, shooter.attributes["Shirt number"] - 1, "successful_takedowns", 1)

    if target_player.has_disc:
        # meaning it was a carrier takedown and a drop

        target_player.reset_position(target_is_left, True)
        increase_stat_by(target_table, target_player.attributes["Shirt number"] - 1, "drops_made", 1)
        increase_stat_by(shooter_table, shooter.attributes["Shirt number"] - 1, "carrier_takedowns", 1)
        return True

    else:
        target_player.reset_position(target_is_left, True)
        return False


def retreat(target_player: Player, shooter: Player, left_team_players_list: list, shot_quality: float,
            left_table: DataFrame, right_table: DataFrame) -> bool:
    """ Makes a player who have taken a hit retreat backwards.

    :param target_player:
    :param shooter:
    :param left_team_players_list:
    :param shot_quality:
    :param left_table:
    :param right_table:
    :return:
    """

    blocks = determine_retreat(target_player.attributes["stability"], shot_quality)
    target_is_left = bool(target_player in left_team_players_list)
    there_is_a_takedown = False
    if target_is_left and target_player.column <= blocks:
        there_is_a_takedown = True
    elif not target_is_left and (21 - target_player.column) <= blocks:
        there_is_a_takedown = True

    if target_is_left:
        target_table = left_table
        shooter_table = right_table
    else:
        blocks *= -1
        target_table = right_table
        shooter_table = left_table

    if there_is_a_takedown:
        result = take_down(target_player, shooter, target_is_left, target_table, shooter_table)
        return result

    else:
        target_player.column -= blocks
        return False


def face_off(shooter: Player, running_team: list, left_team_players_list: list,
             left_table: DataFrame, right_table: DataFrame, silent: bool) -> (bool, str):
    # choose a target
    target_player = choose_target(shooter, running_team)
    if target_player is None:
        return False, None

    # determine shot quality and evasion attempt
    shot_quality = randint(1, shooter.attributes["shooting"]) // calculate_distance(shooter, target_player)
    evasion_attempt = randint(1, target_player.attributes["agility"])

    # check on which team the shooter is
    if shooter in left_team_players_list:
        shooter_table, target_table = left_table, right_table
    else:
        shooter_table, target_table = right_table, left_table

    # evade or try to balance
    if shot_quality > evasion_attempt:
        increase_stat_by(shooter_table, shooter.attributes["Shirt number"] - 1, "successful_shots", 1)
        increase_stat_by(target_table, target_player.attributes["Shirt number"] - 1, "hits_taken", 1)
        if not silent:
            print(f"{shooter.format_name()} hit {target_player.format_name()}")
            sleep(1)

        there_was_a_drop = retreat(target_player, shooter, left_team_players_list, shot_quality,
                                   left_table, right_table)
        return there_was_a_drop
    else:
        increase_stat_by(target_table, target_player.attributes["Shirt number"] - 1, "evasions", 1)
        return False
