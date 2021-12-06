import numpy as np
import random
import time
import sys
import os
from BaseAI import BaseAI
from Grid import Grid
from Utils import *
import sys
import os
from helper_functions import *

# setting path to parent directory
sys.path.append(os.getcwd())


# TO BE IMPLEMENTED
#
class PlayerAI(BaseAI):

    def __init__(self) -> None:
        # You may choose to add attributes to your player - up to you!
        super().__init__()
        self.pos = None
        self.player_num = None

    def getPosition(self):
        return self.pos

    def setPosition(self, new_position):
        self.pos = new_position

    def getPlayerNum(self):
        return self.player_num

    def setPlayerNum(self, num):
        self.player_num = num

    def getMove(self, grid: Grid) -> tuple:
        """
        YOUR CODE GOES HERE

        The function should return a tuple of (x,y) coordinates to which the player moves.

        It should be the result of the ExpectiMinimax algorithm, maximizing over the Opponent's *Trap* actions,
        taking into account the probabilities of them landing in the positions you believe they'd throw to.

        Note that you are not required to account for the probabilities of it landing in a different cell.

        You may adjust the input variables as you wish (though it is not necessary). Output has to be (x,y) coordinates.

        """

        # available_moves = grid.get_neighbors(self.pos, only_available=True)
        # new_pos = random.choice(available_moves) if available_moves else None
        new_pos = move_heuristic(player_num=self.player_num, position=self.pos, grid=grid)
        return new_pos

    def getTrap(self, grid: Grid) -> tuple:
        """
        YOUR CODE GOES HERE

        The function should return a tuple of (x,y) coordinates to which the player *WANTS* to throw the trap.

        It should be the result of the ExpectiMinimax algorithm, maximizing over the Opponent's *Move* actions,
        taking into account the probabilities of it landing in the positions you want.

        Note that you are not required to account for the probabilities of it landing in a different cell.

        You may adjust the input variables as you wish (though it is not necessary). Output has to be (x,y) coordinates.

        """
        # Random Traps:
        # available_cells = grid.getAvailableCells()
        trap = trap_heuristic(player_num=self.player_num, grid=grid)
        return trap
