import homework3_yfj5098 as h


############################################################
# Test - Section 1: Tile Puzzle
############################################################

def test_get_board():
    p = h.create_tile_puzzle(3, 3)
    assert p.get_board() == [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]
    p = h.create_tile_puzzle(2, 4)
    assert p.get_board() == [
        [1, 2, 3, 4],
        [5, 6, 7, 0]
    ]

def test_perform_move():
    p = h.create_tile_puzzle(3, 3)
    assert p.perform_move("up") == True
    assert p.get_board() == [
        [1, 2, 3],
        [4, 5, 0],
        [7, 8, 6]
    ]
    assert p.perform_move("up") == True
    assert p.get_board() == [
    [1, 2, 0],
    [4, 5, 3],
    [7, 8, 6]
    ]
    assert p.perform_move("up") == False
    assert p.perform_move("right") == False
    assert p.perform_move("left") == True
    assert p.get_board() == [
    [1, 0, 2],
    [4, 5, 3],
    [7, 8, 6]
    ]
    assert p.perform_move("down") == True
    assert p.get_board() == [
    [1, 5, 2],
    [4, 0, 3],
    [7, 8, 6]
    ]

def test_is_solved():
    p = h.create_tile_puzzle(3, 3)
    assert (p.is_solved()) == True
    p.perform_move("up")
    assert (p.is_solved()) == False
    p.perform_move("up")
    assert (p.is_solved()) == False
    p.perform_move("down")
    assert (p.is_solved()) == False
    p.perform_move("down")
    assert (p.is_solved()) == True

def test_copy():
    p = h.create_tile_puzzle(3, 3)
    p2 = p.copy()
    assert p.get_board() == p2.get_board()
    p.perform_move("left")
    assert (p.get_board() == p2.get_board()) == False

def test_successors():
    b = [[1, 2, 3], [4, 0, 5], [6, 7, 8]]
    p = h.TilePuzzle(b)
    lst = []
    for move, new_p in p.successors():
        lst.append((move, new_p.get_board()))
    assert lst == [('up', [[1, 0, 3], [4, 2, 5], [6, 7, 8]]), ('down', [[1, 2, 3], [4, 7, 5], [6, 0, 8]]), ('left', [[1, 2, 3], [0, 4, 5], [6, 7, 8]]), ('right', [[1, 2, 3], [4, 5, 0], [6, 7, 8]])]

    p = h.create_tile_puzzle(3, 3)
    lst = []
    for move, new_p in p.successors():
        lst.append((move, new_p.get_board()))
    assert lst == [('up', [[1, 2, 3], [4, 5, 0], [7, 8, 6]]), ('left', [[1, 2, 3], [4, 5, 6], [7, 0, 8]])]

def test_find_solutions_iddfs():
    b = [[4, 1, 2], [0, 5, 3], [7, 8, 6]]
    c = [[1, 2, 3], [4, 0, 8], [7, 6, 5]]
    p = h.TilePuzzle(b)
    assert list(p.find_solutions_iddfs()) == [['up', 'right', 'right', 'down', 'down']]
    p = h.TilePuzzle(c)
    assert list(p.find_solutions_iddfs()) == [['down', 'right', 'up', 'left', 'down', 'right'], ['right', 'down', 'left', 'up', 'right', 'down']]

def test_find_solution_a_star():
    b = [[4, 1, 2], [0, 5, 3], [7, 8, 6]]
    c = [[1, 2, 3], [4, 0, 5], [6, 7, 8]]
    p = h.TilePuzzle(b)
    assert p.find_solution_a_star() == ['up', 'right', 'right', 'down', 'down']
    p = h.TilePuzzle(c)
    assert p.find_solution_a_star() == ['right', 'down', 'left', 'left', 'up', 'right', 'down', 'right', 'up', 'left', 'left', 'down', 'right', 'right']


############################################################
# Test - Section 3: Linear Disk Movement, Revisited
############################################################

