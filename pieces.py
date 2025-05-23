import pygame

class Piece_Super:    #super class for all pieces
    def __init__(self, name, side, row, column, board):
        self.name = name
        self.side = side
        self.column = column
        self.row = row
        self.board = board

        #set position
        self.start_position = self.get_board_position(row, column)

        #set image
        self.image = pygame.image.load(self.image_path).convert_alpha()

        #track position
        self.current_position = self.start_position

    # get piece position
    def get_board_position(self, row, column):
        self.column = column
        self.row = row
        return (row, column)
    
    # to be defined by each piece separately
    def move_validation(self):
        pass

    # uses the sub-classes move_validation to create a list of available moves
    def get_valid_moves(self, board, ignore_check = False):
        moves = []

        for next_row in range(8):
            for next_col in range(8):
                if self.move_validation(board, next_row, next_col):
                    if ignore_check:
                        moves.append((next_row, next_col))
                    else:
                        old_row, old_col = self.row, self.column                                # keep track of where the piece was
                        captured_piece = board.board_positions[next_row][next_col]["piece"]     # keep track of the piece where you are moving to

                        # simulate the move
                        board.board_positions[old_row][old_col]["piece"] = None 
                        board.board_positions[old_row][old_col]["occupied"] = False

                        self.row, self.column = next_row, next_col
                        board.board_positions[next_row][next_col]["piece"] = self
                        board.board_positions[next_row][next_col]["occupied"] = True

                        in_check = board.is_in_check(self.side)

                        self.row, self.column = old_row, old_col
                        board.board_positions[old_row][old_col]["piece"] = self
                        board.board_positions[old_row][old_col]["occupied"] = True

                        board.board_positions[next_row][next_col]["piece"] = captured_piece
                        board.board_positions[next_row][next_col]["occupied"] = bool(captured_piece)

                        if not in_check:    # add the move if it does not put the piece in check
                            moves.append((next_row, next_col))

        return moves

    # move tiles
    def move_piece(self, new_position):
        self.current_position = new_position


class Pawn(Piece_Super):
    def __init__(self, side, row, column, board):
        self.move_count = 0
        
        #choose image based on side
        if side == "White":
            self.image_path = 'assets/White Pawn.png'
        else: 
            self.image_path = 'assets/Black Pawn.png'

        super().__init__("Pawn", side, row, column, board)


    def move_validation(self, board, end_row, end_col, en_passant_target = None):
        direction = -1 if self.side == "White" else 1

        dx = end_col - self.column
        dy = end_row - self.row

        # one tile move
        if dy == direction and dx == 0:
            if not board.board_positions[end_row][end_col]["occupied"]:
                return True
            
        # two tile move
        if dx == 0 and dy == 2 * direction and self.move_count == 0:
            inter_row = self.row + direction    # can move two tiles if something is in the way
            if (not board.board_positions[inter_row][self.column]["occupied"] and 
                not board.board_positions[end_row][end_col]["occupied"]):
                return True
                
        # diagonal for capture
        if abs(dx) == 1 and dy == direction:
            target = board.board_positions[end_row][end_col]
            if target["occupied"] and target["piece"].side != self.side:
                return True
            
        # en passant capture
        if en_passant_target and (end_row, end_col) == en_passant_target:
            if dy == direction and abs(dx) == 1:
                if not board.board_positions[end_row][end_col]["occupied"]:
                    behind_row = end_row - direction
                    captured_piece = board.board_positions[behind_row][end_col]["piece"]
                    if isinstance(captured_piece, Pawn) and captured_piece.side != self.side:
                        return True

    def get_valid_moves(self, board, ignore_check = False, en_passant_target = None):
        moves = []

        for next_row in range(8):
            for next_col in range(8):
                if self.move_validation(board, next_row, next_col, en_passant_target):
                    if ignore_check:
                       moves.append((next_row, next_col))
                    else:
                        old_row, old_col = self.row, self.column                                # keep track of where the piece was
                        captured_piece = board.board_positions[next_row][next_col]["piece"]     # keep track of the piece where you are moving to

                        # simulate the move
                        board.board_positions[old_row][old_col]["piece"] = None 
                        board.board_positions[old_row][old_col]["occupied"] = False

                        self.row, self.column = next_row, next_col
                        board.board_positions[next_row][next_col]["piece"] = self
                        board.board_positions[next_row][next_col]["occupied"] = True

                        in_check = board.is_in_check(self.side)

                        self.row, self.column = old_row, old_col
                        board.board_positions[old_row][old_col]["piece"] = self
                        board.board_positions[old_row][old_col]["occupied"] = True

                        board.board_positions[next_row][next_col]["piece"] = captured_piece
                        board.board_positions[next_row][next_col]["occupied"] = bool(captured_piece)

                        if not in_check:    # add the move if it does not put the piece in check
                            moves.append((next_row, next_col))

       
        return moves
            
