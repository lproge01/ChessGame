import pygame
from pieces import Pawn, Rook, Knight, Bishop, Queen, King

class Board:
    def __init__(self, size = 60, margin = 60, border = 5):

        # board visuals
        pygame.font.init()
        self.size = size
        self.margin = margin
        self.border = border
        self.border_color = (0, 0, 0)
        self.colors = [(4, 62, 133), (138 , 96, 96)] 
        self.font = pygame.font.Font(None, 24)

        # board positions setup
        self.board_positions = [[None for _ in range(8)] for _ in range(8)]
        for row in range(8):
            for col in range(8):
                self.board_positions[row][col] = {
                    "position": f"{row},{col}",     # wow a dict in a list this couldnt possibly lead to 3 hours of debugging because i cant spell
                    "occupied": False,
                    "piece": None
                }

        # place the pieces for a standard game of chess
        self.place_pieces()

        # setup for movement
        self.selected_piece = None
        self.valid_moves = []
        self.dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0

    # draw the board
    def draw(self, screen):
        offset = self.margin
        border_offset = self.margin - self.border
        board_size = self.size * 8

        # draw the outside border
        pygame.draw.rect(screen, self.border_color, 
                         (border_offset, border_offset,
                          board_size + 2 * self.border, board_size + 2 * self.border),
                          self.border)

        # draw the board tiles
        for row_unflipped in range(8):
            row = 7 - row_unflipped # reverse direction of row
            for col in range(8):
                # draw the board
                color = self.colors[(row + col) % 2]
                rect = pygame.Rect((offset + (col * self.size), offset + (row * self.size), self.size, self.size))
                pygame.draw.rect(screen, color, rect)

                if self.selected_piece and (row, col) in self.valid_moves:  # add a green border to tiles that are within valid moves
                    pygame.draw.rect(screen, (0, 255, 0), rect, 4)

                # draw the pieces
                space = self.board_positions[row][col]
                if space["occupied"]:
                    piece = space["piece"]

                    # draw the pieces while not dragging
                    if piece != self.selected_piece or not self.dragging:   # draw the piece images
                        image_surface = piece.image  

                        xcenter = 60 + col * self.size + (self.size - image_surface.get_width()) // 2
                        ycenter = 60 + row * self.size + (self.size - image_surface.get_height()) // 2

                        screen.blit(image_surface, (xcenter, ycenter))
                
                # draw the images where your cursor is while dragging
                if self.dragging and self.selected_piece:
                    image_surface = self.selected_piece.image
                    xcenter = self.drag_offset_x - image_surface.get_width() // 2
                    ycenter = self.drag_offset_y - image_surface.get_height() // 2
                    screen.blit(image_surface, (xcenter, ycenter))

        # label the rows
        for row in range(8):
            label = self.font.render(str(8 - row), True, (0, 0, 0))
            screen.blit(label, (self.margin // 2, 10 + row * self.size + offset + self.size // 4)) # +10 to align to the center of the square

        # label the columns
        columns = "ABCDEFGH"
        for col in range(8):
            label = self.font.render(columns[col], True, (0, 0, 0))
            screen.blit(label, (10 + col * self.size + offset + self.size // 4, self.margin // 2)) # +10 to align to the center of the square


    def place_pieces(self):
        # white pawns
        for col in range(8):
            row = 6
            piece = Pawn("White", row, col, self)
            self.board_positions[row][col]["occupied"] = True
            self.board_positions[row][col]["piece"] = piece

        # black pawns
        for col in range(8):
            row = 1
            piece = Pawn("Black", row, col, self)
            self.board_positions[row][col]["occupied"] = True
            self.board_positions[row][col]["piece"] = piece

        # rooks
        self.board_positions[7][0]["occupied"] = True
        self.board_positions[7][0]["piece"] = Rook("White", 7, 0, self)

        self.board_positions[7][7]["occupied"] = True
        self.board_positions[7][7]["piece"] = Rook("White", 7, 7, self)

        self.board_positions[0][0]["occupied"] = True
        self.board_positions[0][0]["piece"] = Rook("Black", 0, 0, self)

        self.board_positions[0][7]["occupied"] = True
        self.board_positions[0][7]["piece"] = Rook("Black", 0, 7, self)
        
        # knights
        self.board_positions[7][1]["occupied"] = True
        self.board_positions[7][1]["piece"] = Knight("White", 7, 1, self)

        self.board_positions[7][6]["occupied"] = True
        self.board_positions[7][6]["piece"] = Knight("White", 7, 6, self)

        self.board_positions[0][1]["occupied"] = True
        self.board_positions[0][1]["piece"] = Knight("Black", 0, 1, self)

        self.board_positions[0][6]["occupied"] = True
        self.board_positions[0][6]["piece"] = Knight("Black", 0, 6, self)

        # bishops
        self.board_positions[7][2]["occupied"] = True
        self.board_positions[7][2]["piece"] = Bishop("White", 7, 2, self)

        self.board_positions[7][5]["occupied"] = True
        self.board_positions[7][5]["piece"] = Bishop("White", 7, 5, self)

        self.board_positions[0][2]["occupied"] = True
        self.board_positions[0][2]["piece"] = Bishop("Black", 0, 2, self)

        self.board_positions[0][5]["occupied"] = True
        self.board_positions[0][5]["piece"] = Bishop("Black", 0, 5, self)

        # queens
        self.board_positions[7][3]["occupied"] = True
        self.board_positions[7][3]["piece"] = Queen("White", 7, 3, self)

        self.board_positions[0][3]["occupied"] = True
        self.board_positions[0][3]["piece"] = Queen("Black", 0, 3, self)

        # kings
        # kings are assigned variables to keep track of for check validation
        self.white_king = King("White", 7, 4, self)     
        self.board_positions[7][4]["occupied"] = True
        self.board_positions[7][4]["piece"] = self.white_king
        
        self.black_king = King("Black", 0, 4, self)
        self.board_positions[0][4]["occupied"] = True
        self.board_positions[0][4]["piece"] = self.black_king

    # change the position of a piece
    def move_piece(self, piece, new_row, new_col, game):
        if piece.side != game.turn:     # dont move if its not their turn
            return
        
        # keep track of where the piece was and where its going
        old_row, old_col = piece.row, piece.column
        captured_piece = self.board_positions[new_row][new_col]["piece"]
        captured_occupied = self.board_positions[new_row][new_col]["occupied"]
        promo_row = 0 if piece.side == "White" else 7
        
        # en passant
        if isinstance(piece, Pawn) and game.en_passant_target == (new_row, new_col):
            direction = -1 if piece.side == "White" else 1
            captured_row = new_row - direction
            captured_piece = self.board_positions[captured_row][new_col]["piece"]

            if captured_piece:
                if captured_piece.side == "White":
                    self.white_pieces.remove(captured_piece)
                else:
                    self.black_pieces.remove(captured_piece)

            if isinstance(captured_piece, Pawn) and captured_piece.side != piece.side:
                self.board_positions[captured_row][new_col]["piece"] = None
                self.board_positions[captured_row][new_col]["occupied"] = False
        
        # castling logic
        if isinstance(piece, King) and abs(new_col - old_col) == 2:
            rook_col = 0 if new_col < old_col else 7
            game.handle_castling(old_row, old_col, old_row, rook_col)
            return
        
        # change status of the old position
        self.board_positions[old_row][old_col]["occupied"] = False
        self.board_positions[old_row][old_col]["piece"] = None
        

        piece.row = new_row     # change the pieces data
        piece.column = new_col
        self.board_positions[new_row][new_col]["occupied"] = True   # change the state of the new tile
        self.board_positions[new_row][new_col]["piece"] = piece

        # dont allow a move that puts the king in check
        if self.is_in_check(piece.side):
            piece.row, piece.column = old_row, old_col
            self.board_positions[old_row][old_col]["occupied"] = True
            self.board_positions[old_row][old_col]["piece"] = piece
            
            self.board_positions[new_row][new_col]["occupied"] = False
            self.board_positions[new_row][new_col]["piece"] = None

            self.board_positions[new_row][new_col]["occupied"] = captured_occupied
            self.board_positions[new_row][new_col]["piece"] = captured_piece

            return
        
        # pawn promotion
        if isinstance(piece, Pawn) and new_row == promo_row:
            game.promoting_pawn = piece
            self.selected_piece = None
            self.valid_moves = []
            self.dragging = False
            

        piece.move_count += 1   # increase the move count so that some moves arent possible anymore

    # put the remaining pieces on each side into a list
    def list_piece(self):
        self.white_pieces = []
        self.black_pieces = []
        for row in range(8):
            for col in range(8):    # go through the board
                piece = self.board_positions[row][col]["piece"]
                if piece != None:
                    if piece.side == "White":
                        self.white_pieces.append(piece) # add white pieces to white piece list
                    else:
                        self.black_pieces.append(piece) # add black pieces to black piece list
        return self.white_pieces, self.black_pieces

    def is_in_check(self, side):
        king = self.white_king if side == "White" else self.black_king
        king_pos = (king.row, king.column)

        for row in range(8):
            for col in range(8):    # iterate across the whole board
                space = self.board_positions[row][col]
                if space["occupied"]:
                    piece = space["piece"]
                    if piece and piece.side != side:
                        if isinstance(piece, Pawn):
                            moves = piece.get_valid_moves(self, ignore_check=True)
                        else:
                            moves = piece.get_valid_moves(self, ignore_check=True)
                        if king_pos in moves:
                            return True
                    

        return False

    #handle mouse click
    def handle_mouse_down(self, mouse_x, mouse_y, game):
        col = (mouse_x - self.margin) // self.size
        row = (mouse_y - self.margin) // self.size

        if 0 <= row < 8 and 0 <= col < 8:
            space = self.board_positions[row][col]
            if space["occupied"]:
                self.selected_piece = space["piece"]
                if self.selected_piece.side != game.turn:
                    return
                if isinstance(self.selected_piece, Pawn):
                    self.valid_moves = self.selected_piece.get_valid_moves(self, en_passant_target = game.en_passant_target)
                else:
                    self.valid_moves = self.selected_piece.get_valid_moves(self)

                self.dragging = True
                self.drag_offset_x = mouse_x
                self.drag_offset_y = mouse_y

    # handle mouse dragging
    def handle_mouse_motion(self, mouse_x, mouse_y):
        if self.dragging:
            self.drag_offset_x = mouse_x
            self.drag_offset_y = mouse_y

    # handle mouse release
    def handle_mouse_up(self, mouse_x, mouse_y, game):
        if not self.dragging or not self.selected_piece:
            return
        
        col = (mouse_x - self.margin) // self.size
        row = (mouse_y - self.margin) // self.size

        if 0 <= row < 8 and 0 <= col < 8:
            if (row, col) in self.valid_moves:
                old_row = self.selected_piece.row
                self.move_piece(self.selected_piece, row, col, game)

                # set an en passant target
                if isinstance(self.selected_piece, Pawn) and abs(row - old_row) == 2:
                    middle_row = (row + old_row) // 2
                    game.en_passant_target = (middle_row, col)

                # promotion
                if isinstance(self.selected_piece, Pawn) and (row == 0 or row == 7):
                    game.promoting_pawn = self.selected_piece
                    game.switch_turn()
                    self.selected_piece = None
                    self.valid_moves = []
                    self.dragging = False
                    return
                
                game.switch_turn()
                self.list_piece()

                if game.is_checkmate() or game.is_stalemate():
                    game.is_over = True

        self.selected_piece = None
        self.valid_moves = []
        self.dragging = False