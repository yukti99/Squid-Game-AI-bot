from Grid import Grid
from Utils import *
from helper_functions import *
import sys

PLAYER = 1
OPPONENT = 2

def new_move_minimax(grid: Grid, depth, player, move, isMax):
    if depth > 5:
        # Todo: Something
        return board_value_for_moves(grid, move)
        # return board_value_of_trap(grid, move, player, 3-player)

    if len(get_opponent_neighbours(grid, player)) == 0:                         # This is where we win
        return sys.maxsize

    if len(grid.get_neighbors(grid.find(player), only_available=True)) == 0:    # This is where opponent wins
        return -sys.maxsize

    if isMax:
        best_value = -sys.maxsize
        grid.move(move, player)
        temporary_trap = trap_h(player_num=player, grid=grid)
        grid.trap(temporary_trap)
        grid.print_grid()
        # my_new_available_moves = grid.get_neighbors(grid.find(player), only_available=True)
        opponent_neighbors = get_opponent_neighbours(grid, player)
        for i in range(len(opponent_neighbors)):
            # score = heuristic_function(grid, my_new_available_moves[i], player=player, opponent=3 - player)
            score = new_move_minimax(grid, depth+1, 3 - player, opponent_neighbors[i], False)
            best_value = max(best_value, score)
        return best_value

    else:
        ## Opponent's Turn
        # print("\n Entered Min with Player No:{}".format(player))
        best_value = -sys.maxsize
        # opponent = 3 - player
        grid.move(move, player)
        temporary_trap = trap_h(player_num=player, grid=grid)
        grid.trap(temporary_trap)
        grid.print_grid()
        opponent_neighbors = get_opponent_neighbours(grid, player)
        for i in range(len(opponent_neighbors)):
            # score = heuristic_function(grid, my_new_available_moves[i], player=player, opponent=3 - player)
            score = new_move_minimax(grid, depth + 1, 3 - player, opponent_neighbors[i], True)
            best_value = max(best_value, score)
        return best_value








        #
        # best_opponent_pos = Something
        # grid.move(best_opponent_pos, opponent)
        #
        # best_trap = something
        # grid.trap(best_trap)



        #
        # my_new_available_moves = grid.get_neighbors(grid.find(player), only_available=True)
        # for i in range(len(my_new_available_moves)):
        #     # score = heuristic_function(grid, my_new_available_moves[i], player=player, opponent=3 - player)
        #     score = new_move_minimax(grid, depth + 1, player, my_new_available_moves[i], True)
        #     best_value = min(best_value, score)
        # # grid.print_grid()
        # return best_value



def find_best_move_new_minmax(grid: Grid, player_no):
    my_position = grid.find(player_no)
    my_new_available_moves = grid.get_neighbors(my_position, only_available=True)
    moves_dict = {}
    grid_clone = grid.clone()
    for i in range(len(my_new_available_moves)):
        move_value = new_move_minimax(grid_clone, 0, player_no, my_new_available_moves[i], True)
        moves_dict[my_new_available_moves[i]] = move_value
    good_move = max(moves_dict, key=moves_dict.get)
    return good_move