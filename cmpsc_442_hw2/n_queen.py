import math

def main():
    print(num_placements_all(4))
    print(num_placements_all(8))
    print(num_placements_one_per_row(4))
    print(num_placements_one_per_row(8))
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

if __name__ == "__main__":
    main()
