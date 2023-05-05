from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir
import random

MAX_TURNS = 7 * 7 * 7
BOARD_N = 7
DRAW =0
RED_WIN=1
BLUE_WIN=2
WIN_POWER_DIFF  = 2

class MatrixBoard:
    def __init__(self, state, turn_count, red_power, blue_power) -> None:
        # create an empty board with each cell representing the power of player
        # channel 1: red 
        # channel 2: blue
        self.state = state.copy()
        self.turn_count = turn_count
        self.red_power = red_power
        self.blue_power = blue_power
        
    def apply_action(self, action: Action, color: PlayerColor):
        match action:
            # the input action is SpawnAction
            case SpawnAction(cell):
                r = cell.r
                q = cell.q
                if (color == PlayerColor.RED):
                    self.state[0][r][q] = 1
                    self.red_power += 1
                else:
                    self.state[1][r][q] = 1
                    self.blue_power += 1
                pass
            # the input action is SpreadAction
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
                
                # Spread
                for i in range(power):
                    # print("r=%d, q=%d, dr=%d, dq=%d" %(r, q, dr, dq))
                    r, q = update_r_q(r, q, dr, dq)
                    self.state[curr_player][r][q] += self.state[opponent][r][q] + 1
                    '''
                    if curr_player eats opponent's token, the power of the current player add the power
                    of the token eaten
                    '''
                    if (curr_player == 0):
                        self.red_power += self.state[opponent][r][q]
                        self.blue_power -= self.state[opponent][r][q]
                    else:
                        self.red_power -= self.state[opponent][r][q]
                        self.blue_power += self.state[opponent][r][q]
                    self.state[opponent][r][q] = 0
                    '''if the token is larger than 6, reduce the power of the current player by 7
                    and remove the token
                    '''
                    if self.state[curr_player][r][q] > 6:
                        self.state[curr_player][r][q] = 0
                        if (curr_player == 0):
                            self.red_power -= 7
                        else:
                            self.blue_power -= 7
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
        
    # function to get the winner of the board
    def winner(self) -> PlayerColor | None:
        if (self.red_power == 0 and self.blue_power == 0):
            return None
        elif (abs(self.red_power - self.blue_power) < WIN_POWER_DIFF):
            return None
        elif (self.red_power > self.blue_power):
            return PlayerColor.RED
        elif (self.red_power < self.blue_power):
            return PlayerColor.BLUE
    
    #function to get the next board by applying the action
    def next_board(self, action: Action, playerColor: PlayerColor):
        next = MatrixBoard(self.state, self.turn_count, self.red_power, self.blue_power)
        next.apply_action(action, playerColor)
        next.turn_count += 1
        return next 

    #function to get all valid actions in the current board
    def get_valid_actions(self, color: PlayerColor):
        output = []
        if (color == PlayerColor.RED):
            curr_player = 0
            opponent = 1
        else:
            curr_player = 1
            opponent = 0
        for r in range(7):
            for q in range(7):
                if (self.state[curr_player][r][q]==0 and (self.state[opponent][r][q]==0) and (self.red_power+self.blue_power)<49):
                    output.append(SpawnAction(HexPos(r,q)))
                elif (self.state[curr_player][r][q] !=0 ):
                    output.append(SpreadAction(HexPos(r,q), HexDir.DownRight))
                    output.append(SpreadAction(HexPos(r,q), HexDir.Down))
                    output.append(SpreadAction(HexPos(r,q), HexDir.DownLeft))
                    output.append(SpreadAction(HexPos(r,q), HexDir.UpLeft))
                    output.append(SpreadAction(HexPos(r,q), HexDir.Up))
                    output.append(SpreadAction(HexPos(r,q), HexDir.UpRight))
        
        return output
    
    #function to simulate a game from the current state
    def playout(self, start_color:PlayerColor) -> PlayerColor | None:
        playout_board = MatrixBoard(self.state, self.turn_count, self.red_power, self.blue_power)
        curr_player = start_color
        depth_limit = 150
        i = 0
        while (not playout_board.game_over() and i < depth_limit):
            playout_board = MatrixBoard(playout_board.state, playout_board.turn_count, playout_board.red_power, playout_board.blue_power)
            actions = playout_board.get_valid_actions(curr_player)
            action = random.choice(actions)
            playout_board.apply_action(action, curr_player)
            playout_board.turn_count += 1
            curr_player = curr_player.opponent
            i += 1
            
        if playout_board.game_over():
            return playout_board.winner()
        else:
            return self.playout_heuristic()
        
    def playout_heuristic(self) -> PlayerColor | None:
        if self.red_power > self.blue_power:
            result = PlayerColor.RED
        elif self.red_power == self.blue_power:
            result =  None
        else:
            result = PlayerColor.BLUE
        return result
    
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
                    power = self.state[0, r, q] if self.state[0, r, q] != 0 else self.state[1, r, q] 
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