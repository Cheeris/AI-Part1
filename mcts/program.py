# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent
from .board import MatrixBoard
import numpy as np
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir
from .mcts import MCNode, monte_carlo_tree_search
import numpy as np


# This is the entry point for your game playing agent. Currently the agent
# simply spawns a token at the centre of the board if playing as RED, and
# spreads a token at the centre of the board if playing as BLUE. This is
# intended to serve as an example of how to use the referee API -- obviously
# this is not a valid strategy for actually playing the game!

class Agent:
    def __init__(self, color: PlayerColor, **referee: dict):
        """
        Initialise the agent.s
        """
        self._color = color
        self.board = MatrixBoard(np.zeros([2,7,7], dtype=int), 0, 0, 0)
        self.root = MCNode(MatrixBoard(np.zeros([2,7,7], dtype=int), 0, 0, 0), color)

    def action(self, **referee: dict) -> Action:
        """
        Return the next action to take.
        """
        result, self.root = monte_carlo_tree_search(self.root)
        self.root.parent = None
        return result
        
    def turn(self, color: PlayerColor, action: Action, **referee: dict):
        """
        Update the agent with the last player's action.
        """
        # match action:
        #     case SpawnAction(cell):
        #         print(f"Testing: {color} SPAWN at {cell}")
        #         pass
        #     case SpreadAction(cell, direction):
        #         print(f"Testing: {color} SPREAD from {cell}, {direction}")
        #         pass
            
        self.board = self.board.next_board(action, color)
        
        if color == self._color:
            return
        
        if color != self._color:
        # find the child whose action is the same as the opponent's
            found = False
            for i in range(len(self.root.children)):
                if self.root.children[i].action == action:
                    self.root = self.root.children[i]
                    found = True
                    break
        
            # not found. Create a new node
            if not found:
                new_board = self.root.board.next_board(action, color)
                self.root = MCNode(new_board,
                                color=self._color,
                                action=None,
                                parent=None)
               
