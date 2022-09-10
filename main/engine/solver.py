from engine.state import *

def minimax(board):
    ''' Returns the optimal action for the current player on the board. '''
    def max_value(board, alpha, beta):
        if terminal(board):
            return [utility(board), None]

        # n will always be greater than -inf, therefore, chosen_action=None will always be changed
        v = float("-inf")
        chosen_action = None

        for action in actions(board):
            node_value = min_value(result(board, action), alpha, beta)[0]
            if node_value > v:
                v = node_value
                chosen_action = action

            if node_value >= beta:
                break
            alpha = max(alpha, node_value)
        return [v, chosen_action]

    def min_value(board, alpha, beta):
        if terminal(board):
            return [utility(board), None]

        # n will always be less than inf, therefore, chosen_action=None will always be changed
        v = float("inf")
        chosen_action = None

        for action in actions(board):
            node_value = max_value(result(board, action), alpha, beta)[0]
            if node_value < v:
                v = node_value
                chosen_action = action

            if node_value <= alpha:
                break
            beta = min(beta, node_value)
        return [v, chosen_action]

    # Starting
    # If current player is X -> Maximizing agent
    if player(board) == X:
        return max_value(board, float("-inf"), float("inf"))[1]

    # Elif current player is O -> Minimizing agent
    else:
        return min_value(board, float("-inf"), float("inf"))[1]
