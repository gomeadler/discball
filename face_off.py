from pandas import DataFrame
from player_class import Player
from team_class import Team
from data import increase_stat_by
from general import choose_player_by_probabilities, calculate_distance
from random import randint
from time import sleep


def choose_target(shooter: Player, eligible_players: list) -> Player:
    probabilities = []
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
              game_table):

    increase_stat_by(game_table, target_player.id, "balance_losses", 1)
    increase_stat_by(game_table, shooter.id, "successful_takedowns", 1)

    if target_player.has_disc:
        # meaning it was a carrier takedown and a drop

        target_player.reset_position(target_is_left, True)
        increase_stat_by(game_table, target_player.id, "drops_made", 1)
        increase_stat_by(game_table, shooter.id, "carrier_takedowns", 1)
        return True

    else:
        target_player.reset_position(target_is_left, True)
        return False


def retreat(target_player: Player, shooter: Player, left_team: Team, shot_quality: float,
            game_table: DataFrame) -> bool:

    blocks = determine_retreat(target_player.attributes["stability"], shot_quality)
    target_is_left = bool(target_player in left_team.line_up)
    there_is_a_takedown = False
    if target_is_left and target_player.column <= blocks:
        there_is_a_takedown = True
    elif not target_is_left and (21 - target_player.column) <= blocks:
        there_is_a_takedown = True

    if not target_is_left:

        blocks *= -1

    if there_is_a_takedown:
        result = take_down(target_player, shooter, target_is_left, game_table)
        return result

    else:
        target_player.column -= blocks
        return False


def face_off(shooter: Player, running_team: Team, left_team: Team,
             game_table: DataFrame, silent: bool) -> (bool, str):
    # choose a target
    eligible_players = [player for player in running_team.line_up if player.column not in [0, 21]]
    if len(eligible_players) == 0:
        return False
    target_player = choose_target(shooter, eligible_players)

    # determine shot quality and evasion attempt
    shot_quality = randint(1, shooter.attributes["shooting"]) // calculate_distance(shooter, target_player)
    evasion_attempt = randint(1, target_player.attributes["agility"])

    # evade or try to balance
    if shot_quality > evasion_attempt:
        increase_stat_by(game_table, shooter.id, "successful_shots", 1)
        increase_stat_by(game_table, target_player.id, "hits_taken", 1)
        if not silent:
            print(f"{shooter.format_name()} hit {target_player.format_name()}")
            sleep(1)

        there_was_a_drop = retreat(target_player, shooter, left_team, shot_quality, game_table)
        return there_was_a_drop
    else:
        increase_stat_by(game_table, target_player.id, "evasions", 1)
        return False
