import math
from enum import Enum
from referee.game import Board, Action
from referee.agent import PlayerColor
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
                 color: PlayerColor,
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
        self.color = color
    
    def is_over(self) -> bool:
        return self.board.game_over()
    
    def winner_color(self) -> PlayerColor | None:
        return self.board.winner_color()
        
    def select(self):
        '''
        Select the child with the highest UCB score.
        '''
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

    
    def simulate(self) -> PlayerColor:
        '''
        Perform a playout from the newly added node to a terminal  state, 
        but dont add the moves/states explored in the playout to the search tree
        Return the winner's color.
        '''
        if self.is_over():
            return self.winner_color()
    
    def expand(self):
        '''
        Expand the node by adding to the tree a single new child from that node.
        '''
        pass
    
    def backpropagate(self, winColor: PlayerColor):
        '''
        Use the outcome from the playout to  update the statistics of each node 
        from the newly added node back up to the route.
        '''
        self.playouts += 1 
        if (self.color == winColor):
            self.wins += 1
        if self.parent is not None:
            self.parent.backpropagate(winColor)

            
def monte_carlo_tree_search(time_limit: float, space_limit: float, board: Board): 
    root = MCNode(time_limit=time_limit, space_limit=space_limit, 
                  board=board, color=PlayerColor.RED)
    
    ### TODO: how to stop when the program reaches time/space limit
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
        result = current_node.simulate()
        
        # Backpropagation 
        current_node.backpropagate(result)
    
    
    best_child = root.select()
    return best_child.action