from agent.board import MatrixBoard
import numpy as np
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir


matrix = np.zeros([2,7,7], dtype=int)
matrix[0, 1, 4] = 6
matrix[1, 1, 2] = 1
matrix[1, 1, 3] = 1
matrix[1, 1, 5] = 1
matrix[1, 1, 1] = 1
board = MatrixBoard(matrix, 0, 6, 4)

print(board.render(use_color=True, use_unicode=True))
# board.apply_action(SpawnAction(HexPos(1,1)), PlayerColor.RED)
# board.apply_action(SpawnAction(HexPos(1,4)), PlayerColor.BLUE)

# print(board.render(use_color=True, use_unicode=True))
# board.apply_action(SpreadAction(HexPos(1,1), HexDir.DownRight), PlayerColor.RED)
# board.apply_action(SpreadAction(HexPos(1,2), HexDir.DownRight), PlayerColor.RED)
# board.apply_action(SpreadAction(HexPos(1,2), HexDir.DownRight), PlayerColor.BLUE)

# print(board.render(use_color=True, use_unicode=True))
# board.apply_action(SpreadAction(HexPos(1,3), HexDir.DownRight), PlayerColor.BLUE)

# print(board.render(use_color=True, use_unicode=True))
# board.apply_action(SpreadAction(HexPos(1,4), HexDir.UpLeft), PlayerColor.BLUE)

# board.apply_action(SpawnAction(HexPos(1, 4), PlayerColor.RED))
board.apply_action(SpreadAction(HexPos(1,4), HexDir.UpLeft), PlayerColor.RED)

print(board.render(use_color=True, use_unicode=True))
print("red_power=%d, blue_power=%d" %(board.red_power, board.blue_power))