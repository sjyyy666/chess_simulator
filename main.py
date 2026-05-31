import copy

SUCCESS = 1
NOT_SUCCESS = 0
CASTLE_SUCCESS = 2
EN_PASSANT = 2
POSITIVE_STEP = 1
TWO_P_STEP = POSITIVE_STEP * 2
NEGATIVE_STEP = - POSITIVE_STEP
TWO_N_STEP = NEGATIVE_STEP * 2
EMPTY = ''
NAME_IDX = 1
SIDE_IDX = 2
MAX_RAN = 8
MIN_RAN = 1
PLAYER_MOVEMENT = 1
POTENTIAL_MOVEMENT = 0
KING = 'k'
QUEEN = 'q'
ROOK = 'r'
BISHOP = 'b'
KNIGHT = 'n'
PAWN = 'p'
WHITE = 'w'
BLACK = 'b'
COLUMN = 'c'
ROW = 'r'
ROUND_LIST = 'round list'
PAWN_LIST = 'pawn list'
KING_RULE_EXPLAINATION = ' Usually, a king moves exactly one square adjacent to it.'
QUEEN_RULE_EXPLAINATION = ' The queen moves any number of vacant squares horizontally, vertically, or diagonally.'
ROOK_RULE_EXPLAINATION = ' A rook moves any number of vacant squares horizontally or vertically.'
BISHOP_RULE_EXPLAINATION = ' A bishop moves any number of vacant squares diagonally.'
KNIGHT_RULE_EXPLAINATION = ' A knight moves to one of the nearest squares not on the same rank, file, or diagonal.'
PAWN_RULE_EXPLAINATION = ' Usually, a pawn can only move one step onwards.'
INVALID_POSITION = 'Please enter a valid position with integers between 1-8.'
PIECE_NOT_FOUNT = ' There is no piece on the position.'
SIDE_INCORRECT = ' This is the wrong side.'
POSITION_NOT_CHANGED = ' You need to change the position.'
POSITION_TAKEN = ' The position is already taken.'
KING_ATTACK = ' Your king is being attacked.'
TRY_AGAIN = ' Try again.'
ILLEGAL_MOVE = 'The move was illegal.'
# a chess board is 8*8
# Naming of pieces
# The first index is a letter that stands for the name
# k: king, q: queen, r: rook, b: bishop, n: knight, p: pawn.
# The second index is a letter that stands for the side
# w: white side, b: black side.
# The third index is a number that help distinguish pieces 
# same in sides and names
# Note: the last columns are always blank, only for format use.
START_BOARD = [['', 'col 1', 'col 2', 'col 3', 'col 4', 'col 5', 'col 6', 'col 7', 'col 8', ''], 
                ['row 1', ' rb1 ', ' nb1 ', ' bb1 ', ' qb1 ', ' kb1 ', ' bb2 ', ' nb2 ', ' rb2 ', ''], 
                ['row 2', ' pb1 ', ' pb2 ', ' pb3 ', ' pb4 ', ' pb5 ', ' pb6 ', ' pb7 ', ' pb8 ', ''], 
                ['row 3', '', '', '', '', '', '', '', '', ''], 
                ['row 4', '', '', '', '', '', '', '', '', ''], 
                ['row 5', '', '', '', '', '', '', '', '', ''], 
                ['row 6', '', '', '', '', '', '', '', '', ''],
                ['row 7', ' pw1 ', ' pw2 ', ' pw3 ', ' pw4 ', ' pw5 ', ' pw6 ', ' pw7 ', ' pw8 ', ''],
                ['row 8', ' rw1 ', ' nw1 ', ' bw1 ', ' qw1 ', ' kw1 ', ' bw2 ', ' nw2 ', ' rw2 ', '']]


# TEST_BOARD = [['', 'col 1', 'col 2', 'col 3', 'col 4', 'col 5', 'col 6', 'col 7', 'col 8', ''], 
#                ['row 1', '', '', ' bb1 ', '', '', '', '', '', ''], 
#                ['row 2', '', '', '', '', '', '', '', ' qw1 ', ''], 
#                ['row 3', '', '', '', '', '', '', ' kb1 ', '', ''], 
#                ['row 4', '', '', '', '', ' kw1 ', '', '', '', ''], 
#                ['row 5', '', '', ' pb3 ', '', ' nw1 ', '', '', '', ''], 
#                ['row 6', '', '', '', ' pb4 ', '', '', '', '', ''],
#                ['row 7', '', ' pw2 ', '', ' pw4 ', '', '', ' pw7 ', '', ''],
#                ['row 8', ' rw1 ', '', '', '', ' bw1 ', '', '', ' rw2 ', '']]

