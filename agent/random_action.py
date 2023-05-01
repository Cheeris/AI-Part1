from agent.board import MatrixBoard
import numpy as np
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir
import random

def random_action(board: MatrixBoard, color: PlayerColor) -> Action:
    actions = board.get_valid_actions(color)
    return random.choice(actions)