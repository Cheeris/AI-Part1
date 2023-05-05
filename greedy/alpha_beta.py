from .board import MatrixBoard, update_r_q
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir
import random
import numpy
class ABNode:
    def __init__(self, board: MatrixBoard, color: PlayerColor):
        self.board = MatrixBoard(board.state, board.turn_count, board.red_power, board.blue_power)
        self.children = []
        self.color = color
        self.action = None
        
    def add_children(self):
        all_children =[]
        for action in self.board.get_valid_actions(self.color):
            child_board= self.board.next_board(action, self.color)
            child = ABNode(child_board, PlayerColor.RED if self.color == PlayerColor.BLUE else PlayerColor.BLUE)
            child.action = action
            all_children.append(child)
        all_children.sort(key = key_function)
        # use top K algorithm: select k nodes with highest utility
        for child in all_children[:10]:
            self.children.append(child)


def alpha_beta(node: ABNode, depth: int, alpha, beta, maximize:bool, color: PlayerColor):
    if (depth==0) or (node.board.game_over()):
        return eval(node.board, color)
    if (maximize==True):
        best = float('-inf')
        for child in node.children:
            child.add_children()
            child_eval = alpha_beta(child, depth-1, alpha, beta, False, color)
            best = max(best, child_eval)
            alpha = max(alpha, best)
            if beta<=alpha:
                break
        return best
    else:
        worst = float('inf')
        child_len = len(node.children)
        for child in node.children:
            child.add_children()
            child_eval = alpha_beta(child, depth-1, alpha, beta, True, color)
            worst = min(beta, child_eval)
            beta = min(beta, worst)
            if beta<=alpha:
                break
        return worst

def minimax_with_alpha_beta(node: ABNode, color:PlayerColor, depth:int):
    '''
    Use minimax search algorithm.
    Calculate all the minimum evaluation value of the children of the root, and select
    the child with the highest evaluation value.
    '''
    values = dict()
    for child in node.children:
        child.add_children()
        values.update({child.action: alpha_beta(child,depth,float('-inf'),float('inf'), False, color)})
    choices = []
    best_eval = max(values.values())
    for action in values.keys():
        if values[action] == best_eval:
            choices.append(action)
    return random.choice(choices)

def eval(board: MatrixBoard, color: PlayerColor):
    unique,count = numpy.unique(board.state[0],return_counts=True)
    red = dict(zip(unique, count))
    unique,count = numpy.unique(board.state[1],return_counts=True)
    blue = dict(zip(unique, count))
    red_num = sum(red.values())
    blue_num = sum(red.values())
    if abs(board.red_power - board.blue_power) < 30:
        attack_power, safe_power = calculate_attack_range(board.state, color)
    else:
        attack_power, safe_power = 0, 0
    if color == PlayerColor.RED:
        return 1*(red.get(1,0)-blue.get(1,0))+\
                2*(red.get(2,0)-blue.get(2,0))+\
                3*(red.get(3,0)-blue.get(3,0))+\
                4*(red.get(4,0)-blue.get(4,0))+\
                6*(red.get(5,0)-blue.get(5,0))+\
                3*(red.get(6,0)-blue.get(6,0))+\
                6*(red_num-blue_num)+\
                6*(board.red_power - board.blue_power)+\
                3*attack_power+\
                3*safe_power
    else:
        return 1*(blue.get(1,0)-red.get(1,0))+\
                2*(blue.get(2,0)-red.get(2,0))+\
                3*(blue.get(3,0)-red.get(3,0))+\
                4*(blue.get(4,0)-red.get(4,0))+\
                6*(blue.get(5,0)-red.get(5,0))+\
                3*(blue.get(6,0)-red.get(6,0))+\
                6*(blue_num-red_num)+\
                6*(board.blue_power-board.red_power)+\
                3*attack_power+\
                3*safe_power
    
def key_function(obj):
    util =-100
    util = eval(obj.board, obj.color)
    return (util, random.random())       #random.ramdom() ensures the randomness of selection when utilities are same
    
def utility(board: MatrixBoard, color: PlayerColor):
    if color == PlayerColor.RED:
        return board.red_power-board.blue_power
    else:
        return board.blue_power-board.red_power
    
def calculate_attack_range(state, color):
    domain_state = numpy.zeros(shape=[2,7,7], dtype=int)
    curr_player = 0 if color == PlayerColor.RED else 1
    opposite = 1 if color == PlayerColor.RED else 0
    all_dir = [HexDir.Down, HexDir.DownLeft, HexDir.DownRight, 
            HexDir.Up, HexDir.UpLeft, HexDir.UpRight]

    for player in range(2):
        for i in range(7):
            for j in range(7):
                power = state[player][i][j]
                if power == 0:
                    continue
                for d in all_dir:
                    r = i
                    q = j
                    dr = d.value.r
                    dq = d.value.q
                    for p in range(power):
                        r, q = update_r_q(r, q, dr, dq)
                        domain_state[player, r, q] = 1


    domain_coodinates = set([tuple(x) for x in numpy.argwhere(domain_state[curr_player] > 0)])
    player_coordinates = set([tuple(x) for x in numpy.argwhere(state[curr_player] > 0)])
    opposite_coordinates = set([tuple(x) for x in numpy.argwhere(state[opposite] > 0)])
    opposite_domain = set([tuple(x) for x in numpy.argwhere(domain_state[opposite] > 0)])
    attack_coord = domain_coodinates & opposite_coordinates
    safeguard_coord = player_coordinates & opposite_domain
    
    # overlap_num = len(overlap_coord)
    # the total power of opposite which can be eaten by the player
    attack_power = sum([state[opposite][x] for x in attack_coord])
    
    # the total power of player which can NOT be eaten by the opposite
    safeguard_power = sum([state[curr_player][x] for x in safeguard_coord])
    return attack_power, safeguard_power