from Grid import Grid
from Utils import *
import sys

def trap_heuristic(grid:Grid, trap_pos, player_num):
    opponent = 3-player_num


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
def minimax_trap(grid: Grid, depth, player, position, isMax):
    '''
    BASE CASES
    '''
    opp_neighbours = get_opponent_neighbours(grid, player)
    player_neighbours = grid.get_neighbors(grid.find(player), True)
    if depth > 2:
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

    if isMax is True:
        # we put trap
        best_value = -sys.maxsize
        # add a trap to the current position
        grid.trap(position)
        # grid changes
        good_trap_positions = trap_heuristic()
        for i in good_trap_positions:
            grid.trap(i)
            best_value = max(best_value, minimax_trap(grid, depth+1, player, False))
            grid.untrap(i)
        for pos in grid.get
        return best_value
    else:
        # opponent moves
        best_value = sys.maxsize
        good_trap_positions = trap_heuristic()
        for j in good_moves_opponent:
            grid.move(opponent,j)
            good_trap_positions
            best_value = min(best_value, minimax_trap(grid, depth+1, player, False))
            grid.move_to_previous(opponent,j)
        return best_value


def find_traps(grid, player):
    # get opponent available moves
    opp_neighbours = get_opponent_neighbours(grid, player)
    grid_clone = grid.clone()
    good_trap = -sys.maxsize
    good_trap_pos = (-1,-1)
    for i in range(len(opp_neighbours)):
        # print("Checking Current Move:{}".format(opp_neighbours[i]))
        trap_value = minimax_trap(grid_clone, 0, player, opp_neighbours[i], True)
        if good_trap < trap_value:
            good_trap = trap_value
            good_trap_pos = opp_neighbours[i]
    return good_trap_pos

