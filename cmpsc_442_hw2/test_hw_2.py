import homework2_yfj5098 as l


# 1. N_Queens Tests:

def test_num_placements_all():
    assert l.num_placements_all(4) == 1820
    assert l.num_placements_all(8) == 4426165368

def test_num_placements_one_per_row():
    assert l.num_placements_one_per_row(4) == 256
    assert l.num_placements_one_per_row(8) == 16777216

def test_n_queens_valid():
    assert l.n_queens_valid([0, 0]) == False
    assert l.n_queens_valid([0, 1]) == False
    assert l.n_queens_valid([0, 2]) == True
    assert l.n_queens_valid([0, 3, 1]) == True

def test_n_queens_solutions():
    assert list(l.n_queens_solutions(4)) == [
        [1, 3, 0, 2],
        [2, 0, 3, 1]
    ]
    assert list(l.n_queens_solutions(6)) == [
        [1, 3, 5, 0, 2, 4],
        [2, 5, 1, 4, 0, 3],
        [3, 0, 4, 1, 5, 2],
        [4, 2, 0, 5, 3, 1]
    ]
    assert len(list(l.n_queens_solutions(8))) == 92

# 2. Light_out Tests:

def test_init_getter():
    b = [[True, False], [False, True]]
    p = l.LightsOutPuzzle(b)
    assert p.get_board() == [[True, False], [False, True]]

    b = [[True, True], [True, True]]
    p = l.LightsOutPuzzle(b)
    assert p.get_board() == [[True, True], [True, True]]

def test_create_puzzle():
    p = l.create_puzzle(2, 2)
    assert p.get_board() == [[False, False], [False, False]]

    p = l.create_puzzle(2, 3)
    assert p.get_board() == [
        [False, False, False],
        [False, False, False]
    ]

def test_perform_move():
    p = l.create_puzzle(3, 3)
    p.perform_move(1, 1)
    assert p.get_board() == [
        [False, True, False],
        [True, True, True],
        [False, True, False]
    ]

    p = l.create_puzzle(3, 3)
    p.perform_move(0, 0)
    assert p.get_board() == [
        [True, True, False],
        [True, False, False],
        [False, False, False]
    ]

def test_is_solved():
    b = [[True, False], [False, True]]
    p = l.LightsOutPuzzle(b)
    assert p.is_solved() == False

    b = [[False, False], [False, False]]
    p = l.LightsOutPuzzle(b)
    assert p.is_solved() == True

def test_copy():
    p = l.create_puzzle(3, 3)
    p2 = p.copy()
    assert (p.get_board() == p2.get_board()) == True

    p = l.create_puzzle(3, 3)
    p2 = p.copy()
    p.perform_move(1, 1)
    assert (p.get_board() == p2.get_board()) == False

def test_successors():
    p = l.create_puzzle(2, 2)
    for move, new_p in p.successors():
        print(move, new_p.get_board())

    for i in range(2, 6):
        p = l.create_puzzle(i, i+1)
        print(len(list(p.successors())))
test_successors()

def test_find_solution():
    p = l.create_puzzle(2, 3)
    for row in range(2):
        for col in range(3):
            p.perform_move(row, col)
    assert p.find_solution() == [(0,0), (0,2)]

    b = [
        [False, False, False],
        [False, False, False]
    ]
    b[0][0] = True
    p = l.LightsOutPuzzle(b)
    assert (p.find_solution() is None) == True

    b = [
        [True, True, False],
        [True, False, False],
        [False, False, False]
    ]
    p = l.LightsOutPuzzle(b)
    assert p.find_solution() == [(0, 0)]

# 3. Linear_disk_movement Tests:

def test_solve_identical_disks():
    assert l.solve_identical_disks(4, 2) == [(0, 2), (1, 3)]
    assert l.solve_identical_disks(4, 3) == [(1, 3), (0, 1)]
    assert l.solve_identical_disks(5, 2) == [(0, 2), (1, 3), (2, 4)]
    assert l.solve_identical_disks(5, 3) == [(1, 3), (0, 1), (2, 4), (1, 2)]

def test_solve_distinct_disks():
    assert l.solve_distinct_disks(4, 2) == [(0, 2), (2, 3), (1, 2)]
    assert l.solve_distinct_disks(4, 3) == [(1, 3), (0, 1), (2, 0), (3, 2), (1, 3), (0, 1)]
    assert l.solve_distinct_disks(5, 2) == [(0, 2), (1, 3), (2, 4)]
    assert l.solve_distinct_disks(5, 3) == [(1, 3), (2, 1), (0, 2), (2, 4), (1, 2)]