chess_board = START_BOARD
# Keep track of some conditions to check later successful moves.
conditions = {'kw1': {'moved': 0}, 
              'kb1': {'moved': 0},
              'rb1': {'moved': 0},
              'rb2': {'moved': 0},
              'rw1': {'moved': 0},
              'rw2': {'moved': 0}}

en_passant = {ROUND_LIST: [], PAWN_LIST: []}
king_position = {WHITE: 0, BLACK: 0}

# Print chess board on terminal in a readable format.
def print_chess_board(chess_board):
    for i in chess_board:
        for j in i:
            print(f'|{j:5.5s}', end = '')
        print('')
    return

# Check all the position provided was in the range.
def valid_position(row, col):
    if row >= MIN_RAN and row <= MAX_RAN and col >= MIN_RAN and col <= MAX_RAN:
        return SUCCESS
    print(INVALID_POSITION)
    return NOT_SUCCESS

# This function identifies the piece that is going to be moved by the location.
def type_identify(row, col, board):
    if board[row][col] == EMPTY:
        return NOT_SUCCESS
    else:
        return board[row][col][NAME_IDX]
    
# This function identifies the side of piece matches with the round.
def side_identify(row, col, round, board):
    if round % 2 == 1:
        if board[row][col][SIDE_IDX] == WHITE:
            return SUCCESS
    else:
        if board[row][col][SIDE_IDX] == BLACK:
            return SUCCESS
    return NOT_SUCCESS

def find_king_position(board, side):
    for i in range(1, 9):
        for j in range(1, 9):
            if board[i][j] != EMPTY and board[i][j][NAME_IDX] == KING and board[i][j][SIDE_IDX] == side:
                return [i, j]
    return

# This function identifies whether the movement of the piece is successful.
def movement_successful(ini_row, ini_col, new_row, new_col, board, king_position, round, player_movement):

    row_change = ini_row - new_row
    col_change = ini_col - new_col

    # Identify the type of piece being moved, then check if player broke the rule.
    name = type_identify(ini_row, ini_col, board)
    castle_move = NOT_SUCCESS
    en_pass_move = NOT_SUCCESS

    if name == NOT_SUCCESS:
        return PIECE_NOT_FOUNT
    elif player_movement and not side_identify(ini_row, ini_col, round, board):
        return SIDE_INCORRECT
    elif row_change == 0 and col_change == 0:
        return POSITION_NOT_CHANGED
    
    elif name == KING:
        movement = king_movement_successful(ini_row, ini_col, row_change, col_change, board)
        if not movement:
            return KING_RULE_EXPLAINATION
        elif movement == CASTLE_SUCCESS:
            castle_move = SUCCESS

    elif name == QUEEN:
        if not queen_movement_successful(board, ini_row, ini_col, new_row, new_col, row_change, col_change):
            return QUEEN_RULE_EXPLAINATION
    elif name == ROOK:
        if not rook_movement_successful(board, ini_row, ini_col, new_row, new_col, row_change, col_change):
            return ROOK_RULE_EXPLAINATION
    elif name == BISHOP:
        if not bishop_movement_successful(board, ini_row, ini_col, new_row, new_col, row_change, col_change):
            return BISHOP_RULE_EXPLAINATION
    elif name == KNIGHT:
        if not knight_movement_successful(row_change, col_change):
            return KNIGHT_RULE_EXPLAINATION
    else:

        movement = pawn_movement_successful(ini_row, ini_col, new_row, new_col, row_change, col_change, round, board)
        if not movement:
            return PAWN_RULE_EXPLAINATION
        elif movement == EN_PASSANT:
            en_pass_move = SUCCESS
    
    # Check if there's other piece on the board and if it is the same side.
    if board[new_row][new_col] != EMPTY:
        if board[ini_row][ini_col][SIDE_IDX] == board[new_row][new_col][SIDE_IDX]:
            return POSITION_TAKEN
        
    # Finally, check if the movement could cause the king directly being attacked.
    # Stimulate the new chess board
    king_moved = 0
    rook_moved = 0
    new_board = copy.deepcopy(board)

    if not player_movement:
        return SUCCESS

    process_movement(ini_row, ini_col, new_row, new_col, new_board)
    side = new_board[new_row][new_col][SIDE_IDX]
    oppo_side = opposite_side(side)

    # Keep track of king's position if king was moved.
    if new_board[new_row][new_col][NAME_IDX] == KING:
        update_king_position(king_position, new_board)
        king_moved = 1

        # Keep track of conditions for king castling
        if player_movement:
            conditions[new_board[new_row][new_col][1:4]]['moved'] += 1

    elif new_board[new_row][new_col][NAME_IDX] == ROOK and player_movement:
        conditions[new_board[new_row][new_col][1:4]]['moved'] += 1
        rook_moved = 1

    elif en_pass_move:
        if side == WHITE:
            new_board[new_row + POSITIVE_STEP][new_col] = EMPTY
        else:
            new_board[new_row + NEGATIVE_STEP][new_col] = EMPTY

    # Find all potential positions of pieced from the other side
    potential_positions = find_potential_positions(new_board, oppo_side, round)
    temp_king_position = find_king_position(new_board, side)
    if temp_king_position in potential_positions:

        if king_moved:
            conditions[new_board[new_row][new_col][1:4]]['moved'] -= 1

        if rook_moved and player_movement:
            conditions[new_board[new_row][new_col][1:4]]['moved'] -= 1

        return KING_ATTACK
    
    # If a pawn movement was successful, check if promotion applies.
    if name == PAWN and (new_row == MIN_RAN or new_row == MAX_RAN):
        if player_movement:
            print("You can now promote your pawn.")
            new_piece = input("Please enter q for queen, r for rook, b for bishop, or n for knight: ")
            for i in range(0, 9):
                new_name = ' ' + new_piece + chess_board[ini_row][ini_col][SIDE_IDX] + f'{i} '
                for j in range(1, 8):
                    if new_name in chess_board[j]:
                        break
                chess_board[ini_row][ini_col] = new_name
                break

    # Process the rook's castle movement:
    if castle_move and player_movement:
        if new_col == 3:
            process_movement(ini_row, MIN_RAN, ini_row, new_col + POSITIVE_STEP, chess_board)
        else:
            process_movement(ini_row, MAX_RAN, ini_row, MAX_RAN + TWO_N_STEP, chess_board)

    # Process enpassant attack
    if en_pass_move and player_movement:
        if side == WHITE:
            board[new_row + POSITIVE_STEP][new_col] = EMPTY
        else:
            board[new_row + NEGATIVE_STEP][new_col] = EMPTY

    return SUCCESS

