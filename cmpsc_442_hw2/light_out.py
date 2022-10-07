import random
from queue import Queue
from copy import deepcopy

def main():
    b = [
        [False, False, False],
        [False, False, False]
    ]
    b[0][0] = True
    p = create_puzzle(2, 3)
    for row in range(2):
        for col in range(3):
            p.perform_move(row,col)
    print(p.find_solution())
    k = LightsOutPuzzle(b)
    print(k.find_solution())


class LightsOutPuzzle(object):

    def __init__(self, board):
        self.board = board

    def get_board(self):
        return self.board
    
    def get_dimention(self):
        return (len(self.board), len(self.board[0]))

    def perform_move(self, row, col):
        rows, cols = self.get_dimention()
        self.board[row][col] = not(self.board[row][col])
        if row - 1 >= 0:
            self.board[row - 1][col] = not(self.board[row - 1][col])
        if row + 1 < rows:
            self.board[row + 1][col] = not(self.board[row + 1][col])
        if col - 1 >= 0:
            self.board[row][col - 1] = not(self.board[row][col - 1])
        if col + 1 < cols:
            self.board[row][col + 1] = not(self.board[row][col + 1])

    def scramble(self):
        rows, cols = self.get_dimention()
        for row in range(rows):
            for col in range(cols):
                if random.random() < 0.5:
                    self.perform_move(row, col)

    def is_solved(self):
        rows, cols = self.get_dimention()
        for row in range(rows):
            for col in range(cols):
                if self.board[row][col] != False:
                    return False
        return True

    def copy(self):
        return LightsOutPuzzle(deepcopy(self.board))

    def successors(self):
        rows, cols = self.get_dimention()
        for row in range(rows):
            for col in range(cols):
                copy_board = self.copy()
                copy_board.perform_move(row, col)
                yield (row, col), copy_board

    def find_solution(self):
        q = Queue()
        visited = set()
        q.put(([], self))
        while not q.empty():
            # Pop queue
            current_q_moves, p = q.get()

            # Return current moves if solved
            if p.is_solved():
                return current_q_moves

            # Put current state into visited if not yet 
            state = tuple(map(tuple, p.get_board()))
            if state in visited:
                continue
            else:
                visited.add(state)

            # Brute force try the moves
            for move, new_p in p.successors():
                new_q_moves = deepcopy(current_q_moves)
                new_q_moves.append(move)
                q.put((new_q_moves, new_p))

        return None


def create_puzzle(rows, cols):
    return LightsOutPuzzle([[False for _ in range(cols)] for _ in range(rows)])


if __name__ == "__main__":
    main()