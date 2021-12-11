from Grid import Grid
from Utils import *
import sys
import random
from helper_functions import *
ALPHA = -sys.maxsize
BETA = sys.maxsize


def move_heuristic(player_num: int, grid: Grid):
    opponent_pos = get_opponent_position(grid=grid, player_num=player_num)
    grid_clone = grid.clone()
    position = grid.find(player_num)
    my_new_available_moves = grid_clone.get_neighbors(position, only_available=True)
    moves_dict = {}
    # grid_clone.print_grid()
    for i in range(len(my_new_available_moves)):
        # board_v = board_value_for_moves(grid_clone, my_new_available_moves[i])
        board_v = board_value(grid_clone, my_new_available_moves[i], opponent_pos)
        moves_dict[my_new_available_moves[i]] = board_v
        # print("Position: {} and board value:{}".format(my_new_available_moves[i], board_v))
    max_position = list(sorted(moves_dict, key=moves_dict.get, reverse=True))
    return max_position


def get_opponent_neighbours(grid: Grid, player_num: int):
    opponent_pos = grid.find(3-player_num)
    opponent_neighbours = grid.get_neighbors(opponent_pos, only_available=True)
    return opponent_neighbours


# heuristic given to us by them
def basic_heuristic(grid, my_position, opponent_pos, depth):
    no_neighbours = len(grid.get_neighbors(my_position, only_available=True))
    opponent_neighbours = len(grid.get_neighbors(opponent_pos, only_available=True))
    return 2*no_neighbours - opponent_neighbours


# motive: trap the opponent based on some heuristic
def minimax_move(grid: Grid, depth, player, isMax,  alpha, beta, current_move: tuple):
    '''
    BASE CASES
    '''
    opp_neighbours = get_opponent_neighbours(grid, player)
    player_neighbours = grid.get_neighbors(grid.find(player), True)

    if depth > 3:
        # print("Reducing Depth and returning basic heuristic!!")
        opponent_pos = grid.find(3-player)
        player_pos = grid.find(player)
        # return basic heuristic when depth reached
        b = basic_heuristic(grid, player_pos, opponent_pos, depth)
        # print("bh = ", b)
        # print()
        return b

    # if we win
    if len(opp_neighbours) == 0:
        # print("In this trial we won! and returned maxsize")
        return sys.maxsize

    # if opponent wins
    if len(player_neighbours)== 0:
        # print("In this trial opponent won! and returned minsize")
        return -sys.maxsize

    good_moves_for_player = move_heuristic(player, grid)
    if isMax == 1:
        # we move
        # print("entered isMAx....")
        best_value = -sys.maxsize
        # print("min val initialized = ", best_value)
        previous_player_position = grid.find(player)
        # print("Checking is pos = ", previous_player_position, " is good or not")
        for i in good_moves_for_player:
            grid.move(i, player)
            # print("player moved to ",i," in the grid")
            # grid.print_grid()
            best_value = max(best_value, minimax_move(grid, depth+1, player, 0, alpha, beta, (0,0)))
            alpha = max(alpha, best_value)
            # print("best value obtained = ", best_value)
            grid.move(previous_player_position, player)
            # Alpha Beta Pruning
            if beta <= alpha:
                # print("Tree Pruning in MAX MOVE!")
                break
            # print("moved player in grid to previous pos = ", previous_player_position)
            # grid.print_grid()
            # print()
        return best_value

    elif isMax == 0:
        # print("entered isMin....")
        # opponent puts trap
        best_value = sys.maxsize
        for j in good_moves_for_player:
            # print("setting - ", j," pos as trap")
            # grid.setCellValue(j, -1)
            # grid.print_grid()
            expectation = minimax_move(grid, depth, player, 2, alpha, beta, j)
            best_value = min(expectation, best_value)
            beta = min(beta, best_value)
            # print("best min value obtained = ",best_value)
            # print("resetting - ",j ," pos as empty")
            # grid.setCellValue(j, 0)
            # Alpha Beta Pruning
            if beta <= alpha:
                # print("Tree Pruning in MIN MOVE!")
                break
            # grid.print_grid()
            # print()
        return best_value

    else:
        # chance node
        best_value = sys.maxsize
        current_trap_position = current_move
        hit_probability = 1 - 0.05 * (manhattan_distance(grid.find(3-player), current_trap_position) - 1)
        missing_probability = ((1 - hit_probability) / len(grid.get_neighbors(current_trap_position)))
        expectation = 0
        all_possible_positions = grid.get_neighbors(current_trap_position, only_available=True)
        all_possible_positions.append(current_trap_position)
        for j in range(len(all_possible_positions)):
            grid.setCellValue(all_possible_positions[j], -1)

            if current_trap_position == all_possible_positions[j]:
                best_value = minimax_move(grid, depth + 1, player, 1, alpha, beta, (0, 0))
                expectation = expectation + hit_probability * best_value
            else:
                best_value = minimax_move(grid, depth + 1, player, 1, alpha, beta, (0, 0))
                expectation = expectation + missing_probability * best_value

            grid.setCellValue(all_possible_positions[j], 0)

        # alpha = max(alpha, best_value)
        # if beta <= alpha:
        #     print("BREAK!!!")
        #     break
        return expectation


def find_move(grid, player):
    # print("USING NEW MOVE MINMAX ----------------------------------")
    # get opponent available moves
    my_neighbours = grid.get_neighbors(grid.find(player), True)
    grid_clone = grid.clone()
    good_move = -sys.maxsize
    good_move_pos = random.choice(my_neighbours)
    for i in range(len(my_neighbours)):
        # print("moving player to = ",my_neighbours[i], " in th grid and called minmax for the same")
        grid_clone.move(my_neighbours[i], player)
        move_value = minimax_move(grid_clone, 0, player, 1, ALPHA, BETA, (0,0))
        grid_clone.setCellValue(my_neighbours[i], 0)
        # print("\n Move value obtained for -", my_neighbours[i], " is  = ", move_value)
        # print()
        if good_move < move_value:
            good_move = move_value
            good_move_pos = my_neighbours[i]
    return good_move_pos

