from gomill_tests import gomill_test_support

from gomill import ascii_boards
from gomill import boards
from gomill import sgf
from gomill import sgf_moves

def make_tests(suite):
    suite.addTests(gomill_test_support.make_simple_tests(globals()))


SAMPLE_SGF = """\
(;AP[testsuite:0]CA[utf-8]DT[2009-06-06]FF[4]GM[1]KM[7.5]PB[Black engine]
PL[B]PW[White engine]RE[W+R]SZ[9]AB[ai][bh][ee]AW[fc][gc];B[dg];W[ef]C[comment
on two lines];B[];W[tt]C[Final comment])
"""

DIAGRAM1 = """\
9  .  .  .  .  .  .  .  .  .
8  .  .  .  .  .  .  .  .  .
7  .  .  .  .  .  o  o  .  .
6  .  .  .  .  .  .  .  .  .
5  .  .  .  .  #  .  .  .  .
4  .  .  .  .  .  .  .  .  .
3  .  .  .  .  .  .  .  .  .
2  .  #  .  .  .  .  .  .  .
1  #  .  .  .  .  .  .  .  .
   A  B  C  D  E  F  G  H  J\
"""

DIAGRAM2 = """\
9  .  .  .  .  .  .  .  .  .
8  .  .  .  .  .  .  .  .  .
7  .  .  .  .  .  .  .  .  .
6  .  .  .  .  .  .  .  .  .
5  .  .  .  .  .  .  .  .  .
4  .  .  .  .  #  .  .  .  .
3  .  .  .  .  .  .  .  .  .
2  .  .  #  .  .  .  .  .  .
1  .  .  .  .  .  .  .  .  .
   A  B  C  D  E  F  G  H  J\
"""


def test_get_setup_and_moves(tc):
    g1 = sgf.sgf_game_from_string(SAMPLE_SGF)
    board1, moves1 = sgf_moves.get_setup_and_moves(g1)
    tc.assertDiagramEqual(ascii_boards.render_board(board1), DIAGRAM1)
    tc.assertEqual(moves1,
                   [('b', (2, 3)), ('w', (3, 4)), ('b', None), ('w', None)])

    g2 = sgf.Sgf_game(size=9)
    root = g2.get_root()
    root.set("AB", [(1, 2), (3, 4)]);
    node = g2.extend_main_sequence()
    node.set("B", (5, 6))
    node = g2.extend_main_sequence()
    node.set("W", (5, 7))
    board2, moves2 = sgf_moves.get_setup_and_moves(g2)
    tc.assertDiagramEqual(ascii_boards.render_board(board2), DIAGRAM2)
    tc.assertEqual(moves2,
                   [('b', (5, 6)), ('w', (5, 7))])


def test_set_initial_position(tc):
    board = boards.Board(9)
    board.play(0, 0, 'b')
    board.play(6, 5, 'w')
    board.play(1, 1, 'b')
    board.play(6, 6, 'w')
    board.play(4, 4, 'b')
    tc.assertDiagramEqual(ascii_boards.render_board(board), DIAGRAM1)
    sgf_game = sgf.Sgf_game(9)
    sgf_moves.set_initial_position(sgf_game, board)
    root = sgf_game.get_root()
    tc.assertEqual(root.get("AB"), set([(0, 0), (1, 1), (4, 4)]))
    tc.assertEqual(root.get("AW"), set([(6, 5), (6, 6)]))
    tc.assertRaises(KeyError, root.get, 'AE')

def test_indicate_first_player(tc):
    g1 = sgf.sgf_game_from_string("(;FF[4]GM[1]SZ[9];B[aa];W[ab])")
    sgf_moves.indicate_first_player(g1)
    tc.assertEqual(sgf.serialise_sgf_game(g1),
                   "(;FF[4]GM[1]SZ[9];B[aa];W[ab])\n")
    g2 = sgf.sgf_game_from_string("(;FF[4]GM[1]SZ[9];W[aa];B[ab])")
    sgf_moves.indicate_first_player(g2)
    tc.assertEqual(sgf.serialise_sgf_game(g2),
                   "(;FF[4]GM[1]PL[W]SZ[9];W[aa];B[ab])\n")
    g3 = sgf.sgf_game_from_string("(;AW[bc]FF[4]GM[1]SZ[9];B[aa];W[ab])")
    sgf_moves.indicate_first_player(g3)
    tc.assertEqual(sgf.serialise_sgf_game(g3),
                   "(;FF[4]AW[bc]GM[1]PL[B]SZ[9];B[aa];W[ab])\n")
