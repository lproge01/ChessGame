
from board import Board
from pieces import Pawn, Rook, Knight, Bishop, King, Queen

class Game:
    def __init__(self):
        self.board = Board()
        self.turn = "White"             # white always goes first
        self.selected_piece = None
        self.en_passant_target = None
        self.winner = None
        self.is_over = False

    # change turn
    def switch_turn(self):
        self.turn = "Black" if self.turn == "White" else "White"

    # castling logic
    def handle_castling(self, king_row, king_col, rook_row, rook_col):
        king = self.board.board_positions[king_row][king_col]["piece"]  
        rook = self.board.board_positions[rook_row][rook_col]["piece"]
        if (king.side != self.turn) or king.side != rook.side:          # make sure it is your turn
            return
        if not isinstance(king, King) or not isinstance(rook, Rook):    # ensure selected piece is a king or rook
            return
        if king.move_count != 0 and rook.move_count != 0:               # cannot castle if king or rook has moved
            return
        # spaces between king and rook need to be empty
        # king cannot be in check
        ##### WIP #####

    # promote pawn to another piece
    def handle_promotion(self, row, column):
        pass
    ##### WIP #####
        

    # check for checkmate - in check with no valid moves
    def is_checkmate(self):
        # choose the list of your sides pieces
        pieces = self.board.white_pieces if self.turn == "White" else self.board.black_pieces
        if self.board.is_in_check(self.turn):               # function that looks for check
            for piece in pieces:                            
                moves = piece.get_valid_moves(self.board)   # check valid moves
                if moves:                                   # if not empty there are valid moves so no checkmate
                    return False

            self.winner = "Black" if self.turn == "White" else "White"  # winner is the opposite of whose turn it is since turn switches immediatley after a move
            self.is_over = True                                         # bool for ending game
            return True
            
        return False

    # check for stalemate - not in check but no valid moves
    def is_stalemate(self):
        pieces = self.board.white_pieces if self.turn == "White" else self.board.black_pieces
        if not self.board.is_in_check(self.turn):           # looks to see if the there isn't check
            for piece in pieces:
                moves = piece.get_valid_moves(self.board)   # check the valid moves
                if moves:                                   # if there are valid moves no stalemate
                    return False
            self.winner = "Draw"
            self.is_over = True
            return True

        return False
    

        
    
                