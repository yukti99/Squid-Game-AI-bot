from Grid import Grid
from Utils import *
import sys
import random
from helper_functions import *


def move_heuristic(player_num: int, position, grid: Grid):
    opponent_pos = get_opponent_position(grid=grid, player_num=player_num)
    grid_clone = grid.clone()
    my_new_available_moves = grid_clone.get_neighbors(position, only_available=True)
    moves_dict = {}
    grid_clone.print_grid()
    for i in range(len(my_new_available_moves)):
        board_v = board_value_for_moves(grid_clone, my_new_available_moves[i])
        moves_dict[my_new_available_moves[i]] = board_v
        # print("Position: {} and board value:{}".format(my_new_available_moves[i], board_v))
    max_position = list(sorted(moves_dict, key=moves_dict.get, reverse=True))
    return max_position


def get_opponent_neighbours(grid: Grid, player_num: int):
    opponent_pos = grid.find(3-player_num)
    opponent_neighbours = grid.get_neighbors(opponent_pos, only_available=True)
    return opponent_neighbours


# heuristic given to us by them
def basic_heuristic(grid, my_position, opponent_pos):
    no_neighbours = len(grid.get_neighbors(my_position, only_available=True))
    opponent_neighbours = len(grid.get_neighbors(opponent_pos, only_available=True))
    return 2*no_neighbours - opponent_neighbours


# motive: trap the opponent based on some heuristic
def minimax_move(grid: Grid, depth, player, isMax):
    '''
    BASE CASES
    '''
    opp_neighbours = get_opponent_neighbours(grid, player)
    player_neighbours = grid.get_neighbors(grid.find(player), True)

    if depth > 3:
        opponent_pos = grid.find(3-player)
        player_pos = grid.find(player)
        # return basic heuristic when depth reached
        return basic_heuristic(grid, player_pos, opponent_pos)

    # if we win
    if len(opp_neighbours):
        return sys.maxsize

    # if opponent wins
    if len(player_neighbours):
        return -sys.maxsize

    good_moves_for_player = move_heuristic(player, grid)
    if isMax is True:
        # we move
        best_value = -sys.maxsize
        previous_player_position = grid.find(player)
        for i in good_moves_for_player:
            grid.move(i, player)
            best_value = max(best_value, minimax_move(grid, depth+1, player, False))
            grid.move(previous_player_position, player)
        return best_value

    else:
        # opponent puts trap
        best_value = sys.maxsize
        for j in good_moves_for_player:
            grid.setCellValue(j, -1)
            best_value = min(best_value, minimax_move(grid, depth+1, player, True))
            grid.setCellValue(j, 0)
        return best_value


def find_move(grid, player):
    print("USING NEW MOVE MINMAX ----------------------------------")
    # get opponent available moves
    my_neighbours = grid.get_neighbors(grid.find(player), True)
    grid_clone = grid.clone()
    good_move = -sys.maxsize
    good_move_pos = (-1, -1)
    for i in range(len(my_neighbours)):
        # print("Checking Current Move:{}".format(opp_neighbours[i]))
        grid.move(my_neighbours[i], player)
        move_value = minimax_move(grid_clone, 0, player,  True)
        if good_move < move_value:
            good_move = move_value
            good_move_pos = my_neighbours[i]
    return good_move_pos

