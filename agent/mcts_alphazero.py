import math
import random
from enum import Enum
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir
from agent.board import MatrixBoard
from agent.CNNModel import CNNModel, convert_to_state_input
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

# from abc import abstractmethod

SEED_VALUE = 100

class MCState(Enum):
    UNVISITIED = 0;
    UNEXPANDED = 1;
    EXPANDED = 2;

class MCNode:
    def __init__(self, 
                 board: MatrixBoard, 
                 color: PlayerColor,
                 model: CNNModel,
                 action: Action = None,
                 parent = None
                 ) -> None:
        self.playouts = 0
        self.wins = 0
        self.q_value = 0
        self.ucb = 0
        self.state = MCState.UNVISITIED
        self.board = board
        self.parent = parent
        self.children = []
        self.all_actions = []
        self.action = action
        self.color = color
        self.model = model
    
    def is_over(self) -> bool:
        return self.board.game_over()
    
    # def winner_color(self) -> int: 
    #     winner = self.board.winner_color()
    #     if winner == self.color:
    #         return 1
    #     elif winner == None:
    #         return 0
    #     return -1
    
    def update_ucb(self, c):
        '''
        Calculate the UCB score.
        '''
        if self.playouts == 0:
            self.ucb = math.inf
        else:
            self.ucb = self.wins / self.playouts \
                + c * math.sqrt(math.log(self.parent.playouts) / self.playouts)
        return 
    
    def select(self):
        '''
        Select the child with the highest UCB score.
        '''
        # print("--Select--")
        best_score = -math.inf 
        best_child = None
        # if self.board.turn_count < 200 or self.board.red_power < self.board.blue_power:
        #     c = 3   # larger C, more adventurous
        # else:
        #     c = 1
        # c = 2
        for child in self.children:
            # child.update_ucb(c)
            # score = child.ucb + child.q_value
            # score = child.ucb
            score = child.q_value
            if score > best_score: 
                best_score = score 
                best_child = child
        
        if best_child != None:
            return best_child
        elif len(self.children) != 0:
            print(len(self.children))
            return self.children[0]
        else:
            print("Wrong")

    
    # expand the node of MCTS
    def expand(self):
        '''
        Expand the node by adding to the tree a single new child from that node.
        '''
        # print("--Expand--")
        # if haven't get all the valid actions
        # if len(self.all_actions) == 0 and len(self.children) == 0:
        if self.state == MCState.UNVISITIED:
            self.all_actions = self.board.get_valid_actions(self.color)
            self.state = MCState.UNEXPANDED if len(self.all_actions) != 0 else MCState.EXPANDED
            
        # randomly pick one action
        # random.seed(SEED_VALUE)
        action = random.choice(self.all_actions)
        # action = self.all_actions[random.randint(0, len(self.all_actions) - 1)]
        next_board = self.board.next_board(action, self.color)
        child = MCNode(next_board, 
                       PlayerColor.RED if self.color == PlayerColor.BLUE \
                        else PlayerColor.BLUE, 
                        action=action, 
                        parent=self,
                        model=self.model)
        self.children.append(child)
        self.all_actions.remove(action)
        
        if len(self.all_actions) == 0 and len(self.children) != 0 and not self.is_over():
            self.state = MCState.EXPANDED
            
        return self.select()
    
    def backpropagate(self, win_score):
        '''
        Use the outcome from the playout to  update the statistics of each node 
        from the newly added node back up to the route.
        '''
        # print("--backpropagate--")
        self.playouts += 1 
        
        if type(win_score) == PlayerColor:
            if self.color == win_score:
                self.wins += 1
                self.q_value += 1
            elif win_score != None:  # lose
                self.q_value -= 1
                self.wins -= 1
        else:
            if self.color == PlayerColor.RED:
                self.q_value += win_score
            else:
                self.q_value -= win_score
        if self.parent is not None:
            self.parent.backpropagate(win_score)

    def playout_model(self):
        tmp = self.board.state
        tmp = convert_to_state_input(tmp).reshape([1,2,7,7])
        tmp_t = torch.from_numpy(tmp).float()
        # print(self.model)
        self.model.eval()
        with torch.no_grad():
            test_out = self.model(tmp_t).numpy()
        return test_out[0][0]
            
def monte_carlo_tree_search(root: MCNode) -> tuple[Action, MCNode]: 
    # root = MCNode(board=board, color=playerColor)
    '''
    Perform Monte-Carlo Tree Search ALgorithm. 
    '''
    ### TODO: how to stop when the program reaches time/space limit
    num_iterations = 50000
    for _ in range(num_iterations): 
        # print("----SEARCH: %d----" %i)
        # Selection
        current_node = root
        # while len(current_node.children) != 0: # find the leaf node
        #     current_node = current_node.select()
        while current_node.state == MCState.EXPANDED:
            current_node = current_node.select()
            
        # Expand one node if node's state is UNVISITED or UNEXPANDED
        if not current_node.is_over():
            current_node = current_node.expand()  
            
        # Simulation
        # result = current_node.board.playout(current_node.color)
        result = current_node.playout_model()
        # result = current_node.board.playout_heuristic(current_node.color)
        
        # Backpropagation 
        current_node.backpropagate(result)
        
        current_node = root
    
    best_child = root.select()
    # print(root.board.turn_count)
    # if (best_child == None):
    #     print(root.all_actions)
    #     print(root.action)
    #     print(root.children)
    #     print(root.playouts)
    #     print(root.is_over())
    #     print(root.board.turn_count)
    
    return best_child.action, best_child