from Grid import Grid
from Utils import *
from helper_functions import *
import sys

PLAYER = 1
OPPONENT = 2


def new_trap_minimax(grid: Grid, depth, player, position, isMax):
    if depth > 5:
        # Todo: Something
        return board_value_of_trap(grid, position, player, 3 - player)
        # return board_value_of_trap(grid, move, player, 3-player)

    if len(get_opponent_neighbours(grid, player)) == 0:  # This is where we win
        return sys.maxsize

    if len(grid.get_neighbors(grid.find(player), only_available=True)) == 0:  # This is where opponent wins
        return -sys.maxsize

    if isMax:
        best_value = -sys.maxsize
        # putting trap against opponent
        grid.trap(position)
        # opponent's turn to move
        temporary_move = move_heuristic(OPPONENT, grid.find(OPPONENT), grid)
        grid.move(temporary_move, OPPONENT)
        # opponent will find the best neighbour to put a trap against us
        my_neighbors = grid.get_neighbors(grid.find(PLAYER))
        for i in range(len(my_neighbors)):
            # we call for opponent's turn
            score = new_trap_minimax(grid, depth + 1, 3-PLAYER, my_neighbors[i], False)
            best_value = max(best_value, score)
        return best_value

    else:
        # Opponent's Turn
        best_value = -sys.maxsize
        # opponent lays down the trap against us
        grid.trap(position)
        # player (us) will move to a position now
        temporary_move = move_heuristic(PLAYER, grid.find(PLAYER), grid)
        grid.move(temporary_move, PLAYER)
        # our turn to find the best trap against opponent
        my_neighbors = grid.get_neighbors(grid.find(OPPONENT))
        for i in range(len(my_neighbors)):
            score = new_trap_minimax(grid, depth + 1, PLAYER, my_neighbors[i], True)
            best_value = max(best_value, score)
        return best_value


def find_best_trap_new_minimax(grid: Grid, player_no):
    print("Minimax called")
    opponent_available_moves = get_opponent_neighbours(grid, player_num=player_no)
    trap_dict = {}
    grid_clone = grid.clone()
    for i in range(len(opponent_available_moves)):
        print("Checking Current Move:{}".format(opponent_available_moves[i]))
        trap_value = new_trap_minimax(grid_clone, 0, PLAYER, opponent_available_moves[i], True)
        trap_dict[opponent_available_moves[i]] = trap_value
    good_trap = max(trap_dict, key=trap_dict.get)
    return good_trap