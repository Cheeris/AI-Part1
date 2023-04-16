import math
from enum import Enum
from referee.game import Board, Action
# from abc import abstractmethod

class MCState(Enum):
    UNVISITIED = 0;
    UNEXPANDED = 1;
    EXPANDED = 2;

class MCNode:
    def __init__(self, 
                 time_limit: float | None, 
                 space_limit: float | None,
                 board: Board, 
                 action: Action = None,
                 parent = None,
                 ) -> None:
        self.playouts = 0
        self.wins = 0
        self.state = MCState.UNVISITIED
        self.time_limit = time_limit
        self.space_limit = space_limit
        self.board = board
        self.parent = parent
        self.children = []
        self.action = action
    
    def is_over(self):
        return self.board.game_over()
        
    def select(self):
        # select the child with the highest UCB score
        best_score = -math.inf 
        best_child = None
        c = 1   # larger C, more adventurous
        for child in self.children:
            score = child.wins / child.playouts \
                + c * math.sqrt(2 * math.log(self.playouts) / child.playouts)
            if score > best_score: 
                best_score = score 
                best_child = child
        return best_child

    
    def simulate(self):
        pass
    
    def expand(self):
        pass
    
    def backpropagate(self, result):
        self.playouts += 1 
        self.wins += result 
        if self.parent is not None:
            self.parent.backpropagate(result)

            
def monte_carlo_tree_search(time_limit: float, space_limit: float, board: Board): 
    root = MCNode(time_limit=time_limit, space_limit=space_limit, board=board)
    num_iterations = 1000
    for i in range(num_iterations): 
        # Selection
        current_node = root
        while len(current_node.children) != 0:
            current_node = current_node.select()
            
        # Expansion
        if not current_node.is_over():
            current_node = current_node.expand()
            
        # Simulation
        playout_result = current_node.simulate()
        
        # Backpropagation 
        current_node.backpropagate(playout_result)
    
    
    best_child = root.select()
    return best_child.action