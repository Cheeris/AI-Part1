from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir
    
MAX_TURNS = 7 * 7 * 7

class Board:
    def __init__(self, state, turn_count, red_power, blue_power) -> None:
        # create an empty board with each cell representing the power of player
        # channel 1: red 
        # channel 2: blue
        self.state = state
        self.turn_count = turn_count
        self.red_power = red_power
        self.blue_power = blue_power
        
    def apply_action(self, action: Action, color: PlayerColor):
        match action:
            case SpawnAction(cell):
                r = cell.r
                q = cell.q
                if (color == PlayerColor.RED):
                    self.state[0][r][q] = 1
                    self.red_power+=1
                else:
                    self.state[1][r][q] = 1
                    self.blue_power+=1
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
                    '''
                    if Curr_player eat opponent's token, the power of the current player add the power
                    of the token eaten
                    '''
                    if (curr_player==0):
                        self.red_power+=self.state[opponent][r][q]
                        self.blue_power-=self.state[opponent][r][q]
                    else:
                        self.red_power-=self.state[opponent][r][q]
                        self.blue_power-=self.state[opponent][r][q]
                    self.state[opponent][r][q] = 0
                    '''if the token is larger than 6, reduce the power of the current player by 7
                    and remove the token
                    '''
                    if self.state[curr_player][r][q] >6:
                        self.state[curr_player][r][q] = 0
                        if (curr_player==0):
                            self.red_power-=7
                        else:
                            self.blue_power-=7
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
    
    def next_board(self, action: Action):
        next = Board(self.state, self.turn_count, self.red_power, self.blue_power)
        next.apply_action(action)
        next.turn_count = self.turn_count + 1
        return next

    
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