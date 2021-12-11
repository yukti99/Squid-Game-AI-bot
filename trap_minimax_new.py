from Grid import Grid
from Utils import *
import sys
import random
from helper_functions import *
ALPHA = -sys.maxsize
BETA = sys.maxsize
MAX_DEPTH = 2

# f = open("test.txt", 'w')



def hardcode(grid, player):
    corners = [(1, 1), (1, 5), (5, 1), (5, 5)]
    opponent_pos = get_opponent_position(grid, player)
    x, y = opponent_pos
    dictionary = {}
    for i in range(4):
        dictionary[corners[i]] = manhattan_distance(corners[i], opponent_pos)

    best_corner = min(dictionary, key=dictionary.get)
    print("best_corner:{}".format(best_corner))
    weights_list = [7, 6, 5, 4, 3, 2, 1]

    d = [(max(x - 1, 0), min(y + 1, 6)), (x, min(y + 1, 6)), (max(x - 1, 0), y), (max(x - 1, 0), max(y - 1, 0)),
         (min(x + 1, 6), min(y + 1, 6)), (min(x + 1, 6), y), (min(x + 1, 6), y)]

    # Right-up, right, right-down, up, up-left, left, down
    if best_corner == (5, 1):
        d = [(max(x - 1, 0), min(y + 1, 6)), (x, min(y + 1, 6)), (max(x - 1, 0), y), (max(x - 1, 0), max(y - 1, 0)),
             (min(x + 1, 6), min(y + 1, 6)), (min(x + 1, 6), y), (min(x + 1, 6), y)]

    # Bottom Right, Bottom, Bottom Left, Right, Top Right, Top, Left, Top Left
    elif best_corner == (1, 1):
        d = [(min(x + 1, 6), min(y + 1, 6)), (min(x+1, 6), y), (min(x + 1, 6), max(y-1, 0)), (x, min(y + 1, 6)),
             (max(x - 1, 0), min(y + 1, 6)), (min(x - 1, 6), y), (max(x - 1, 0), min(y-1, 0))]

    # #Top Left, Left, Top, Bottom Left, Top Right, Right, Bottom Right
    elif best_corner == (5, 5):
        d = [(max(x - 1, 0), max(y - 1, 0)), (max(x-1, 0), y), (x, max(y-1, 0)), (min(x + 1, 6), max(y - 1, 0)),
             (max(x - 1, 0), min(y + 1, 6)), (x, min(y+1, 6)), (min(x + 1, 6), min(y+1, 6))]
    # else:
    #     d = [(max(x - 1, 0), min(y + 1, 6)), (x, min(y + 1, 6)), (max(x - 1, 0), y), (max(x - 1, 0), max(y - 1, 0)),
    #          (min(x + 1, 6), min(y + 1, 6)), (min(x + 1, 6), y), (min(x + 1, 6), y)]
    max_pos = []
    for i in range(len(d)):
        if grid.getCellValue(d[i]) == 0:
            max_pos.append(d[i])
    return max_pos


def trap_h_new(grid, player):





    opponent_neighbors = get_opponent_neighbours(grid, player)
    corner_distance_dict = {}
    for i in range(len(opponent_neighbors)):
        corner_distance_dict[opponent_neighbors[i]] = manhattan_distance(best_corner, opponent_neighbors[i])

    return max(corner_distance_dict, key=corner_distance_dict.get)


def diagonal(pos1, pos2):
    (x1,y1) = pos1
    (x2, y2) = pos2
    if x1 != x2 and y1 != y2:
        return True
    else:
        return False