class Rook(Piece_Super):
    def __init__(self, side, row, column, board):
        self.move_count = 0
        
        #choose image based on side
        if side == "White":
            self.image_path = 'assets/White Rook.png'
        else: 
            self.image_path = 'assets/Black Rook.png'

        super().__init__("Rook", side, row, column, board)

    def move_validation(self, board, end_row, end_col):
        if self.row == end_row and self.column == end_col:
            return False
        
        directions = [(-1,0), (1,0), (0,1), (0,-1)] # directions rook can move

        for dy, dx in directions:
            r = self.row
            c = self.column

            while True:     # loop through all tiles valid directions for rook
                r += dy
                c += dx

                if r < 0 or r >= 8 or c < 0 or c >= 8:  # looks backwards but it works
                    break

                if r == end_row and c == end_col:
                    target = board.board_positions[r][c]
                    if target["occupied"]:
                        if target["piece"] and target["piece"].side == self.side:   # can't capture your own piece
                            return False
                    return True
                
                if board.board_positions[r][c]["occupied"]:     # can't move through another piece
                    break
        
        return False

class Knight(Piece_Super):
    def __init__(self, side, row, column, board):
        self.move_count = 0
        
        #choose image based on side
        if side == "White":
            self.image_path = 'assets/White Knight.png'
        else: 
            self.image_path = 'assets/Black Knight.png'
        
        super().__init__("Knight", side, row, column, board)

    def move_validation(self, board, end_row, end_col):
        if self.row == end_row and self.column == end_col:
            return False
        
        directions = [(2,1), (1,2), (-2,1), (-1,2), (2,-1), (1, -2), (-2,-1), (-1,-2)]

        for dy, dx in directions:
            r = self.row + dy
            c = self.column + dx

            if r < 0 or r >= 8 or c < 0 or c >=8:
                continue

            if r == end_row and c == end_col:
                target = board.board_positions[r][c]
                if target["occupied"]:
                    if target["piece"] and target["piece"].side == self.side:
                        return False
                return True
                
            if board.board_positions[r][c]["occupied"]:
                    continue
        
        return False
        
class Bishop(Piece_Super):
    def __init__(self, side, row, column, board):
        self.move_count = 0
        
        #choose image based on side
        if side == "White":
            self.image_path = 'assets/White Bishop.png'
        else: 
            self.image_path = 'assets/Black Bishop.png'

        super().__init__("Bishop", side, row, column, board)

    def move_validation(self, board, end_row, end_col):
        if self.row == end_row and self.column == end_col:
            return False
        
        directions = [(-1,1), (-1,-1), (1,1), (1,-1)]

        for dy, dx in directions:
            r = self.row
            c = self.column

            while True:
                r += dy
                c += dx

                if r < 0 or r >= 8 or c < 0 or c >= 8:
                    break

                if r == end_row and c == end_col:
                    target = board.board_positions[r][c]
                    if target["occupied"]:
                        if target["piece"] and target["piece"].side == self.side:
                            return False
                    return True
                
                if board.board_positions[r][c]["occupied"]:
                    break
        
        return False


class Queen(Piece_Super):
    def __init__(self, side, row, column, board):
        self.move_count = 0
        
        #choose image based on side
        if side == "White":
            self.image_path = 'assets/White Queen.png'
        else: 
            self.image_path = 'assets/Black Queen.png'

        super().__init__("Queen", side, row, column, board)

    def move_validation(self, board, end_row, end_col):
        if self.row == end_row and self.column == end_col:
            return False
        
        directions = [(-1,0), (1,0), (0,1), (0,-1), (-1,1), (-1,-1), (1,1), (1,-1)]

        for dy, dx in directions:
            r = self.row
            c = self.column

            while True:
                r += dy
                c += dx

                if r < 0 or r >= 8 or c < 0 or c >= 8:
                    break

                if r == end_row and c == end_col:
                    target = board.board_positions[r][c]
                    if target["occupied"]:
                        if target["piece"] and target["piece"].side == self.side:
                            return False
                    return True
                
                if board.board_positions[r][c]["occupied"]:
                    break
        
        return False