def process_movement(ini_row, ini_col, new_row, new_col, board):
    board[new_row][new_col] = board[ini_row][ini_col]
    board[ini_row][ini_col] = EMPTY
    return board

# Calculate the step between two positions (in rows or columns)
def calc_step(ini, new):
    if ini - new > 0:
        return NEGATIVE_STEP
    else:
        return POSITIVE_STEP

# Print when the movement violates the piece's rule.
def print_failure_rule(rule_str):
    print(ILLEGAL_MOVE + rule_str + TRY_AGAIN)
    return

def king_movement_successful(ini_row, ini_col, row_change, col_change, board):

    if row_change <= POSITIVE_STEP and row_change >= NEGATIVE_STEP\
        and col_change <= POSITIVE_STEP and col_change >= NEGATIVE_STEP:
        return SUCCESS
    
    # Compute all possible kingside and queenside rook destinations relative to king.
    # If found the correct relative position between king and rook, further check
    # if king and rook have't moved before, there's nothing in between, and king will
    # not be attacked while moving.
    
    elif row_change == 0 and (col_change == TWO_N_STEP or col_change == TWO_P_STEP):
        pairs = under_castle_condition(conditions)
        
        if ini_col == 5: # Ensure index not out of range.

            king_side_rook = chess_board[ini_row][ini_col - col_change + POSITIVE_STEP]
            queen_side_rook = chess_board[ini_row][ini_col - col_change + TWO_N_STEP]
            king = chess_board[ini_row][ini_col]

            if king_side_rook != EMPTY and king_side_rook[NAME_IDX] == ROOK:
                rook_col = ini_col - col_change + POSITIVE_STEP
                if castle_check(king, king_side_rook, pairs, rook_col, board):
                    return CASTLE_SUCCESS
               
            if queen_side_rook != EMPTY and queen_side_rook[NAME_IDX] == ROOK:
                rook_col = ini_col - col_change + TWO_N_STEP
                if castle_check(king, queen_side_rook, pairs, rook_col, board):
                    return CASTLE_SUCCESS
    
    return NOT_SUCCESS