def trap_h(player_num: int, grid: Grid, depth):
    # global f
    opponent_neighbours = get_opponent_neighbours(grid, player_num=player_num)
    opponent_position = get_opponent_position(grid, player_num)

    board_value_dict = {}
    grid_clone = grid.clone()
    player_pos = grid.find(player_num)

    # if depth == 0 or depth == 1:
    #     slice_no = int(len(opponent_neighbours)/float(1.5))
    # elif len(opponent_neighbours) > 5:
    #     slice_no = int(len(opponent_neighbours) * (1 - depth/10))
    # else:
    #     slice_no = len(opponent_neighbours)
    for i in range(len(opponent_neighbours)):
        if grid_clone.getCellValue(opponent_neighbours[i]) == 0:
            available_cells = len(grid.get_neighbors(opponent_neighbours[i], only_available=True))
            board_v = available_cells * board_value(grid_clone, opponent_neighbours[i], player_pos)
            if diagonal(opponent_position, opponent_neighbours[i]):
                board_v = board_v * 1.5
            # print("Position: {} and board value:{}".format(opponent_neighbours[i], board_v))
            board_value_dict[opponent_neighbours[i]] = board_v
    max_position = list(sorted(board_value_dict, key=board_value_dict.get,reverse=True))
    # max_position = max_position[:slice_no]
    # f.write(str(len(max_position)/len(opponent_neighbours)))
    # f.write("\n")
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
def minimax_trap(grid: Grid, depth, player, isMax, alpha, beta, current_trap: tuple):
    '''
    BASE CASES
    '''
    # print("Increasing Depth by 1 :{}".format(depth))
    opp_neighbours = get_opponent_neighbours(grid, player)
    player_neighbours = grid.get_neighbors(grid.find(player), only_available=True)

    if depth > MAX_DEPTH:
        # print("Terminal State reached!!!!")
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

    # good_traps_against_opponent = trap_h(player, grid, depth)
    good_traps_against_opponent = hardcode(grid,player)

    if isMax == 1:
        # we put trap
        best_value = -sys.maxsize
        counter = 0
        for i in good_traps_against_opponent:

            # hit_probability = 1 - 0.05 * (manhattan_distance(grid.find(player), i) - 1)
            # all_possible_positions = grid.get_neighbors(i, only_available=True)
            # all_possible_positions.append(i)
            # missing_probability = ((1 - hit_probability) / len(grid.get_neighbors(i)))
            # expectation = 0
            #
            # for j in range(len(all_possible_positions)):
            #     if i == all_possible_positions[j]:
            # grid.setCellValue(i, -1)
            expectation = (len(good_traps_against_opponent) - counter) * minimax_trap(grid, depth, player, 2, alpha, beta, i)
            # grid.setCellValue(i, 0)
                # else:
                #     expectation = expectation + missing_probability * best_value

            best_value = max(best_value, expectation)
            alpha = max(alpha, best_value)
            if beta <= alpha:
                # print("Tree Pruning in MAX TRAP!")
                #print("BREAK!!!")
                break
            counter = counter + 1
        return best_value

    elif isMax == 0:
        # opponent moves
        best_value = sys.maxsize
        previous_player_position = grid.find(3-player)
        for j in good_traps_against_opponent:
            grid.move(j, 3-player)
            best_value = min(best_value, minimax_trap(grid, depth+1, player, 1, alpha, beta, (0, 0)))
            beta = min(beta, best_value)
            grid.move(previous_player_position, 3-player)
            if beta <= alpha:
                # print("Tree Pruning in MIN TRAP!")
                break
        return best_value

    else:
        # chance node
        best_value = -sys.maxsize
        i = current_trap
        hit_probability = 1 - 0.05 * (manhattan_distance(grid.find(player), i) - 1)
        missing_probability = ((1 - hit_probability) / len(grid.get_neighbors(i)))
        expectation = 0
        all_possible_positions = grid.get_neighbors(i, only_available=True)
        # all_possible_positions = all_possible_positions[:something(depth)]
        all_possible_positions.append(i)
        for j in range(len(all_possible_positions)):
            grid.setCellValue(all_possible_positions[j], -1)

            if i == all_possible_positions[j]:
                best_value = minimax_trap(grid, depth + 1, player, 0, alpha, beta, (0,0))
                expectation = expectation + hit_probability * best_value
            else:
                best_value = minimax_trap(grid, depth + 1, player, 0, alpha, beta, (0, 0))
                expectation = expectation + missing_probability * best_value

            grid.setCellValue(all_possible_positions[j], 0)
            best_value = max(best_value, expectation)
            alpha = max(alpha, best_value)
            if beta <= alpha:
                # print("Tree Pruning in CHANCE MIN TRAP!")
                break
        # alpha = max(alpha, best_value)
        # if beta <= alpha:
        #     print("BREAK!!!")
        #     break
        return expectation


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
            trap_value = minimax_trap(grid_clone, 0, player, 1, ALPHA, BETA, (0,0))
            grid_clone.setCellValue(opp_neighbours[i], 0)
            # print("\n Trap value obtained for -", opp_neighbours[i], " is  = ", trap_value)
            if good_trap < trap_value:
                good_trap = trap_value
                good_trap_pos = opp_neighbours[i]
        return good_trap_pos