class King(Piece_Super):
    def __init__(self, side, row, column, board):
        self.move_count = 0
        
        #choose image based on side
        if side == "White":
            self.image_path = 'assets/White King.png'
        else: 
            self.image_path = 'assets/Black King.png'

        super().__init__("King", side, row, column, board)

    

    def move_validation(self, board, end_row, end_col):
        if self.row == end_row and self.column == end_col:
            return False
        
        directions = [(-1,0), (1,0), (0,1), (0,-1), (-1,1), (-1,-1), (1,1), (1,-1)]

        for dy, dx in directions:
            r = self.row + dy
            c = self.column + dx

            
            if r < 0 or r >= 8 or c < 0 or c >= 8:
                continue

            if r == end_row and c == end_col:
                target = board.board_positions[r][c]
                if target["occupied"]:
                    if target["piece"] and target["piece"].side == self.side:
                        return False
                return True
                
            if board.board_positions[r][c]["occupied"]:
                    continue
        
        return False
    

    def get_valid_moves(self, board, ignore_check=False):
        moves = []
        directions = [(-1,0), (1,0), (0,1), (0,-1), (-1,1), (-1,-1), (1,1), (1,-1)]

        for dy, dx in directions:
            r = self.row + dy
            c = self.column + dx

            if 0 <= r < 8 and 0 <= c < 8:
                target = board.board_positions[r][c]
                if not target["occupied"] or target["piece"].side != self.side:
                    if ignore_check:
                        moves.append((r, c))
                    else:
                        old_row, old_col = self.row, self.column
                        captured_piece = board.board_positions[r][c]["piece"]

                        board.board_positions[old_row][old_col]["piece"] = None
                        self.row, self.column = r, c
                        board.board_positions[r][c]["piece"] = self

                        in_check = board.is_in_check(self.side)

                        # Undo simulation
                        self.row, self.column = old_row, old_col
                        board.board_positions[old_row][old_col]["piece"] = self
                        board.board_positions[r][c]["piece"] = captured_piece

                        if not in_check:
                            moves.append((r, c))

        # castling
        if not ignore_check and self.move_count == 0 and not board.is_in_check(self.side):
            row = self.row

        # Kingside (rook on col 7)
            if isinstance(board.board_positions[row][7]["piece"], Rook):
                rook = board.board_positions[row][7]["piece"]
                if rook.side == self.side and rook.move_count == 0:
                    if all(not board.board_positions[row][c]["occupied"] for c in [5, 6]):
                        safe = True
                        for col in [5, 6]:
                            self.column = col
                            board.board_positions[row][col]["piece"] = self
                            board.board_positions[row][col]["occupied"] = True
                            board.board_positions[self.row][4]["piece"] = None
                            board.board_positions[self.row][4]["occupied"] = False
                            if board.is_in_check(self.side):
                                safe = False
                            board.board_positions[row][col]["piece"] = None
                            board.board_positions[row][col]["occupied"] = False
                            board.board_positions[self.row][4]["piece"] = self
                            board.board_positions[self.row][4]["occupied"] = True
                            self.column = 4
                            if not safe:
                                break
                        if safe:
                            moves.append((row, 6))  # king moves to col 6

            # Queenside (rook on col 0)
            if isinstance(board.board_positions[row][0]["piece"], Rook):
                rook = board.board_positions[row][0]["piece"]
                if rook.side == self.side and rook.move_count == 0:
                    if all(not board.board_positions[row][c]["occupied"] for c in [1, 2, 3]):
                        safe = True
                        for col in [3, 2]:
                            self.column = col
                            board.board_positions[row][col]["piece"] = self
                            board.board_positions[row][col]["occupied"] = True
                            board.board_positions[self.row][4]["piece"] = None
                            board.board_positions[self.row][4]["occupied"] = False
                            if board.is_in_check(self.side):
                                safe = False
                            board.board_positions[row][col]["piece"] = None
                            board.board_positions[row][col]["occupied"] = False
                            board.board_positions[self.row][4]["piece"] = self
                            board.board_positions[self.row][4]["occupied"] = True
                            self.column = 4
                            if not safe:
                                break
                        if safe:
                            moves.append((row, 2)) # king moves to col 2

        return moves
