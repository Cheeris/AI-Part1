import math
# import board
import random
from enum import Enum
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir
from agent.board import MatrixBoard
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
                 action: Action = None,
                 parent = None,
                 ) -> None:
        self.playouts = 0
        self.wins = 0
        self.state = MCState.UNVISITIED
        self.board = board
        self.parent = parent
        self.children = []
        self.all_actions = []
        self.action = action
        self.color = color
        # self.ubc
    
    def is_over(self) -> bool:
        return self.board.game_over()
    
    def winner_color(self) -> PlayerColor | None: 
        return self.board.winner_color()
    
    def ucb(self, c):
        '''
        Calculate the UCB score.
        '''
        if self.playouts == 0:
            return math.inf
        return self.wins / self.playouts \
                + c * math.sqrt(2 * math.log(self.playouts) / self.playouts)
        
    def select(self):
        '''
        Select the child with the highest UCB score.
        '''
        # print("--Select--")
        best_score = -math.inf 
        best_child = None
        c = 1   # larger C, more adventurous
        for child in self.children:
            score = child.ucb(c)
            if score > best_score: 
                best_score = score 
                best_child = child
        
        return best_child
    
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
        random.seed(SEED_VALUE)
        action = self.all_actions[random.randint(0, len(self.all_actions) - 1)]
        next_board = self.board.next_board(action, self.color)
        child = MCNode(next_board, 
                       PlayerColor.RED if self.color == PlayerColor.BLUE \
                        else PlayerColor.BLUE, 
                        action, 
                        self)
        self.children.append(child)
        self.all_actions.remove(action)
        
        if len(self.all_actions) == 0 and len(self.children) != 0 and not self.is_over():
            self.state = MCState.EXPANDED
            
        return self.select()
    
    def backpropagate(self, winColor: PlayerColor):
        '''
        Use the outcome from the playout to  update the statistics of each node 
        from the newly added node back up to the route.
        '''
        # print("--backpropagate--")
        self.playouts += 1 
        if (self.color == winColor):
            self.wins += 1
        if self.parent is not None:
            self.parent.backpropagate(winColor)
        
            
def monte_carlo_tree_search(root: MCNode) -> tuple[Action, MCNode]: 
    # root = MCNode(board=board, color=playerColor)
    '''
    Perform Monte-Carlo Tree Search ALgorithm. 
    '''
    ### TODO: how to stop when the program reaches time/space limit
    num_iterations = 6
    for i in range(num_iterations): 
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
        result = current_node.board.playout(current_node.color)
        # result = current_node.board.playout_heuristic(current_node.color)
        
        # Backpropagation 
        current_node.backpropagate(result)
        
        current_node = root
    
    best_child = root.select()
    
    return best_child.action, best_child