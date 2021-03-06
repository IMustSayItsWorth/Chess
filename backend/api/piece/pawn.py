from api.piece.piece_interface import PieceInterface, Color


class Pawn(PieceInterface):
    """
    Piece Pawn
    """
    def en_passant(self, attack_col: int, row: int, col: int) -> bool:
        """
        Check if en passant is available for the capturing pawn at Coordinate(row, col)
        and the captured pawn at Coordinate(row, attack_col)
        En passant only occurred immediately after a pawn makes a move of two squares from its starting square,
        and it could have been captured by an enemy pawn had it advanced only one square.
        :param attack_col: the col of captured pawn
        :param row: the row of the capturing pawn ( same as the row of captured pawn)
        :param col: the col of the capturing pawn
        :return: True if en passant is available. Otherwise, False.
        """

        if len(self.game.history) == 0:
            return False
        last_fen = self.game.history[-1]["fen"]
        field = last_fen.split()
        en_passant_target_notation = field[3]
        if en_passant_target_notation == "-":
            return False
        if int(en_passant_target_notation[-1]) == 6:
            tar_row = int(en_passant_target_notation[-1]) - 2
        else:
            tar_row = int(en_passant_target_notation[-1])
        tar_col = ord(en_passant_target_notation[0]) - ord("a")
        if row == tar_row and abs(col - tar_col) == 1 and tar_col == attack_col:
            # and self.color != self.game.board[tar_row][tar_col]:
            return True
        return False

    def get_moves(self) -> list:
        """
        :return: a list of all available moves and captures of a pawn.
        """
        row, col = self.x, self.y
        direction = self.color.value
        moves = []

        # captures
        attack_row = row + direction
        for attack_col in [col + 1, col - 1]:
            if PieceInterface.is_valid_coord(attack_row, attack_col) and \
                    ((self.game.board[attack_row][attack_col].color not in [self.color, Color.EMPTY]) or
                     (self.en_passant(attack_col, row, col))):
                moves.append((attack_row, attack_col))

        # moves
        steps = 1
        if (self.color == Color.WHITE and row == 1) or (self.color == Color.BLACK and row == 6):
            steps = 2
        for step in range(1, steps + 1):
            ret_row = row + step * direction
            if PieceInterface.is_valid_coord(ret_row, col) and \
                    self.game.board[ret_row][col].color == Color.EMPTY:
                moves.append((ret_row, col))
            else:
                break

        return moves

    def to_string(self) -> str:
        """
        :return: "K" if the color of the piece is Color.WHITE. Otherwise, "k".
        """
        if self.color == Color.WHITE:
            return "P"
        return "p"
