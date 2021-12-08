from Grid import Grid
from Utils import *
from helper_functions import *
import sys


def trap_minimax(grid: Grid, depth, player_no, move, isMax):
    print("\n Current Move :{}".format(move))
    position = move
    grid.move(position, 3 -player_no)
    print("player_no:{}".format(player_no))
    if len(get_opponent_neighbours(grid, player_no)) == 0:
        return board_value(grid, grid.find(player_no), grid.find(3 - player_no))
    if len(grid.get_neighbors(position)) == 0:
        return board_value(grid, grid.find(player_no), grid.find(3 - player_no))
        #return board_value(grid, grid.find(player_no), grid.find(3 - player_no))
    if depth > 2: #or get_opponent_neighbours(grid, player_no) == 0:
        return board_value(grid, grid.find(player_no), grid.find(3 - player_no))
    if isMax:
        print("Entered isMax with Player No:{}".format(player_no))
        best_val = -sys.maxsize
        # my_new_available_moves = grid.get_neighbors(position, only_available=True)
        my_new_available_moves = grid.get_neighbors(grid.find(3 - player_no), only_available=True)
        for i in range(len(my_new_available_moves)):
            print("Checking Current Move:{}".format(my_new_available_moves[i]))
            heuristic_value = board_value(grid, grid.find(player_no), move)
            # heuristic_value = board_value_for_moves(grid, grid.find(player_no))
            print("heuristic_value returned:{}".format(heuristic_value))
            recursive_value = trap_minimax(grid, depth+1, player_no, my_new_available_moves[i], False)
            print("recursive_value returned:{}".format(recursive_value))
            best_val = max(heuristic_value, recursive_value)
            print("best_val:{}".format(best_val))
        return best_val
    else:
        print("Entered Min with Player No:{}".format(player_no))
        best_val = sys.maxsize
        # my_new_available_moves = grid.get_neighbors(position, only_available=True)
        my_new_available_moves = grid.get_neighbors(grid.find(3-player_no), only_available=True)
        for i in range(len(my_new_available_moves)):
            print("Checking Current Move:{}".format(my_new_available_moves[i]))
            heuristic_value = board_value(grid, move, grid.find(3 - player_no))
            print("heuristic_value returned:{}".format(heuristic_value))
            recursive_value = trap_minimax(grid, depth+1, player_no, my_new_available_moves[i], True)
            print("recursive_value returned:{}".format(recursive_value))
            best_val = min(heuristic_value, recursive_value)
            print("best_val:{}".format(best_val))
        return best_val


def find_best_trap(grid: Grid, player_no):
    print("Minimax called")
    opponent_available_moves = get_opponent_neighbours(grid, player_num=player_no)
    trap_dict = {}
    grid_clone = grid.clone()
    for i in range(len(opponent_available_moves)):
        print("Checking Current Move:{}".format(opponent_available_moves[i]))
        trap_value = trap_minimax(grid_clone, 0, player_no, opponent_available_moves[i], True)
        trap_dict[opponent_available_moves[i]] = trap_value
    good_trap = max(trap_dict, key=trap_dict.get)
    return good_trap