from agent.board import MatrixBoard
import numpy as np
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir
from agent.mcts_alphazero import MCNode, monte_carlo_tree_search
from agent.CNNModel import CNNModel
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
# matrix = np.zeros([2,7,7], dtype=int)
# matrix[0, 1, 4] = 6
# matrix[1, 1, 2] = 1
# matrix[1, 1, 3] = 1
# matrix[1, 1, 5] = 1
# matrix[1, 1, 1] = 1
# board = MatrixBoard(matrix, 0, 6, 4)

# print(board.render(use_color=True, use_unicode=True))
# # board.apply_action(SpawnAction(HexPos(1,1)), PlayerColor.RED)
# # board.apply_action(SpawnAction(HexPos(1,4)), PlayerColor.BLUE)

# # print(board.render(use_color=True, use_unicode=True))
# # board.apply_action(SpreadAction(HexPos(1,1), HexDir.DownRight), PlayerColor.RED)
# # board.apply_action(SpreadAction(HexPos(1,2), HexDir.DownRight), PlayerColor.RED)
# # board.apply_action(SpreadAction(HexPos(1,2), HexDir.DownRight), PlayerColor.BLUE)

# # print(board.render(use_color=True, use_unicode=True))
# # board.apply_action(SpreadAction(HexPos(1,3), HexDir.DownRight), PlayerColor.BLUE)

# # print(board.render(use_color=True, use_unicode=True))
# # board.apply_action(SpreadAction(HexPos(1,4), HexDir.UpLeft), PlayerColor.BLUE)

# # board.apply_action(SpawnAction(HexPos(1, 4), PlayerColor.RED))
# board.apply_action(SpreadAction(HexPos(1,4), HexDir.UpLeft), PlayerColor.RED)

# print(board.render(use_color=True, use_unicode=True))
# print("red_power=%d, blue_power=%d" %(board.red_power, board.blue_power))

###############MODEL###################
# MODEL_PATH = '/Users/clarec/Desktop/COMP30024-AI-ProjectB/rr_e100.pth'
# color = PlayerColor.RED
# board = MatrixBoard(np.zeros([2,7,7], dtype=int), 0, 0, 0)
# model = CNNModel()
# model.load_state_dict(torch.load(MODEL_PATH))
# root = MCNode(MatrixBoard(np.zeros([2,7,7], dtype=int), 0, 0, 0), color, model=model)
# result, root = monte_carlo_tree_search(root)
# print(result)
###############MODEL###################


np_more_red = np.array([[[0,0,1,3,5,0,0], 
                        [0,1,0,0,0,3,0],
                        [0,0,5,2,0,0,0],
                        [1,2,0,0,3,0,4],
                        [3,0,1,0,0,0,0],
                        [0,2,1,0,0,0,0],
                        [1,0,0,2,0,4,6]],
                        [[1,2,0,0,0,0,0],
                         [3,0,0,0,0,0,0],
                         [4,0,0,0,0,0,0],
                         [0,0,0,0,0,0,0],
                         [0,0,0,0,0,3,0],
                         [0,0,0,0,0,0,0],
                         [0,0,0,0,5,0,0]]])
board_mroe_red = MatrixBoard(np_more_red, 100, np_more_red[0].sum(), np_more_red[1].sum())
board_mroe_red.render(use_color=True, use_unicode=True)