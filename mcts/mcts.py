import math
import random
from enum import Enum
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir
from .board import MatrixBoard
import numpy as np

class MCState(Enum):
    UNVISITIED = 0;
    UNEXPANDED = 1;
    EXPANDED = 2;

class MCNode:
    def __init__(self, 
                 board: MatrixBoard, 
                 color: PlayerColor,
                 action: Action = None,
                 parent = None
                 ) -> None:
        self.playouts = 0
        self.wins = 0
        self.ucb = 0
        self.state = MCState.UNVISITIED
        self.board = board
        self.parent = parent
        self.children = []
        self.all_actions = []
        self.action = action
        self.color = color
    
    def is_over(self) -> bool:
        return self.board.game_over()
    
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
        best_score = -math.inf 
        best_child = None

        c = 0
        for child in self.children:
            child.update_ucb(c)
            score = child.ucb
            if score > best_score: 
                best_score = score 
                best_child = child
        
        return best_child

    def expand(self):
        '''
        Expand the node by adding to the tree a single new child from that node.
        '''
        # if haven't get all the valid actions
        if self.state == MCState.UNVISITIED:
            self.all_actions = self.board.get_valid_actions(self.color)
            self.state = MCState.UNEXPANDED if len(self.all_actions) != 0 else MCState.EXPANDED
            
        # randomly pick one action
        action = random.choice(self.all_actions)
        next_board = self.board.next_board(action, self.color)
        child = MCNode(next_board, 
                       PlayerColor.RED if self.color == PlayerColor.BLUE \
                        else PlayerColor.BLUE, 
                        action=action, 
                        parent=self)
        self.children.append(child)
        self.all_actions.remove(action)
        
        if len(self.all_actions) == 0 and len(self.children) != 0 and not self.is_over():
            self.state = MCState.EXPANDED
            
        return self.select()
    
    def backpropagate(self, result):
        '''
        Use the outcome from the playout to  update the statistics of each node 
        from the newly added node back up to the route.
        '''
        self.playouts += 1 
        if result == self.color:
            self.wins += 1
        elif result == self.color.opponent:
            self.wins -= 1
        
        if self.parent is not None:
            self.parent.backpropagate(result)
    
    def playout_eval(self):
        parent = self.parent
        result = (self.board.red_power - self.board.blue_power) 
            
        if parent == None:
            return result 
        
        if self.color == PlayerColor.RED:
            result += self.board.red_power - parent.board.red_power
        else:
            result += self.board.blue_power - parent.board.blue_power
        
        return result
            
def monte_carlo_tree_search(root: MCNode) -> tuple[Action, MCNode]: 
    '''
    Perform Monte-Carlo Tree Search ALgorithm. 
    '''
    num_iterations = 1000
    for _ in range(num_iterations): 
        # Selection
        current_node = root
        while current_node.state == MCState.EXPANDED:
            current_node = current_node.select()
            
        # Expand one node if node's state is UNVISITED or UNEXPANDED
        if not current_node.is_over():
            current_node = current_node.expand()  
            
        # Simulation
        result = current_node.board.playout(current_node.color)
        
        # Backpropagation 
        current_node.backpropagate(result)
        
        current_node = root
    
    best_child = root.select()
    
    return best_child.action, best_child