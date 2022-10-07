############################################################
# CMPSC 442: Homework 3
############################################################

student_name = "Yubo Jing"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.

import random
from copy import deepcopy
from queue import PriorityQueue, Queue
import math


############################################################
# Section 1: Tile Puzzle
############################################################

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
        while not PQ.empty():
            _, current_moves, p = PQ.get()
            if p.is_solved():
                return current_moves
            for new_moves, new_p in p.successors():
                if new_p.get_board() in visited:
                    continue
                visited.append(p.board)
                # total cost = current cost + md cost
                updated_moves = current_moves + [new_moves]
                PQ.put((len(current_moves) + new_p.md_h(), updated_moves, new_p))


############################################################
# Section 2: Grid Navigation
############################################################

# Euclidean distance heuristic
def ed_h(start, goal):
    return math.sqrt((start[0] - goal[0]) ** 2 + (start[1] - goal[1]) ** 2)

def get_moves(current_location, scene):
    current_location_x, current_location_y = current_location
    max_x, max_y = len(scene) - 1, len(scene[0]) - 1
    for possible_move_x in range(current_location_x - 1, current_location_x + 2):
        for possible_move_y in range(current_location_y - 1, current_location_y + 2):
            if 0 <= possible_move_x <= max_x and 0 <= possible_move_y <= max_y and scene[possible_move_x][possible_move_y] == False:
                yield possible_move_x, possible_move_y

def find_path(start, goal, scene):
    # Edge case check: Can't start or end at obstacles
    if scene[start[0]][start[1]] or scene[goal[0]][goal[1]]:
        return None

    PQ = PriorityQueue()
    cost_till_current = 0
    total_cost = ed_h(start, goal) + cost_till_current
    current_path = [start]
    current_location = start
    PQ.put((total_cost, cost_till_current, current_path, current_location))
    visited = set()
    while not PQ.empty():
        _, cost_till_current, current_path, current_location = PQ.get()
        if current_location in visited:
            continue
        else:
            visited.add(current_location)
        if current_location == goal:
            return current_path
        for new_location in get_moves(current_location, scene):
            if new_location not in visited:
                updated_path = current_path + [new_location]
                PQ.put((cost_till_current + ed_h(current_location, new_location) + ed_h(new_location, goal), 
                cost_till_current + ed_h(current_location, new_location), updated_path, new_location))
    return None

############################################################
# Section 3: Linear Disk Movement, Revisited
############################################################

def solve_distinct_disks(length, n):
    solved_disks = [0 for i in range(length - n)] + [j for j in range(n, 0, -1)]
    disks_state = [i if i <= n else 0 for i in range(1, length + 1)]
    # A star set up
    PQ = PriorityQueue()
    visited = []
    total_moves = []
    PQ.put((0, total_moves, disks_state))

    def h(disks):
        h = 0
        for i in range(len(disks)):
            if disks[i] != 0:
                h += abs(i - solved_disks.index(disks[i]))
        return h
        
    # While not brute force all the possible outcomes
    while not PQ.empty():
        cost, total_moves, current_disks = PQ.get()
        if current_disks == solved_disks:
            return total_moves
        if current_disks in visited:
            continue
        else:
            visited.append(current_disks)

        # Helper function to cover different steps movement and put new structure into queue
        def move_disks(step, location):
            new_disks = deepcopy(current_disks)
            temp = new_disks[location]
            new_disks[location] = new_disks[location + step]
            new_disks[location + step] = temp
            new_moves = deepcopy(total_moves)
            new_moves.append((location, location + step))
            return (new_moves, new_disks)

        for i in range(length):
            
            # One step forward movement
            if i < length - 1 and current_disks[i] != 0 and current_disks[i+1] == 0:
                new_moves, new_disks = move_disks(1, i)
                PQ.put((1 + h(new_disks), new_moves, new_disks))

            # Two steps forward movement
            if i < length - 2 and current_disks[i] != 0 and current_disks[i + 1] != 0 and current_disks[i + 2] == 0:
                new_moves, new_disks = move_disks(2, i)
                PQ.put((1 + h(new_disks), new_moves, new_disks))

            # One step backward movement
            if i > 0 and current_disks[i] != 0 and current_disks[i - 1] == 0:
                new_moves, new_disks = move_disks(-1, i)
                PQ.put((1 + h(new_disks), new_moves, new_disks))

            # Two steps backward movement
            if i > 1 and current_disks[i] != 0 and current_disks[i - 1] != 0 and current_disks[i - 2] == 0:
                new_moves, new_disks = move_disks(-2, i)
                PQ.put((1 + h(new_disks), new_moves, new_disks))
    return None

############################################################
# Section 4: Dominoes Game
############################################################

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

############################################################
# Section 5: Feedback
############################################################

feedback_question_1 = """
12.0
"""

feedback_question_2 = """
The iddfs is confusing
"""

feedback_question_3 = """
MINIMAX is cool to implement
"""
