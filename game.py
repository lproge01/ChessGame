
import pygame
from board import Board
from pieces import Pawn, Rook, Knight, Bishop, King, Queen

class Game:
    def __init__(self):
        self.board = Board()
        self.turn = "White"             # white always goes first
        self.selected_piece = None
        self.winner = None
        self.is_over = False
        self.en_passant_target = None
        self.promoting_pawn = None

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
        if king.move_count != 0 or rook.move_count != 0:               # cannot castle if king or rook has moved
            return
        if self.board.is_in_check(king.side):
            return
        
        # tiles between king and rook should be empty and king cannot move into check
        col_diff = king_col - rook_col
        direction = -1 if col_diff > 0 else 1

        start = min(king_col, rook_col) + 1
        end = max(king_col, rook_col)

        for col in range(start, end):
            if self.board.board_positions[king_row][col]["occupied"]:
                return
            
            #simulate king moving one tile at a time to see if it would pass into check
            old_col = king.column
            king.column = col

            self.board.board_positions[king_row][old_col]["piece"] = None 
            self.board.board_positions[king_row][col]["piece"] = king

            in_check = self.board.is_in_check(king.side)

            # undo simulation
            self.board.board_positions[king_row][col]["piece"] = None
            self.board.board_positions[king_row][old_col]["piece"] = king

            if in_check:
                return
            
        # determine new positions
        new_king_col = king_col + 2 * direction
        new_rook_col = king_col + direction

        # clear old positions
        self.board.board_positions[king_row][king_col]["piece"] = None
        self.board.board_positions[king_row][king_col]["occupied"] = False
        self.board.board_positions[rook_row][rook_col]["piece"] = None
        self.board.board_positions[rook_row][rook_col]["occupied"] = False

        # place king
        king.column = new_king_col
        self.board.board_positions[king_row][new_king_col]["piece"] = king
        self.board.board_positions[king_row][new_king_col]["occupied"] = True

        # place rook
        rook.column = new_rook_col
        self.board.board_positions[king_row][new_rook_col]["piece"] = rook
        self.board.board_positions[king_row][new_rook_col]["occupied"] = True

        king.move_count += 1
        rook.move_count += 1



    # promote pawn to another piece
    def handle_promotion(self, screen, mouse_x, mouse_y):
        pawn = self.promoting_pawn
        if not pawn:
            return

        bar_x = 180
        bar_y = 0 if pawn.side == "White" else 540

        self.promo_images = {
            "Rook": pygame.image.load('assets/White Rook.png' if pawn.side == "White" else 'assets/Black Rook.png'),
            "Knight": pygame.image.load('assets/White Knight.png' if pawn.side == "White" else 'assets/Black Knight.png'),
            "Bishop": pygame.image.load('assets/White Bishop.png' if pawn.side == "White" else 'assets/Black Bishop.png'),
            "Queen": pygame.image.load('assets/White Queen.png' if pawn.side == "White" else 'assets/Black Queen.png'),
        }

        # draw promotion options
        choice_background = pygame.Rect(bar_x, bar_y, 240, 60)
        pygame.draw.rect(screen, "grey", choice_background)
        buttons = {}
        for i, (name, img) in enumerate(self.promo_images.items()):
            x = bar_x + i * 60
            screen.blit(img, (x, bar_y))
            buttons[name] = pygame.Rect(x, bar_y, 60, 60)

        # handle click
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for name, rect in buttons.items():
                    if rect.collidepoint(mouse_x, mouse_y):
                        row, col = pawn.row, pawn.column
                        # Replace pawn with new piece
                        if name == "Rook":
                            new_piece = Rook(pawn.side, row, col, pawn.board)
                        elif name == "Knight":
                            new_piece = Knight(pawn.side, row, col, pawn.board)
                        elif name == "Bishop":
                            new_piece = Bishop(pawn.side, row, col, pawn.board)
                        else:
                            new_piece = Queen(pawn.side, row, col, pawn.board)

                        self.board.board_positions[row][col]["piece"] = new_piece
                        self.promoting_pawn = None  # done with promotion
                        break
                

    # check for checkmate - in check with no valid moves
    def is_checkmate(self):
        # choose the list of your sides pieces
        self.board.list_piece()
        pieces = self.board.white_pieces if self.turn == "White" else self.board.black_pieces
        if self.board.is_in_check(self.turn):               # function that looks for check
            for piece in pieces: 
                if isinstance(piece, Pawn): 
                    moves = piece.get_valid_moves(self.board, en_passant_target = self.en_passant_target)   # check valid moves
                else:
                    moves = piece.get_valid_moves(self.board)
                if moves:                                   # if not empty there are valid moves so no checkmate
                    return False

            self.winner = "Black" if self.turn == "White" else "White"  # winner is the opposite of whose turn it is since turn switches immediatley after a move
            self.is_over = True                                         # bool for ending game
            return True
            
        return False

    # check for stalemate - not in check but no valid moves
    def is_stalemate(self):
        self.board.list_piece()
        pieces = self.board.white_pieces if self.turn == "White" else self.board.black_pieces
        if not self.board.is_in_check(self.turn):           # looks to see if the there isn't check
            for piece in pieces:
                if isinstance(piece, Pawn):
                    moves = piece.get_valid_moves(self.board, en_passant_target = self.en_passant_target)   # check the valid moves
                else:
                    moves = piece.get_valid_moves(self.board)
                if moves:                                   # if there are valid moves no stalemate
                    return False
            self.winner = "Draw"
            self.is_over = True
            return True

        return False
    