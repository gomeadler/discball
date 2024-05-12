from data import COLOR_RESET, COLOR_DICT


def create_block(line_color: str, dot_color: str = None) -> str:
    if dot_color is None:
        return f"{line_color}| |{COLOR_RESET}"
    elif dot_color in str(list(range(22))):
        if int(dot_color) > 10:
            dot_color = str(21 - int(dot_color))
        if dot_color == str(10):
            dot_color = "v"
        return f"{line_color}|{dot_color}|{COLOR_RESET}"
    else:
        return f"{line_color}|{dot_color}*{line_color}|{COLOR_RESET}"


def get_positions(team: list) -> list:
    positions = []
    for player in team:
        positions.append(tuple([player.row, player.column]))
        if player.column not in range(22):
            raise ValueError(f"{player.format_name()} is in an invalid position. "
                             f"row: {player.row}, col: {player.column}")
    return positions


def create_field(left_team: list, right_team: list, match_state: dict, carrier_position: tuple):
    # TODO: maybe can be done more efficiently

    left_positions = get_positions(left_team)
    right_positions = get_positions(right_team)
    field_str = ""
    header = ""
    for num in range(22):
        # special columns
        if num == 0 or num == 21:
            header += create_block(COLOR_DICT["purple"], str(num))
        elif num == 10 or num == 11:
            header += create_block(COLOR_DICT["cyan"], str(num))
        else:
            header += create_block(COLOR_DICT["white"], str(num))  # Default color for other columns
    header += "\n"
    field_str += header

    for row in range(10):
        row_str = ""
        for col in range(22):
            dot = None
            if (row, col) == carrier_position:
                dot = match_state["carrier color"]
            elif (row, col) in left_positions:
                dot = match_state["left color"]
            elif (row, col) in right_positions:
                dot = match_state["right color"]

            # special columns
            if col == 0 or col == 21:
                row_str += create_block(COLOR_DICT["purple"], dot)
            elif col == 10 or col == 11:
                row_str += create_block(COLOR_DICT["cyan"], dot)
            else:
                row_str += create_block(COLOR_DICT["white"], dot)  # Default color for other columns
        row_str += "\n"
        field_str += row_str
    print(field_str)