def test_solve_distinct_disks():
    assert h.solve_distinct_disks(4, 2) == [(0, 2), (2, 3), (1, 2)]
    assert h.solve_distinct_disks(4, 3) == [(1, 3), (0, 1), (2, 0), (3, 2), (1, 3), (0, 1)]
    assert h.solve_distinct_disks(5, 2) == [(0, 2), (1, 3), (2, 4)]
    assert h.solve_distinct_disks(5, 3) == [(1, 3), (2, 1), (0, 2), (2, 4), (1, 2)]
    assert h.solve_distinct_disks(11, 4) == [(2, 4), (0, 2), (3, 5), (1, 3), (4, 6), (2, 4), (5, 7), (3, 5), (6, 8), (4, 6), (8, 9), (6, 8), (8, 10), (9, 8), (7, 6), (5, 7), (7, 9), (6, 7)]


############################################################
# Test - Section 4: Dominoes Game
############################################################

def test_get_board_d():
    b = [[False, False], [False, False]]
    g = h.DominoesGame(b)
    assert g.get_board() == [[False, False], [False, False]]
    b = [[True, False], [True, False]]
    g = h.DominoesGame(b)
    assert g.get_board() == [[True, False], [True, False]]

def test_create_dominoes_game():
    g = h.create_dominoes_game(2, 2)
    assert g.get_board() == [[False, False], [False, False]]
    g = h.create_dominoes_game(2, 3)
    assert g.get_board() == [[False, False, False], [False, False, False]]

def test_reset():
    b = [[False, False], [False, False]]
    g = h.DominoesGame(b)
    g.reset()
    assert g.get_board() == [[False, False], [False, False]]
    b = [[True, False], [True, False]]
    g = h.DominoesGame(b)
    g.reset()
    assert g.get_board() == [[False, False], [False, False]]

def test_is_legal_move():
    b = [[False, False], [False, False]]
    g = h.DominoesGame(b)
    assert g.is_legal_move(0, 0, True) == True
    assert g.is_legal_move(0, 0, False) == True

def test_legal_moves():
    g = h.create_dominoes_game(3, 3)
    assert list(g.legal_moves(True)) == [(0,0), (0,1), (0, 2), (1, 0), (1,1), (1,2)]
    assert list(g.legal_moves(False)) == [(0,0), (0,1), (1,0), (1,1), (2,0), (2, 1)]
    b = [[True, False], [True, False]]
    g = h.DominoesGame(b)
    assert list(g.legal_moves(True)) == [(0, 1)]
    assert list(g.legal_moves(False)) == []

def test_perform_move_d():
    g = h.create_dominoes_game(3, 3)
    g.perform_move(0, 1, True)
    assert g.get_board() == [[False, True, False], [False, True, False], [False, False, False]]
    g = h.create_dominoes_game(3, 3)
    g.perform_move(1, 0, False)
    assert g.get_board() == [[False, False, False], [True, True, False], [False, False, False]]

def test_game_over():
    b = [[False, False], [False, False]]
    g = h.DominoesGame(b)
    assert g.game_over(True) == False
    assert g.game_over(False) == False
    b = [[True, False], [True, False]]
    g = h.DominoesGame(b)
    assert g.game_over(True) == False
    assert g.game_over(False) == True

def test_copy_d():
    g = h.create_dominoes_game(4, 4)
    g2 = g.copy()
    assert (g.get_board() == g2.get_board()) == True
    g.perform_move(0, 0, True)
    assert (g.get_board() == g2.get_board()) == False

def test_get_best_move():
    b = [[False] * 3 for i in range(3)]
    g = h.DominoesGame(b)
    assert g.get_best_move(True, 1) == ((0, 1), 2, 6)
    assert g.get_best_move(True, 2) == ((0, 1), 3, 10)
    g.perform_move(0, 1, True)
    assert g.get_best_move(False, 1) == ((2, 0), -3, 2)
    assert g.get_best_move(False, 2) == ((2, 0), -2, 5)