from data import COLOR_RESET, COLOR_DICT


def create_block(line_color: str, dot_color: str = None) -> str:
    return f"{line_color}|{dot_color}|{COLOR_RESET}"


def get_positions(team: list) -> list:
    positions = []
    for player in team:
        positions.append(tuple([player.row, player.column]))
        if player.column not in range(22):
            raise ValueError(f"{player.format_name()} is in an invalid position. "
                             f"row: {player.row}, col: {player.column}")
    return positions


def determine_line_color(col: int):
    if col == 0 or col == 21:
        return COLOR_DICT["purple"]
    elif col == 10 or col == 11:
        return COLOR_DICT["cyan"]
    else:
        return COLOR_DICT["white"]  # Default color for other columns


def make_dot_or_number(row: int, col: int, match_state: dict, carrier_position: tuple,
                       left_positions: list, right_positions: list):
    if row == -1:  # meaning this is the header
        if col < 10:
            return str(col)
        elif col > 11:
            return str(21 - col)
        else:
            return "v"

    elif (row, col) == carrier_position:
        return match_state["carrier color"] + "*" + COLOR_RESET
    elif (row, col) in left_positions:
        return match_state["left color"] + "*" + COLOR_RESET
    elif (row, col) in right_positions:
        return match_state["right color"] + "*" + COLOR_RESET
    else:
        return " "


def create_field(left_team: list, right_team: list, match_state: dict, carrier_position: tuple):
    left_positions = get_positions(left_team)
    right_positions = get_positions(right_team)
    field_str = ""
    for row in range(-1, 10):
        row_str = ""
        for col in range(22):
            row_str += create_block(determine_line_color(col), make_dot_or_number(row, col, match_state,
                                                                                  carrier_position,
                                                                                  left_positions, right_positions))
        row_str += "\n"
        field_str += row_str
    print(field_str)
