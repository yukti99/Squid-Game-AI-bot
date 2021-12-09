from Grid import Grid
from Utils import *
import sys
import random
from helper_functions import *


def trap_h(player_num: int, grid: Grid):
    opponent_neighbours = get_opponent_neighbours(grid, player_num=player_num)
    board_value_dict = {}
    grid_clone = grid.clone()
    player_pos = grid.find(player_num)
    for i in range(len(opponent_neighbours)):
        if grid_clone.getCellValue(opponent_neighbours[i]) == 0:
            board_v = board_value(grid_clone, opponent_neighbours[i], player_pos)
            # print("Position: {} and board value:{}".format(opponent_neighbours[i], board_v))
            board_value_dict[opponent_neighbours[i]] = board_v
    max_position = list(sorted(board_value_dict, key=board_value_dict.get,reverse=True))
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
def minimax_trap(grid: Grid, depth, player, isMax):
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

    good_traps_against_opponent = trap_heuristic(player, grid)
    if isMax is True:
        # we put trap
        best_value = -sys.maxsize
        for i in good_traps_against_opponent:
            grid.trap(i)
            best_value = max(best_value, minimax_trap(grid, depth+1, player, False))
            grid.setCellValue(i, 0)
        return best_value

    else:
        # opponent moves
        best_value = sys.maxsize
        previous_player_position = grid.find(3-player)
        for j in good_traps_against_opponent:
            grid.move(j, 3-player)
            best_value = min(best_value, minimax_trap(grid, depth+1, player, True))
            grid.move(previous_player_position, 3-player)
        return best_value


def find_trap(grid, player):
    print("USING NEW TRAP MINMAX ----------------------------------")
    # get opponent available moves
    opp_neighbours = get_opponent_neighbours(grid, player)
    grid_clone = grid.clone()
    good_trap = -sys.maxsize
    good_trap_pos = (-1, -1)
    for i in range(len(opp_neighbours)):
        # print("Checking Current Move:{}".format(opp_neighbours[i]))
        grid.trap(opp_neighbours[i])
        trap_value = minimax_trap(grid_clone, 0, player,  True)
        if good_trap < trap_value:
            good_trap = trap_value
            good_trap_pos = opp_neighbours[i]
    return good_trap_pos

