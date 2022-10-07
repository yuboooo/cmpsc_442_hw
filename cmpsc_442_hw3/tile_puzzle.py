import random
from copy import deepcopy
from queue import PriorityQueue


def main():
    b = [[4, 1, 2], [0, 5, 3], [7, 8, 6]]
    c = [[1, 2, 3], [4, 0, 5], [6, 7, 8]]
    d = [[5, 1, 3], [2, 0, 8], [4, 6, 7]]
    p = TilePuzzle(b)
    solutions = p.find_solution_a_star()
    print(list(p.find_solutions_iddfs()))


def create_tile_puzzle(rows, cols):
    return TilePuzzle([[(col + row * cols) if (col + row * cols) < (rows * cols) else 0 for col in range(1, cols + 1)]for row in range(rows)])


class TilePuzzle(object):
    def __init__(self, board):
        self.board = board
        self.rows = len(self.board)
        self.cols = len(self.board[0])

    def get_board(self):
        return self.board

    def get_zero_index(self):
        for row, col in enumerate(self.board):
            if 0 in col:
                return row, col.index(0)

    def perform_move(self, direction):
        row, col = self.get_zero_index()

        def swap(r_move, c_move):
            temp = self.board[row][col]
            self.board[row][col] = self.board[row + r_move][col + c_move]
            self.board[row + r_move][col + c_move] = temp

        if direction == "up" and row - 1 >= 0:
            swap(-1, 0)
            return True
        elif direction == "down" and row + 1 < self.rows:
            swap(1, 0)
            return True
        elif direction == "left" and col - 1 >= 0:
            swap(0, -1)
            return True
        elif direction == "right" and col + 1 < self.cols:
            swap(0, 1)
            return True
        return False

    def scramble(self, num_moves):
        choices = ["up", "down", "left", "right"]
        for _ in range(num_moves):
            self.perform_move(random.choice(choices))

    def is_solved(self):
        solved_board = [[(col + row * self.cols) if (col + row * self.cols) < (self.rows * self.cols) else 0 for col in range(1, self.cols + 1)] for row in range(self.rows)]
        if self.board == solved_board:
            return True
        return False

    def copy(self):
        return deepcopy(TilePuzzle(self.board))

    def successors(self):
        possible_moves = ["up", "down", "left", "right"]
        for move in possible_moves:
            new_p = self.copy()
            if new_p.perform_move(move):
                yield move, new_p

    def iddfs_helper(self, limit, current_moves):
        visited = [self.board]
        if self.is_solved():
            yield current_moves
        elif len(current_moves) < limit:
            for new_moves, new_p in self.successors():
                if new_p.get_board() in visited:
                    continue
                visited.append(new_p.board)
                for move in new_p.iddfs_helper(limit, current_moves + [new_moves]):
                    yield move


    # Required
    def find_solutions_iddfs(self):
        limit = 0
        while True:
            solutions = list(self.iddfs_helper(limit, []))
            if len(solutions) > 0:
                for solution in solutions:
                    yield solution
                break
            limit += 1


    def md_h(self):
        '''
        Create a dictionary to store the solved board index for each tile
        For example: 1: (0, 0), 2: (0, 1) ...
        Hence when calculating md: 
        md += abs(tile_row - solved_board_row) + abs(tile_col - solved_board_col)
        '''

        sovled_board_index = {}
        current_tile = 1
        zero_tile = self.rows * self.cols
        for i in range(self.rows):
            for j in range(self.cols):
                if current_tile == zero_tile:
                    sovled_board_index[0] = (i, j)
                else:
                    sovled_board_index[current_tile] = (i, j)
                current_tile += 1

        md = 0
        for row in range(self.rows):
            for col in range(self.cols):
                current_tile = self.board[row][col]
                i, j = sovled_board_index[current_tile]
                md += abs(row - i) + abs(col - j)
        return md


    # Required
    def find_solution_a_star(self):
        PQ = PriorityQueue()
        PQ.put((self.md_h(), [], self.copy()))
        visited = [self.board]
        while PQ:
            _, current_moves, p = PQ.get()
            if p.is_solved():
                return current_moves
            for new_moves, new_p in p.successors():
                if new_p.get_board() in visited:
                    continue
                visited.append(p.board)
                # total cost = current cost + md cost
                total_cost = len(current_moves) + new_p.md_h()
                updated_moves = current_moves + [new_moves]
                PQ.put((total_cost, updated_moves, new_p))

if __name__ == "__main__":
    main()
