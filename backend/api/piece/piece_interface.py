from enum import Enum


class Color(Enum):
    WHITE = 1
    BLACK = -1
    EMPTY = 0


class PieceInterface:
    """
    Interface that a piece should implement
    """
    def __init__(self, game: 'ChessGame', color: Color, x: int, y: int):
        """
        :param game: a chess game instance
        :param color: indicate the color of the piece
        """
        self.x = x
        self.y = y
        self.game = game
        self.color = color

    def update_coordinate(self, x: int, y: int):
        self.x = x
        self.y = y

    def get_moves(self) -> list:
        """
        This function will be implemented in each piece class.
        """
        raise NotImplementedError

    def get_checked_moves(self) -> dict:
        """
        a dictionary. Key is "moves", and value is a list of all available moves that will not
        make the same side king being checked after the move.
        """
        moves = self.get_moves()
        checked_moves = []
        if len(moves) > 0:
            coordinate = self.x, self.y
            for move in moves:
                if not self.game.is_being_checked_after_move(coordinate, move):
                    checked_moves.append(move)
        return {"moves": checked_moves}

    @staticmethod
    def is_valid_coord(row: int, col: int) -> bool:
        """
        Check if a Coordinate(row, col) is valid.
        :param row: the index of rows of the board
        :param col: the index of columns of the board
        :return: True if row and col are all equal to or greater than 0 and less than 8. Otherwise, False.
        """
        return 0 <= row < 8 and 0 <= col < 8

    def to_string(self) -> str:
        """
        This function will be implemented in each piece class.
        """
        raise NotImplementedError
