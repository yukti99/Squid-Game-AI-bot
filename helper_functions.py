from Grid import Grid
from Utils import *


def trap_heuristic(player_num: int, grid: Grid):
    opponent_no = 3 - player_num
    opponent_pos = grid.find(opponent_no)
    opponent_neighbours = grid.get_neighbors(opponent_pos)
    moves_dict = {}
    grid_clone = grid.clone()
    for i in range(len(opponent_neighbours)):
        if grid_clone.getCellValue(opponent_neighbours[i]) == 0:
            grid_clone.trap(opponent_neighbours[i])
            available_opponent_moves = grid_clone.get_neighbors(opponent_pos, only_available=True)
            moves_dict[opponent_neighbours[i]] = len(available_opponent_moves)
            grid_clone.setCellValue(opponent_neighbours[i], 0)
    print(moves_dict)
    good_trap = min(moves_dict, key=moves_dict.get)
    return good_trap


def move_heuristic(player_num: int, position, grid: Grid):
    opponent_no = 3 - player_num
    opponent_pos = grid.find(opponent_no)
    grid_clone = grid.clone()
    my_new_available_moves = grid_clone.get_neighbors(position, only_available=True)
    moves_dict = {}
    for i in range(len(my_new_available_moves)):
        distance = manhattan_distance(my_new_available_moves[i], opponent_pos)
        no_neighbours = len(grid_clone.get_neighbors(my_new_available_moves[i]))
        moves_dict[my_new_available_moves[i]] = distance + no_neighbours
    good_move = max(moves_dict, key=moves_dict.get)
    return good_move