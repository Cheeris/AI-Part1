from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir
    
MAX_TURNS = 7 * 7 * 7

class Board:
    def __init__(self, state) -> None:
        # create an empty board with each cell representing the power of player
        # channel 1: red 
        # channel 2: blue
        self.state = state
        self.turn_count = 0
        self.red_power = 0
        self.blue_power = 0
        
    def apply_action(self, action: Action, color: PlayerColor):
        match action:
            case SpawnAction(cell):
                r = cell.r
                q = cell.q
                if (color == PlayerColor.RED):
                    self.state[0][r][q] = 1
                else:
                    self.state[1][r][q] = 1
                pass
            case SpreadAction(cell,direction):
                r = cell.r
                q = cell.q
                dr = direction.value.r
                dq = direction.value.q
                if (color == PlayerColor.RED):
                    curr_player = 0
                    opponent = 1
                else:
                    curr_player = 1
                    opponent = 0
                power = self.state[curr_player][r][q]
                self.state[curr_player][r][q] = 0 #remove the token
                #Spread
                for i in range(power):
                    r,q = self.update_r_q(r,q,dr,dq)
                    self.state[curr_player][r][q] = self.state[opponent][r][q] + 1
                    self.state[opponent][r][q] = 0
                    if self.state[curr_player][r][q] >6:
                        self.state[curr_player][r][q] = 0
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
    
        # Function to update the r,q if they reach -1 or 7
    def update_r_q(r, q, dr, dq) -> tuple:
        """
        Update the coordinates if the token reaches the edge.
        """
        r += dr
        q += dq
        if r > 6:
            r = 0
        if r < 0:
            r = 6
        if q > 6:
            q = 0
        if q < 0:
            q = 6
        return (r, q)