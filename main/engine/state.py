from sprites.entities.player import Player
import copy

def actions(state):
    ''' Returns legal actions that can be executed on state ("lrtb") '''
    # Get obstacle directions
    def obstacle_directions(string):
        try:
            return string[string.index("[") + 1:string.index("]")]
        except ValueError:
            return []

    # Get cell information if it exists
    def get_cell_information(x_index, y_index):
        try:
            cell_information = state[y_index][x_index]
            if cell_information is None:
                return ""
            return cell_information
        except IndexError:
            return ""

    # Look for cell with player and check obstacles
    legal_actions = ""
    for y_index, row in enumerate(state):
        for x_index, cell in enumerate(row):
            if cell is None:
                continue

            # Get cell obstacles
            current_cell = obstacle_directions(cell)
            left_cell = obstacle_directions(get_cell_information(x_index - 1, y_index))
            right_cell = obstacle_directions(get_cell_information(x_index + 1, y_index))
            top_cell = obstacle_directions(get_cell_information(x_index, y_index - 1))
            bottom_cell = obstacle_directions(get_cell_information(x_index, y_index + 1))

            if "(player)" in cell:
                # Check left and adjacent cells and if it's border
                if not ("l" in current_cell or "r" in left_cell or x_index == 0):
                    legal_actions += "l"
                # Check right and adjacent cells and if it's border
                if not ("r" in current_cell or "l" in right_cell or x_index == len(row) - 1):
                    legal_actions += "r"
                # Check top and adjacent cells and if it's border
                if not ("t" in current_cell or "b" in top_cell or y_index == 0):
                    legal_actions += "t"
                # Check bottom and adjacent cells and if it's border
                if not ("b" in current_cell or "t" in bottom_cell or y_index == len(state) - 1):
                    legal_actions += "b"

                return legal_actions


def result(state, action):
    ''' Returns the state after performing action on state '''
    # If no action or it's not in possible actions, no modification
    if action == None or action not in actions(state):
        return state

    # Make copy of state
    new_state = copy.deepcopy(state)
    # Edit state
    # Find player cell
    for y_index, row in enumerate(state):
        for x_index, cell in enumerate(row):
            if cell is None:
                continue

            if "(player)" in cell:
                # Remove player in previous place
                new_state[y_index][x_index] = new_state[y_index][x_index].replace("(player)", "")
                # If nothing is on the right side anymore
                if not "[" in new_state[y_index][x_index] and not "(" in new_state[y_index][x_index]:
                    new_state[y_index][x_index] = new_state[y_index][x_index].replace(":", "")

                # Apply respective changes
                # https://stackoverflow.com/questions/1034573/python-most-idiomatic-way-to-convert-none-to-empty-string
                # left
                player_replacement = "(player)"
                # For or syntax: None or "" => "" and 'not None' or "" => 'not None'
                if action == "l":
                    new_cell_contents = new_state[y_index][x_index - 1] or ""
                    # If it's currently not divided into typeOfTile:tileInfo
                    if not "[" in new_cell_contents and not "(" in new_cell_contents and new_cell_contents != "":
                        player_replacement = ":" + player_replacement
                    new_state[y_index][x_index - 1] = new_cell_contents + player_replacement
                # right
                elif action == "r":
                    new_cell_contents = new_state[y_index][x_index + 1] or ""
                    # If it's currently not divided into typeOfTile:tileInfo
                    if not "[" in new_cell_contents and not "(" in new_cell_contents and new_cell_contents != "":
                        player_replacement = ":" + player_replacement
                    new_state[y_index][x_index + 1] = new_cell_contents + player_replacement
                # top
                elif action == "t":
                    new_cell_contents = new_state[y_index - 1][x_index] or ""
                    # If it's currently not divided into typeOfTile:tileInfo
                    if not "[" in new_cell_contents and not "(" in new_cell_contents and new_cell_contents != "":
                        player_replacement = ":" + player_replacement
                    new_state[y_index - 1][x_index] = new_cell_contents + player_replacement
                # bottom
                elif action == "b":
                    new_cell_contents = new_state[y_index + 1][x_index] or ""
                    # If it's currently not divided into typeOfTile:tileInfo
                    if not "[" in new_cell_contents and not "(" in new_cell_contents and new_cell_contents != "":
                        player_replacement = ":" + player_replacement
                    new_state[y_index + 1][x_index] = new_cell_contents + player_replacement
                print(new_state)
                return new_state


def winner(state):
    ''' Determine the winner of the game '''
    # Horizontal
    for row in state:
        if row[0] == row[1] == row[2]:
            return row[0]

    # Vertical
    board_width = 3
    for i in range(board_width):
        if state[0][i] == state[1][i] == state[2][i]:
            return state[0][i]

    # Diagonal (tl - br)
    if state[0][0] == state[1][1] == state[2][2]:
        return state[1][1]
    # Diagonal (tr - bl)
    if state[0][2] == state[1][1] == state[2][0]:
        return state[1][1]


def terminal(state):
    ''' Returns True if game is over, False otherwise. '''
    def full(state):
        for row in state:
            for cell in row:
                if cell == EMPTY:
                    return False
        return True

    # If there is no longer any empty cells or there is winner
    if full(state) or winner(state) != None:
        return True
    return False


def utility(state):
    ''' Final numerical value for terminal state '''
    if winner(state) == "player":
        return 1
    elif winner(state) == "enemy":
        return -1
    else:
        return 0