# Check there's nothing in between, and king will not be attacked while moving.
def castle_check(king, rook, pairs, rook_col, board):
    rook_pair = [king[NAME_IDX: 4], rook[NAME_IDX: 4]]
    if rook_pair in pairs:
                    
        step = calc_step(ini_col, rook_col)
        for i in range(ini_col, rook_col, step):

            if board[ini_row][i] != EMPTY and i != ini_col:
                return NOT_SUCCESS
                        
            new_board = copy.deepcopy(board)
            new_board[ini_row][i] = new_board[ini_row][ini_col]
            new_board[ini_row][ini_col] = EMPTY
            side = opposite_side(king[SIDE_IDX])
            potential_positions = find_potential_positions(board, side, round)
            current_king_position = new_board[ini_row][i]

            if current_king_position in potential_positions:
                return NOT_SUCCESS
            

        return SUCCESS

# Reeturn a list with all king rook pair that haven't moved previously.
def under_castle_condition(conditions):
    king_rook_pair = []
    for king in ['kb1', 'kw1']:
        if conditions[king]['moved'] == 0:
            for rook in ['rb1', 'rb2', 'rw1', 'rw2']:
                if conditions[rook]['moved'] == 0:
                    king_rook_pair.append([king, rook])
    return king_rook_pair


def queen_movement_successful(board, ini_row, ini_col, new_row, new_col, row_change, col_change):
    if rook_movement_successful(board, ini_row, ini_col, new_row, new_col, row_change, col_change):
        return SUCCESS
    elif bishop_movement_successful(board, ini_row, ini_col, new_row, new_col, row_change, col_change):
        return SUCCESS
    else:
        return NOT_SUCCESS

def rook_movement_successful(board, ini_row, ini_col, new_row, new_col, row_change, col_change):
    # Must be a straight line
    if row_change != 0 and col_change != 0:
        return NOT_SUCCESS
    
    # Check whether the rook is moving in row or column
    if row_change != 0:
        ini = ini_row
        new = new_row
        fixed = COLUMN
    else:
        ini = ini_col
        new = new_col
        fixed = ROW

    # Check if there's any piece in the way
    step = calc_step(ini, new)
    for i in range(ini + step, new, step):
        if fixed == COLUMN:
            if board[i][new_col] != EMPTY:
                return NOT_SUCCESS
        else:
            if board[new_row][i] != EMPTY:
                return NOT_SUCCESS
    return SUCCESS

def bishop_movement_successful(board, ini_row, ini_col, new_row, new_col, row_change, col_change):
    # A bishop moves any number of vacant squares diagonally.
    if row_change != col_change and row_change != -col_change:
        return NOT_SUCCESS
    
    # Check if there's any piece in the way
    row_step = calc_step(ini_row, new_row)
    col_step = calc_step(ini_col, new_col)
    temp_row = ini_row
    temp_col = ini_col
    max_row = row_change - POSITIVE_STEP
    for i in range(0, max_row):
        temp_row += row_step
        temp_col += col_step
        if board[temp_row][temp_col] != EMPTY:
            return NOT_SUCCESS
    return SUCCESS

def knight_movement_successful(row_change, col_change):
    if (row_change == NEGATIVE_STEP or row_change == POSITIVE_STEP)\
        and (col_change == TWO_N_STEP or col_change == TWO_P_STEP):
        return SUCCESS
    elif (row_change == TWO_N_STEP or row_change == TWO_P_STEP)\
        and (col_change == NEGATIVE_STEP or col_change == POSITIVE_STEP):
        return SUCCESS
    return NOT_SUCCESS

def pawn_movement_successful(ini_row, ini_col, new_row, new_col, row_change, col_change, round, board):

    side = board[ini_row][ini_col][SIDE_IDX]
    if side == WHITE:
        one_row_change = POSITIVE_STEP
        two_row_change = TWO_P_STEP
        start_row = MAX_RAN + NEGATIVE_STEP

    else:
        one_row_change = NEGATIVE_STEP
        two_row_change = TWO_N_STEP
        start_row = MIN_RAN + POSITIVE_STEP

    oppo_side = opposite_side(side)
    # Check regular movement.
    if row_change == one_row_change and col_change == 0 and board[new_row][new_col] == EMPTY:
        return SUCCESS
        
    # Check attack
    elif row_change == one_row_change and (col_change == 1 or col_change == -1):
        if board[new_row][new_col] != EMPTY:
            return SUCCESS
        
        elif (round - 1) in en_passant[ROUND_LIST]:
            e_p_position = en_passant[PAWN_LIST][len(en_passant[PAWN_LIST]) - 1]
            if board[new_row][new_col] == e_p_position:
                return EN_PASSANT
        
    # Check special first movement.
    elif ini_row == start_row and\
            row_change == two_row_change and\
            board[new_row][new_col] == EMPTY and\
            board[new_row + one_row_change][new_col] == EMPTY\
            and col_change == 0:

            # Check if En Passant applicable
            if board[new_row][new_col + 1] == EMPTY and\
                board[new_row][new_col - 1] == EMPTY:
                return SUCCESS
            
            right_col = new_col + POSITIVE_STEP
            left_col = new_col + NEGATIVE_STEP

            find_enpassant_pawn(new_row, right_col, new_col, board, oppo_side, one_row_change, round)
            find_enpassant_pawn(new_row, left_col, new_col, board, oppo_side, one_row_change, round)
            return SUCCESS
            
    return NOT_SUCCESS

