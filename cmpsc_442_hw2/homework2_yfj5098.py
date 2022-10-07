############################################################
# CMPSC 442: Homework 2
############################################################

student_name = "Yubo Jing"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.

import random
from queue import Queue
from copy import deepcopy
import math

############################################################
# Section 1: N-Queens
############################################################

def num_placements_all(n):
    f = math.factorial
    return f(n*n) // f(n) // f(n*n-n)

def num_placements_one_per_row(n):
    return n**n

def n_queens_valid(board):
    row, col, pos_diag, neg_diag = set(), set(), set(), set()
    for r in range(len(board)):
        if r in row or board[r] in col or r + board[r] in pos_diag or r - board[r] in neg_diag:
            return False
        row.add(r)
        col.add(board[r])
        pos_diag.add(r + board[r])
        neg_diag.add(r - board[r])
    return True

def n_queens_solutions(n):

    col = set()
    pos_diag = set()  # r + c
    neg_diag = set()  # r - c
    ans = []
    board = [["."] for _ in range(n)]
    
    def backtrack(r):
        if r == n:
            copy = ["".join(row) for row in board]
            ans.append(copy)
            return
        for c in range(n):
            if c in col or (r + c) in pos_diag or (r - c) in neg_diag:
                continue

            col.add(c)
            pos_diag.add(r + c)
            neg_diag.add(r - c)
            board[r] = str(c)

            backtrack(r + 1)
            
            col.remove(c)
            pos_diag.remove(r + c)
            neg_diag.remove(r - c)
            board[r] = "."

    backtrack(0)
    for ele in ans:
        ret = [int(s) for s in ele if s != "."]
        yield ret

############################################################
# Section 2: Lights Out
############################################################

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


############################################################
# Section 3: Linear Disk Movement
############################################################

def solve_identical_disks(length, n):

    # BFS set up
    q = Queue()
    visited = []
    disks_state = [1 if i < n else 0 for i in range(length)] 
    total_moves = []
    q.put((total_moves, disks_state))

    # While not brute force all the possible outcomes
    while not q.empty():
        total_moves, current_disks = q.get()
        if sum(current_disks[length-n:]) == n:
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
                q.put(move_disks(1, i))

            # Two steps forward movement
            if i < length - 2 and current_disks[i] != 0 and current_disks[i + 1] != 0 and current_disks[i + 2] == 0:
                q.put((move_disks(2, i)))
    return None

def solve_distinct_disks(length, n):

    # BFS set up
    q = Queue()
    visited = []
    disks_state = [i if i <= n else 0 for i in range(1, length + 1)]
    total_moves = []
    q.put((total_moves, disks_state))
    
    # While not brute force all the possible outcomes
    while not q.empty():
        total_moves, current_disks = q.get()
        goal = sorted(current_disks, reverse=True)
        if sum(current_disks[length-n:]) == ((1 + n) * n) // 2 and goal[:n] == current_disks[length - n:]:
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
                q.put(move_disks(1, i))

            # Two steps forward movement
            if i < length - 2 and current_disks[i] != 0 and current_disks[i + 1] != 0 and current_disks[i + 2] == 0:
                q.put(move_disks(2, i))

            # One step backward movement
            if i > 0 and current_disks[i] != 0 and current_disks[i - 1] == 0:
                q.put(move_disks(-1, i))

            # Two steps backward movement
            if i > 1 and current_disks[i] != 0 and current_disks[i - 1] != 0 and current_disks[i - 2] == 0:
                q.put(move_disks(-2, i))
    return None

############################################################
# Section 4: Feedback
############################################################

feedback_question_1 = """
8.0
"""

feedback_question_2 = """
Getting start to code bfs with queue is hard, but after you familiar with it, it becomes easier. 
"""

feedback_question_3 = """
It a cool assignment, is that possible to use DFS solve Q2 and Q3? 
"""

print(solve_distinct_disks(11, 4))