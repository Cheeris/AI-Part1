# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent
from agent.board import MatrixBoard
import numpy as np
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir
# from agent.monte_carlo import MCNode, monte_carlo_tree_search
from agent.random_action import random_action
from agent.mcts_alphazero import MCNode, monte_carlo_tree_search

LOG_PATH = '/Users/clarec/Desktop/COMP30024-AI-ProjectB/agent/log/mcts_random_1000_2'

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
        with open(LOG_PATH+'_state.csv', mode='w') as file:
            pass
                # np.savetxt(file, self.root.board.state.reshape([1,2*7*7]), delimiter=',')
    


    def action(self, **referee: dict) -> Action:
        """
        Return the next action to take.
        """
        # if self._color == PlayerColor.RED:
        #     # with open(LOG_PATH+'_state.csv', mode='a') as file:
        #     #     np.savetxt(file, self.root.board.state.reshape([1,2*7*7]), delimiter=',')
            
        #     result, self.root = monte_carlo_tree_search(self.root)
        #     self.root.parent = None
        #     # with open(LOG_PATH+'_state.csv', mode='a') as file:
        #     #     np.savetxt(file, self.root.board.state.reshape([1,2*7*7]), delimiter=',')
            
        # #     # Open the file in append mode
        # #     # with open(LOG_PATH+'_action.csv', mode='a') as file:
        # #     #     np.savetxt(file, convert_action_to_array(result), delimiter=',')
        # #     # with open(LOG_PATH+'_reward.csv', mode='a') as file:
        # #     #     reward = self.get_reward()
        # #     #     np.savetxt(file, np.array([reward], dtype=int).reshape([1, -1]), delimiter=',')
        # else:
        result = random_action(self.board, self._color)
            # Open the file in append mode
            # with open(LOG_PATH+'_state.csv', mode='a') as file:
            #     np.savetxt(file, self.root.board.state.reshape([1,2*7*7]), delimiter=',')
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
        with open(LOG_PATH+'_state.csv', mode='a') as file:
                np.savetxt(file, self.root.board.state.reshape([1,2*7*7]), delimiter=',')
        
        # TODO: 删掉random-action agent的时候删掉这一行
        # if self._color == PlayerColor.BLUE:
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
        #                         parent=None)
            
        # with open(LOG_PATH+'_state.csv', mode='a') as file:
        #     np.savetxt(file, self.root.board.state.reshape([1,-1]), delimiter=',')
        # with open(LOG_PATH+'_action.csv', mode='a') as file:
        #     np.savetxt(file, convert_action_to_array(action), delimiter=',')
        # with open(LOG_PATH+'_reward.csv', mode='a') as file:
        #     reward = self.get_reward()
        #     np.savetxt(file, np.array([reward], dtype=int).reshape([1, -1]), delimiter=',')
        
    def get_reward(self) -> int:
        return (-1 if self._color == PlayerColor.BLUE else 1) * (self.board.red_power - self.board.blue_power)
        
def convert_action_to_array(action: Action):
    match action:
        case SpawnAction(cell):
            return np.array([cell.r, cell.q, 0, 0], dtype=int).reshape([1,-1])
            # pass
        case SpreadAction(cell, direction):
            return np.array([cell.r, cell.q, direction.r, direction.q], dtype=int).reshape([1,-1])
            # pass