def find_enpassant_pawn(row, col, new_col, board, oppo_side, one_row_change, round):
    if board[row][col] != EMPTY and\
        board[row][col][NAME_IDX] == PAWN\
        and board[row][col][SIDE_IDX] == oppo_side:

            en_passant[ROUND_LIST].append(round)
            en_passant[PAWN_LIST].append(board[row + one_row_change][new_col])
    return

# Print the instruction when need.
def help_func():
    print("To move, you need to enter command as '12,34'")
    print("12 means the piece you are trying to move is at row 1 colomn 2")
    print("34 means you are trying to move the piece to row 3 colomn 4")
    print("If you forget the format, type 'help'.")
    return

# Find all potential positions of the pieces from the specific side.
def find_potential_positions(board, side, round):
    alive_list = find_all_alive(board, side)

    potential_positions = []
    for piece in alive_list:
        for i in range(1, 9):
            for j in range(1, 9):
                if movement_successful(piece[0], piece[1], i, j, board,\
                king_position, round, POTENTIAL_MOVEMENT) == SUCCESS\
                and [i,j] not in potential_positions:
                    potential_positions.append([i,j])

    return potential_positions

def find_all_alive(board, side):
    alive_list = []
    for i in range(1, 9):
        for j in range(1, 9):
            if board[i][j] != EMPTY and board[i][j][SIDE_IDX] == side:
                alive_list.append([i, j])
    return alive_list
            

# Store the two king's position in a dictionary as lists.
def update_king_position(dict, board):
    found = 0
    for i in board:
        for j in i:
            if j != EMPTY and j[NAME_IDX] == KING:
                dict[j[SIDE_IDX]] = [board.index(i), i.index(j)]
                found += 1
            if found == 2:
                return
    return

# Check if the game is over or if there is a check
def check_or_check_mate(row, col, round):
    # Find all potential positions of pieced from the other side
    side = chess_board[row][col][SIDE_IDX]
    oppo_side = opposite_side(chess_board[row][col][SIDE_IDX])
    check = NOT_SUCCESS
    potential_positions = find_potential_positions(chess_board, side, round)
    update_king_position(king_position, chess_board)

    if king_position[oppo_side] in potential_positions:
        check = SUCCESS
        print("CHECK", end = '')

    potential_positions = find_potential_positions(chess_board, oppo_side, round + 1)
    if potential_positions == []:
        if check:
            print("MATE!")
        else:
            print("SALEMATE!")
        return 0
        
    print("")
    return 1
    
# Give the opposite side of the current side
def opposite_side(side):
    if side == WHITE:
        return BLACK
    else:
        return WHITE

king_alive = 1
round = 1
print("Welcome to chess game!")
print("The current chess board looks like: ")
print_chess_board(chess_board)
update_king_position(king_position, chess_board)
help_func()

while king_alive:
    raw_position = input("Please enter your next movement: ")
    if raw_position == 'help':
        help_func()
        continue
    if len(raw_position) != 5:
        print("Invalid input. Try again.")
        continue

    ini_row = int(raw_position[0])
    ini_col = int(raw_position[1])
    new_row = int(raw_position[3])
    new_col = int(raw_position[4])

    piece = chess_board[ini_row][ini_col]
    if (not valid_position(ini_row, ini_col)) or (not valid_position(new_row, new_col)):
        continue

    out = movement_successful(ini_row, ini_col, new_row, new_col, chess_board, king_position, round, PLAYER_MOVEMENT)
    if  out != SUCCESS:
        print_failure_rule(out)
        continue
    else:
        process_movement(ini_row, ini_col, new_row, new_col, chess_board)
        print_chess_board(chess_board)

        king_alive = check_or_check_mate(new_row, new_col, round)

        round += 1

