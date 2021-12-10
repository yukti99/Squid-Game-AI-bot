from Grid import Grid
from Utils import *
import sys
import random
from helper_functions import *
ALPHA = -sys.maxsize
BETA = sys.maxsize

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


def basic_heuristic_for_new_trap(grid, opponent_pos):
    opponent_neighbours = len(grid.get_neighbors(opponent_pos, only_available=True))
    return -opponent_neighbours


# motive: trap the opponent based on some heuristic
def minimax_trap(grid: Grid, depth, player, isMax, alpha, beta):
    '''
    BASE CASES
    '''
    opp_neighbours = get_opponent_neighbours(grid, player)
    player_neighbours = grid.get_neighbors(grid.find(player), only_available=True)

    if depth > 3:
        opponent_pos = grid.find(3-player)
        player_pos = grid.find(player)
        # return basic heuristic when depth reached
        return basic_heuristic(grid, player_pos, opponent_pos)

    # if we win
    if len(opp_neighbours) == 0:
        return sys.maxsize

    # if opponent wins
    if len(player_neighbours) == 0:
        return -sys.maxsize

    good_traps_against_opponent = trap_h(player, grid)
    if isMax is True:
        # we put trap
        best_value = -sys.maxsize

        for i in good_traps_against_opponent:

            hit_probability = 1 - 0.05 * (manhattan_distance(grid.find(player), i) - 1)
            all_possible_positions = grid.get_neighbors(i, only_available=True)
            all_possible_positions.append(i)
            # missing_probability = ((1 - hit_probability) / len(grid.get_neighbors(i)))
            # expectation = 0
            #
            # for j in range(len(all_possible_positions)):
            #     if i == all_possible_positions[j]:
            # grid.setCellValue(all_possible_positions[j], -1)
            grid.setCellValue(i, -1)
            best_value = minimax_trap(grid, depth + 1, player, False, alpha, beta)
            expectation = hit_probability * best_value
            grid.setCellValue(all_possible_positions[j], 0)
                # else:
                #     expectation = expectation + missing_probability * best_value

            best_value = max(best_value, expectation)
            alpha = max(alpha, best_value)
            if beta <= alpha:
                print("BREAK!!!")
                break

        return best_value

    else:
        # opponent moves
        best_value = sys.maxsize
        previous_player_position = grid.find(3-player)
        for j in good_traps_against_opponent:
            grid.move(j, 3-player)
            best_value = min(best_value, minimax_trap(grid, depth+1, player, True, alpha, beta))
            beta = min(beta, best_value)
            grid.move(previous_player_position, 3-player)
            if beta <= alpha:
                break
        return best_value


def get_unavailable_neighbors(grid, player):
    all_neighbors = grid.get_neighbors(pos=grid.find(player), only_available=False)
    unavailable_neighbors = []
    for i in range(len(all_neighbors)):
        if grid.getCellValue(pos=all_neighbors[i]) == -1:
            unavailable_neighbors.append(all_neighbors[i])
    return unavailable_neighbors


def find_trap(grid, player):
    # print("USING NEW TRAP MINMAX ----------------------------------")
    # get opponent available moves
    opp_neighbours = get_opponent_neighbours(grid, player)
    if len(opp_neighbours) == 0:
        unavailable_neighbors = get_unavailable_neighbors(grid, player)
        return random.choice(unavailable_neighbors)
    else:
        grid_clone = grid.clone()
        good_trap = -sys.maxsize
        good_trap_pos = random.choice(opp_neighbours)
        for i in range(len(opp_neighbours)):
            # print("Placing trap on = ", opp_neighbours[i], " in th grid and called minmax for the same")
            grid_clone.setCellValue(opp_neighbours[i], -1)
            trap_value = minimax_trap(grid_clone, 0, player,  True, ALPHA, BETA)
            grid_clone.setCellValue(opp_neighbours[i], 0)
            # print("\n Trap value obtained for -", opp_neighbours[i], " is  = ", trap_value)
            if good_trap < trap_value:
                good_trap = trap_value
                good_trap_pos = opp_neighbours[i]
        return good_trap_pos

