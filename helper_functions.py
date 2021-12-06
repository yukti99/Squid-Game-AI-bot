from Grid import Grid
from Utils import *


def get_opponent_position(grid: Grid, player_num: int):
    opponent_no = 3 - player_num
    print("opponent_no:{}".format(opponent_no))
    grid.print_grid()
    opponent_pos = grid.find(opponent_no)

    return opponent_pos

def get_opponent_neighbours(grid: Grid, player_num: int):
    opponent_pos = get_opponent_position(grid=grid, player_num=player_num)
    opponent_neighbours = grid.get_neighbors(opponent_pos)
    return opponent_neighbours

def trap_heuristic(player_num: int, grid: Grid):
    opponent_neighbours = get_opponent_neighbours(grid,player_num=player_num)
    moves_dict = {}
    grid_clone = grid.clone()
    opponent_pos = get_opponent_position(grid_clone, player_num)
    for i in range(len(opponent_neighbours)):
        if grid_clone.getCellValue(opponent_neighbours[i]) == 0:
            grid_clone.trap(opponent_neighbours[i])
            available_opponent_moves = grid_clone.get_neighbors(opponent_pos, only_available=True)
            moves_dict[opponent_neighbours[i]] = len(available_opponent_moves)
            grid_clone.setCellValue(opponent_neighbours[i], 0)
    print(moves_dict)
    good_trap = min(moves_dict, key=moves_dict.get)
    return good_trap


def board_value(grid, my_position, opponent_pos):
    distance = manhattan_distance(my_position, opponent_pos)
    no_neighbours = len(grid.get_neighbors(my_position))
    return no_neighbours + distance


def move_heuristic(player_num: int, position, grid: Grid):
    opponent_pos = get_opponent_position(grid=grid, player_num=player_num)
    grid_clone = grid.clone()
    my_new_available_moves = grid_clone.get_neighbors(position, only_available=True)
    moves_dict = {}
    for i in range(len(my_new_available_moves)):
        moves_dict[my_new_available_moves[i]] = board_value(grid_clone, my_new_available_moves[i], opponent_pos)
    good_move = max(moves_dict, key=moves_dict.get)
    return good_move