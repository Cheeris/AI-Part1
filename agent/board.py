import numpy as np
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir
    
MAX_TURNS = 7 * 7 * 7

class Board:
    def __init__(self) -> None:
        # create an empty board with each cell representing the power of player
        # channel 1: red 
        # channel 2: blue
        self.state = np.zeros([2,7,7])   
        self.turn_count = 0
        self.red_power = 0
        self.blue_power = 0
        
    def apply_action(self, action: Action):
        pass
    
    
    def game_over(self) -> bool:
        """
        True if the game is over.
        """
        if self.turn_count < 2: 
            return False
        
        return any([
            self.turn_count >= MAX_TURNS,
            self.red_power == 0,
            self.blue_power == 0
        ])