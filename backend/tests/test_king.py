import unittest
from api.piece.king import King
from api.chess_game import ChessGame
from api.piece.piece_interface import Color
from api.piece.rook import Rook
from api.piece.knight import Knight
from api.piece.queen import Queen
from api.piece.empty import Empty


class TestRook(unittest.TestCase):
    def setUp(self) -> None:
        fen = "8/8/8/8/8/8/8/8 w KQkq - 0 1"
        self.chess_game = ChessGame(fen=fen)     # empty board
        self.chess_game.board[4][4] = King(self.chess_game, Color.WHITE, 4, 4)
        self.chess_game.board[4][1] = King(self.chess_game, Color.BLACK, 4, 1)
        self.chess_game.kings_coordinate = [(4, 4), (4, 1)]
        self.chess_game.board[3][3] = Rook(self.chess_game, Color.BLACK, 3, 3)
        self.chess_game.board[3][2] = Rook(self.chess_game, Color.WHITE, 3, 2)

    def test_get_moves(self):
        actual = self.chess_game.board[4][4].get_moves()
        expected = [(5, 4),
                    (5, 5),
                    (4, 5),
                    (3, 5),
                    (3, 4),
                    (3, 3),
                    (4, 3),
                    (5, 3)]
        for item in actual:
            self.assertTrue(item in expected)

    def test_get_color(self):
        actual_w = self.chess_game.board[4][4].color
        actual_b = self.chess_game.board[3][3].color
        expected_w = Color.WHITE
        expected_b = Color.BLACK
        self.assertEqual(actual_w, expected_w)
        self.assertEqual(actual_b, expected_b)

    def test_to_string(self):
        actual_w = self.chess_game.board[4][4].to_string()
        actual_b = self.chess_game.board[4][1].to_string()
        expected_w = "K"
        expected_b = "k"
        self.assertEqual(actual_w, expected_w)
        self.assertEqual(actual_b, expected_b)

    def test_get_checked_moves(self):
        actual = self.chess_game.board[4][4].get_checked_moves()
        expected = {"moves": [(5, 4),
                              (5, 5),
                              (4, 5),
                              (3, 3)]}
        self.assertEqual(actual, expected)

    def test_get_checked_moves_include_castling(self):
        fen = "8/8/8/8/8/8/8/8 w KQkq - 0 1"
        chess_game2 = ChessGame(fen=fen)
        chess_game2.board[0][4] = King(chess_game2, Color.WHITE, 0, 4)
        chess_game2.board[7][4] = King(chess_game2, Color.BLACK, 7, 4)
        chess_game2.board[0][7] = Rook(chess_game2, Color.WHITE, 0, 7)
        chess_game2.board[0][0] = Rook(chess_game2, Color.WHITE, 0, 0)
        actual = chess_game2.board[0][4].get_checked_moves()
        expected = {'moves': [(1, 4),
                              (1, 5),
                              (0, 5),
                              (0, 3),
                              (1, 3),
                              (0, 6),
                              (0, 2)]}
        self.assertEqual(actual, expected)


class TestCastlingFunctions(unittest.TestCase):
    def setUp(self) -> None:
        fen = "8/8/8/8/8/8/8/8 w KQkq - 0 1"
        self.chess_game = ChessGame(fen=fen)  # empty board
        self.chess_game.board[0][4] = King(self.chess_game, Color.WHITE, 0, 4)
        self.chess_game.board[0][7] = Rook(self.chess_game, Color.WHITE, 0, 7)
        self.chess_game.board[0][0] = Rook(self.chess_game, Color.WHITE, 0, 0)
        self.chess_game.board[7][4] = King(self.chess_game, Color.BLACK, 7, 4)
        self.chess_game.board[7][0] = Rook(self.chess_game, Color.BLACK, 7, 0)

    def test_rook_has_moved_not_first_move(self):
        king = self.chess_game.board[0][0]
        king.firstMove = False
        self.assertTrue(self.chess_game.board[0][4].rook_has_moved(king_side=False))

    def test_rook_has_moved_not_exist(self):
        self.chess_game.board[0][7] = Empty(self.chess_game, Color.EMPTY, 0, 7)
        self.assertTrue(self.chess_game.board[0][4].rook_has_moved(king_side=True))

    def test_pieces_between_king_and_rook(self):
        king = self.chess_game.board[7][4]
        self.chess_game.board[7][1] = Knight(self.chess_game, Color.BLACK, 7, 1)
        self.assertTrue(king.pieces_between_king_and_rook(king_side=False))

        king = self.chess_game.board[0][4]
        self.chess_game.board[0][5] = Knight(self.chess_game, Color.BLACK, 0, 5)
        self.assertTrue(king.pieces_between_king_and_rook(king_side=True))

    def test_into_checked(self):
        king = self.chess_game.board[0][4]
        self.chess_game.board[7][3] = Rook(self.chess_game, Color.BLACK, 7, 3)
        self.assertTrue(king.into_checked(king_side=False))

    def test_castling_being_checked(self):
        king = self.chess_game.board[0][4]
        self.chess_game.kings_coordinate = [(0, 4), (7, 4)]
        self.chess_game.board[6][4] = Rook(self.chess_game, Color.BLACK, 6, 4)
        self.assertFalse(king.castling(king_side=True))

    def test_castling_king_has_moved(self):
        king = self.chess_game.board[0][4]
        self.chess_game.kings_coordinate = [(0, 4), (7, 4)]
        king.firstMove = False
        self.assertFalse(king.castling(king_side=True))

    def test_castling_available(self):
        king = self.chess_game.board[0][4]
        self.chess_game.kings_coordinate = [(0, 4), (7, 4)]
        self.assertTrue(king.castling(king_side=True))
        self.assertTrue(king.castling(king_side=False))

    def test_castling_into_checked(self):
        king = self.chess_game.board[0][4]
        self.chess_game.kings_coordinate = [(0, 4), (7, 4)]
        self.chess_game.board[4][6] = Queen(self.chess_game, Color.BLACK, 4, 6)
        self.assertFalse(king.castling(king_side=True))
        self.assertFalse(king.castling(king_side=False))

    def test_castling_pieces_between_king_and_rook(self):
        king = self.chess_game.board[0][4]
        self.chess_game.kings_coordinate = [(0, 4), (7, 4)]
        self.chess_game.board[0][3] = Queen(self.chess_game, Color.WHITE, 0, 3)
        self.assertFalse(king.castling(king_side=False))

    def test_castling_rook_has_moved(self):
        king = self.chess_game.board[0][4]
        self.chess_game.kings_coordinate = [(0, 4), (7, 4)]
        rook = self.chess_game.board[0][7]
        rook.firstMove = False
        self.assertFalse(king.castling(king_side=True))
