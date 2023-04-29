# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent
from agent.board import MatrixBoard
import numpy as np
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir
from alpha_beta.alpha_beta import alpha_beta, ABNode, eval, minimax_with_alpha_beta
import random
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from agent.CNNModel import CNNModel
from agent.random_action import random_action
from agent.mcts_alphazero import MCNode, monte_carlo_tree_search
# This is the entry point for your game playing agent. Currently the agent
# simply spawns a token at the centre of the board if playing as RED, and
# spreads a token at the centre of the board if playing as BLUE. This is
# intended to serve as an example of how to use the referee API -- obviously
# this is not a valid strategy for actually playing the game!
LOG_PATH = '/Users/clarec/Desktop/COMP30024-AI-ProjectB/alpha_beta/log/aba_2'

MODEL_PATH = '/Users/clarec/Desktop/COMP30024-AI-ProjectB/rr_e100.pth'
class Agent:
    def __init__(self, color: PlayerColor, **referee: dict):
        """
        Initialise the agent.
        """
        self._color = color
        self.board = MatrixBoard(np.zeros([2,7,7], dtype=int), 0, 0, 0)
        self.model = CNNModel()
        self.model.load_state_dict(torch.load(MODEL_PATH))
        self.root = MCNode(MatrixBoard(np.zeros([2,7,7], dtype=int), 0, 0, 0), color, model=self.model)
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
            # result, self.root = monte_carlo_tree_search(self.root)
            # self.root.parent = None
            # return result
            root = ABNode(self.board, self._color)
            root.add_children()
            child_len = len(root.children)
            return minimax_with_alpha_beta(root, self._color,3)
            # return random_action(self.board, self._color)
        else:
            # result, self.root = monte_carlo_tree_search(self.root)
            # self.root.parent = None
            # return result
            # return random_action(self.board, self._color)
            root = ABNode(self.board, self._color)
            root.add_children()
            child_len = len(root.children)
            return minimax_with_alpha_beta(root, self._color,3)
            
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
        
        if self._color == PlayerColor.RED:
            with open(LOG_PATH+'.csv', mode='a') as file:
                np.savetxt(file, self.board.state.reshape([1,2*7*7]), delimiter=',')
        
        # if self._color == PlayerColor.RED:
        #     return
        
        # if color == self._color:
        #     return
        
        # if color != self._color:
        # # find the child whose action is the same as the opponent's
        #     found = False
        #     for i in range(len(self.root.children)):
        #         if self.root.children[i].action == action:
        #             self.root = self.root.children[i]
        #             found = True
        #             break
        
        #     # not found. Create a new node
        #     if not found:
        #         new_board = self.root.board.next_board(action, color)
        #         self.root = MCNode(new_board,
        #                         color=self._color,
        #                         action=None,
        #                         parent=None,
        #                         model=self.model)
        
