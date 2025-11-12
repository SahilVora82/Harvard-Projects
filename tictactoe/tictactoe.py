"""
Tic Tac Toe Player
"""

import math
import copy # For deepcopy
X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    xCount = 0
    oCount = 0
    for row in board:
        for space in row:
            if space == X:
                xCount += 1
            if space == O:
                oCount +=1
    if xCount <= oCount: # X is the first move. Assuming both have been played the same amount, it should be X's turn
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possibleActions = set()
    for i in range(0,3):
        for j in range(0,3):
            if board[i][j] == EMPTY: # If a square is empty, a move can be made there
                possibleActions.add((i,j))

    return possibleActions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board): # First check if the variable action is a possible move for that board
        raise Exception("Not a move")

    newBoard = copy.deepcopy(board) # If so, make a new (deep)copy of the board
    newBoard[action[0]][action[1]] = player(board) # Implement this change to the copied board. Uses the player function to see whether to put an X or O

    return newBoard

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    result = utility(board)
    if result == 1:
        return X
    if result == -1:
        return O
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if utility(board) == 1 or utility(board) == -1: # If there is a three in a row, there is a winner
        return True

    # Check for remaining moves on the board
    for row in board: # Check if there are empty spaces. If so, means that game is still going on
        for space in row:
            if space == EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # check horizontal:
    for row in board:
        if row[0] == row [1] == row[2] and row[0] is not EMPTY:
            if row[0] == X:
                return 1
            if row[0] == O:
                return -1

    # check vertical
    for i in range(0,3):
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not EMPTY:
            if board[0][i] == X:
                return 1
            if board[0][i] == O:
                return -1
    # check from top left to bottom right
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not EMPTY:
        if board[0][0] == X:
            return 1
        if board[0][0] == O:
            return -1

    # check from top right to bottom left
    if board[0][2] == board[1][1] == board[2][0] and board[2][0] is not EMPTY:
        if board[1][1] == X:
            return 1
        if board[1][1] == O:
            return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    currentPlayer = player(board)
    if currentPlayer == X: # Maximizing player
        (bestValue, bestMove) = Max_Value(board)
        return bestMove
    else: # if O
        (bestValue, bestMove) = Min_Value(board) # Minimizing player
        return bestMove


def Max_Value(board):
    if terminal(board): # First check if the game is over
        return utility(board), None
    v = -math.inf # So next position is by default going to be greater
    bestAction = None
    for action in actions(board):
        minimumValueAction = Min_Value(result(board, action))
        minimumValue = minimumValueAction[0]
        if minimumValue > v: # Maximizing the values that the minimizing player can play
            bestAction = action
            v = minimumValue
        if v == 1: # Pruning. If found position with v =1 , no need to continue
            return v, action

    return v, bestAction

def Min_Value(board):
    if terminal(board): # Check if game is over
        return utility(board), None
    bestAction = None
    v = math.inf # Next position will by default be smaller
    for action in actions(board):
        maximumValueAction = Max_Value(result(board, action))
        maximumValue = maximumValueAction[0]
        if maximumValue < v: # Minimizing the value that the max player plays
            bestAction = action
            v = maximumValue
        if v == -1: # Pruning. If found position with v = -1 , no need to continue
            return v, action
    return v, bestAction
