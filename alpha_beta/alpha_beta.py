from alpha_beta.board import MatrixBoard
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
    '''
    red_num =0
    blue_num = 0
    red = [0,0,0,0,0,0]
    blue = [0,0,0,0,0,0]
    for r in range(7):
        for q in range(7):
            if board.state[0][r][q] != 0:
                red[board.state[0][r][q]-1] +=1
                red_num+=1
            if board.state[1][r][q] != 0:
                blue[board.state[1][r][q]-1] +=1
                blue_num+=1
    '''
    unique,count = numpy.unique(board.state[0],return_counts=True)
    red = dict(zip(unique, count))
    unique,count = numpy.unique(board.state[1],return_counts=True)
    blue = dict(zip(unique, count))
    red_num = sum(red.values())
    blue_num = sum(red.values())
    if color == PlayerColor.RED:
        return 1*(red.get(1,0)-blue.get(1,0))+2*(red.get(2,0)-blue.get(2,0))+3*(red.get(3,0)-blue.get(3,0))+4*(red.get(4,0)-blue.get(4,0))+5*(red.get(5,0)-blue.get(5,0))+6*(red.get(6,0)-blue.get(6,0))+3*(red_num-blue_num)
    else:
        return 1*(blue.get(1,0)-red.get(1,0))+2*(blue.get(2,0)-red.get(2,0))+3*(blue.get(3,0)-red.get(3,0))+4*(blue.get(4,0)-red.get(4,0))+5*(blue.get(5,0)-red.get(5,0))+6*(blue.get(6,0)-red.get(6,0))+3*(blue_num-red_num)
    
def key_function(obj):
    util =-100
    util = utility(obj.board, obj.color)
    return (util, random.random())
    
def utility(board: MatrixBoard, color: PlayerColor):
    if color == PlayerColor.RED:
        return board.red_power-board.blue_power
    else:
        return board.blue_power-board.red_power