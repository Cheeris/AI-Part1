# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent
from agent.board import MatrixBoard
import numpy as np
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir
from agent.monte_carlo import MCNode, monte_carlo_tree_search
from agent.random_action import random_action

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
        match color:
            case PlayerColor.RED:
                print("Testing: I am playing as red")
            case PlayerColor.BLUE:
                print("Testing: I am playing as blue")
        

    def action(self, **referee: dict) -> Action:
        """
        Return the next action to take.
        """
        if self._color == PlayerColor.RED:
            result, self.root = monte_carlo_tree_search(self.root)
            
        else:
            result = random_action(self.board, self._color)
        return result
        # match self._color:
        #     case PlayerColor.RED:
        #         return SpawnAction(HexPos(3, 3))
        #     case PlayerColor.BLUE:
        #         # This is going to be invalid... BLUE never spawned!
        #         return SpreadAction(HexPos(3, 3), HexDir.Up)


    def turn(self, color: PlayerColor, action: Action, **referee: dict):
        """
        Update the agent with the last player's action.
        """
        match action:
            case SpawnAction(cell):
                print(f"Testing: {color} SPAWN at {cell}")
                pass
            case SpreadAction(cell, direction):
                print(f"Testing: {color} SPREAD from {cell}, {direction}")
                pass
        self.board = self.board.next_board(action, color)
        
        if self._color == PlayerColor.BLUE:
            return
        
        if color == self._color:
            return
        
        if color != self._color:
        # find the child whose action is the same as the opponent's
            for i in range(len(self.root.children)):
                if self.root.children[i].action == action:
                    self.root = self.root.children[i]
                    return 
        
            # not found. Create a new node
            self.root = MCNode(self.root.board.next_board(action, color), 
                            color=self._color,
                            action=action,
                            parent=self.root)
        
        
        
