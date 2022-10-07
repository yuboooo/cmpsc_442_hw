import random
from copy import deepcopy

def create_dominoes_game(rows, cols):
    return DominoesGame([[False] * cols for _ in range(rows)])


class DominoesGame(object):
    # Required
    def __init__(self, board):
        self.board = board
        self.rows = len(board)
        self.cols = len(board[0])
        self.best_move = None
        self.MAX, self.MIN = float('inf'), float('-inf')

    def get_board(self):
        return self.board

    def reset(self):
        self.board = [[False] * self.cols] * self.rows

    def is_legal_move(self, row, col, vertical):
        # Out of bounds
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return False
        # Current is filled
        if self.board[row][col]:
            return False
        # Vertical out of bounds or filled
        if vertical and (row + 1 >= self.rows or self.board[row + 1][col]):
            return False
        # Horizontal out of bounds or filled
        if not vertical and (col + 1 >= self.cols or self.board[row][col + 1]):
            return False
        return True

    def legal_moves(self, vertical):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.is_legal_move(i, j, vertical):
                    yield i, j

    def perform_move(self, row, col, vertical):
        if self.is_legal_move(row, col, vertical):
            self.board[row][col] = True
            if vertical:
                self.board[row + 1][col] = True
            else:
                self.board[row][col + 1] = True

    def game_over(self, vertical):
        return len(list(self.legal_moves(vertical))) == 0

    def copy(self):
        return DominoesGame(deepcopy(self.board))

    def successors(self, vertical):
        for row, col in self.legal_moves(vertical):
            new_board = self.copy()
            new_board.perform_move(row, col, vertical)
            yield (row, col), new_board

    def get_random_move(self, vertical):
        return random.choice(list(self.legal_moves(vertical)))


    def get_successors(self, vertical):
        return list(self.successors(vertical)), list(self.successors(not vertical))

    def utility(self, p, q):
        return len(p) - len(q)

    def max_value(self, vertical, limit, current_move, a, b):
        vp, hp = self.get_successors(vertical)
        utility = self.utility(vp, hp)
        if limit == 0 or self.game_over(vertical):
            return current_move, utility, 1
        # set v:
        max_move, max_val, max_depth = current_move, self.MIN, 0
        for new_move, new_g in vp:
            min_move, min_val, min_depth = new_g.min_value(not vertical, limit - 1, new_move, a, b)
            # v = max(v, min_val(s, a, b))
            if min_val > max_val:
                max_val = min_val
                max_move = new_move
            max_depth += min_depth

            if max_val >= b:
                return max_move, max_val, max_depth
            a = max(a, max_val)
        return max_move, max_val, max_depth

    def min_value(self, vertical, limit, current_move, a, b):
        vp, hp = self.get_successors(vertical)
        utility = self.utility(hp, vp)
        if limit == 0 or self.game_over(vertical):
            return current_move, utility, 1
        # set v:
        min_move, min_val, min_depth = current_move, self.MAX, 0
        for new_move, new_g in vp:
            max_move, max_val, max_depth = new_g.max_value(not vertical, limit - 1, new_move, a, b)
            # v = min(v, max_val(a, b))
            if min_val > max_val:
                min_val = max_val
                min_move = new_move
            min_depth += max_depth

            if min_val <= a:
                return min_move, min_val, min_depth
            b = min(b, min_val)
        return min_move, min_val, min_depth


    # Required
    def get_best_move(self, vertical, limit):
        return self.max_value(vertical, limit, [], self.MIN, self.MAX)