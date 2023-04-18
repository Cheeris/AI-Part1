from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir
    
MAX_TURNS = 7 * 7 * 7
BOARD_N = 7
class MatrixBoard:
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
            
            case SpreadAction(cell, direction):
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
    
    def render(self, use_color: bool=False, use_unicode: bool=False) -> str:
        """
        Return a visualisation of the game board via a multiline string. The
        layout corresponds to the axial coordinate system as described in the
        game specification document.
        """
        def apply_ansi(str, bold=True, color=None):
            # Helper function to apply ANSI color codes
            bold_code = "\033[1m" if bold else ""
            color_code = ""
            if color == "r":
                color_code = "\033[31m"
            if color == "b":
                color_code = "\033[34m"
            return f"{bold_code}{color_code}{str}\033[0m"

        dim = BOARD_N
        output = ""
        for row in range(dim * 2 - 1):
            output += "    " * abs((dim - 1) - row)
            for col in range(dim - abs(row - (dim - 1))):
                # Map row, col to r, q
                r = max((dim - 1) - row, 0) + col
                q = max(row - (dim - 1), 0) + col
                
                if (self.state[0, r, q] != 0) or (self.state[1, r, q] != 0):
                    power = self.state[0, r, q]
                    color = "r" if self.state[0, r, q] != 0 else "b"
                    text = f"{color}{power}".center(4)
                    if use_color:
                        output += apply_ansi(text, color=color, bold=False)
                    else:
                        output += text
                else:
                    output += " .. "
                output += "    "
            output += "\n"
        return output