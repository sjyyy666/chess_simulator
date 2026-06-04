import copy

# NOTE: because the calculation of row and column change was set as
# initial - new, the number we use will be the opposite number to 
# actual change.
SUCCESS = 1
NOT_SUCCESS = 0
CASTLE_SUCCESS = 2
EN_PASSANT = 2
ATTACK_MOVEMENT = 0
SIMULATE_MOVEMENT = 1
POSITIVE_STEP = 1
TWO_P_STEP = POSITIVE_STEP * 2
NEGATIVE_STEP = - POSITIVE_STEP
TWO_N_STEP = NEGATIVE_STEP * 2
EMPTY = ''
NAME_IDX = 1
SIDE_IDX = 2
ROW_IDX = 0
COL_IDX = 1
NEW_ROW_IDX = 3
NEW_COL_IDX = 4
BOARD_IDX = 0
CONDITION_IDX = 1
EN_PASS_IDX = 2
ROUND_IDX = 3
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
HELP = 'help'
ROUND_LIST = 'round list'
PAWN_LIST = 'pawn list'
CHECK = 'CHECK'
CHECK_MATE = 'MATE!'
SALE_MATE = 'SALEMATE!'
MOVED = 'moved'
ROUND_NUM = 'round num'
EN_PASS_CON = 'En passant'
CONDITIONS = 'conditions'
BOARD = 'board'
BOARD_AT_ROUND = 'The chess board of round '
INVALID_ROUND = 'Please enter a valid round number'
CONFIRM_CHANGE = 'Would you like to continue go back to round '
CHOICE = ' Y/N?'
YES = 'Y'
NO = 'N'
CHANGE_ROUND = 'reverse'
ENTER_ROUND_NUM ='Please enter the round number you\'d like to reverse to'
SUCCESS_CHANGE = 'Change successful!'
WELCOME = "Welcome to chess game!"
NEXT_MOVE = "Please enter your next movement: "
HELP_STR_1 = "To move, you need to enter command as '12,34'"
HELP_STR_2 = "12 means the piece you are trying to move is at row 1 colomn 2"
HELP_STR_3 = "34 means you are trying to move the piece to row 3 colomn 4"
HELP_STR_4 = "If you forget the format, type 'help'."
HELP_STR_5 = "If you'd like to reverse to a specific round, type 'reverse'."
ROUND = 'ROUND'
INVALID_INPUT = "Invalid input. Try again."
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
PROMO_MESSAGE = "You can now promote your pawn."
PROMOTION = "Please enter q for queen, r for rook, b for bishop, or n for knight: "
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
# Keep track of king and rook movement conditions to check castling.
conditions = {' kw1 ': {'moved': 0}, 
              ' kb1 ': {'moved': 0},
              ' rb1 ': {'moved': 0},
              ' rb2 ': {'moved': 0},
              ' rw1 ': {'moved': 0},
              ' rw2 ': {'moved': 0}}

en_passant = {ROUND_LIST: [], PAWN_LIST: []}
king_position = {WHITE: 0, BLACK: 0}
memory = {ROUND_NUM: 0}

# Memorize every success movement of player
def memorize_movement(memory, round, board, conditions, en_passant):
    curr_board = copy.deepcopy(board)
    curr_condition = copy.deepcopy(conditions)
    curr_en_pass = copy.deepcopy(en_passant)
    new_memory = {BOARD: curr_board, CONDITIONS: curr_condition,\
                                EN_PASS_CON: curr_en_pass}
    memory[round] = new_memory
    memory[ROUND_NUM] += 1
    return

# Print chess board of specific round.
def view_memory(memory, past_round):
    if past_round not in memory:
        print(INVALID_ROUND)
        return NOT_SUCCESS
    
    print(BOARD_AT_ROUND + f'{past_round}')
    print_chess_board(memory[past_round][BOARD])
    return SUCCESS

# Go back to a specific round, delete memory afterwards
def go_to_memory(memory, past_round):
    if not view_memory(memory, past_round):
        return NOT_SUCCESS
    
    continue_change = 0
    while continue_change != YES and continue_change != NO:
        continue_change = input(CONFIRM_CHANGE + f'{past_round}' + CHOICE)

    if continue_change == YES:
        memory_block = memory[past_round]
        chess_board = copy.deepcopy(memory_block[BOARD])
        conditions = copy.deepcopy(memory_block[CONDITIONS])
        en_passant = copy.deepcopy(memory_block[EN_PASS_CON])
        round = past_round + 1

        for next_round in range(round, memory[ROUND_NUM]):
            del memory[next_round]

        memory[ROUND_NUM] = round
        print(SUCCESS_CHANGE)
        
        return chess_board, conditions, en_passant, round

    else:
        return NOT_SUCCESS

# Print chess board on terminal in a readable format.
def print_chess_board(chess_board):
    for row in chess_board:
        for check in row:
            print(f'|{check:5.5s}', end = EMPTY)
        print(EMPTY)
    return

# Check all the position provided was in the range.
def valid_position(row, col):
    if row >= MIN_RAN and row <= MAX_RAN and\
    col >= MIN_RAN and col <= MAX_RAN:
        return SUCCESS
    
    print(INVALID_POSITION)
    return NOT_SUCCESS

# This function identifies type of the piece on a given position.
def type_identify(row, col, board):
    piece = board[row][col]
    if piece == EMPTY:
        return NOT_SUCCESS
    else:
        return piece[NAME_IDX]
    
# Check if the side being moved matches the round.
def side_identify(row, col, round, board):

    side = board[row][col][SIDE_IDX]

    # White side moves first, round should be odd number.
    if round % 2 == 1:
        if side == WHITE:
            return SUCCESS
        
    # Round for black side should be even number.
    else:
        if side == BLACK:
            return SUCCESS
        
    return NOT_SUCCESS

# Find position of a specific black or white king
def find_king_position(board, side):
    for row in range(1, 9):
        for col in range(1, 9):

            check = board[row][col]

            if check != EMPTY and\
                check[NAME_IDX] == KING\
                and check[SIDE_IDX] == side:

                return [row, col]
    return

# Detect if movement is legal. The detection include:
# If there's no piece on the position, or no movement.
# If it is the wrong side to the round.
# If the movement is legal to the piece type.
# If the position is already taken by a piece.
# If the king of the same side will be attacked after the movement.

# Process Enpassant movement, castle movement and pawn promotion of user.
def movement_successful(ini_row, ini_col, new_row, new_col, board,\
                        round, simulate_movement, player_movement):

    row_change = ini_row - new_row
    col_change = ini_col - new_col

    name = type_identify(ini_row, ini_col, board)
    new_position = board[new_row][new_col]
    ini_position = board[ini_row][ini_col]

    castle_move = NOT_SUCCESS
    en_pass_move = NOT_SUCCESS

    # No piece on position.
    if name == NOT_SUCCESS:
        return PIECE_NOT_FOUNT
    
    # Wrong side to the round.
    elif player_movement and\
        not side_identify(ini_row, ini_col, round, board):
        return SIDE_INCORRECT
    
    # No movement being made.
    elif row_change == 0 and col_change == 0:
        return POSITION_NOT_CHANGED
    
    # Check if movement legal to the piece type.
    elif name == KING:
        movement = king_movement_successful(ini_row, ini_col,\
                row_change, col_change, board, simulate_movement)

        if not movement:
            return KING_RULE_EXPLAINATION
        elif movement == CASTLE_SUCCESS:
            castle_move = SUCCESS

    elif name == QUEEN:
        if not queen_movement_successful(board, ini_row, ini_col,\
                        new_row, new_col, row_change, col_change):
            return QUEEN_RULE_EXPLAINATION
        
    elif name == ROOK:
        if not rook_movement_successful(board, ini_row, ini_col,\
                        new_row, new_col, row_change, col_change):
            return ROOK_RULE_EXPLAINATION
        
    elif name == BISHOP:
        if not bishop_movement_successful(board, ini_row, ini_col,\
                        new_row, new_col, row_change, col_change):
            return BISHOP_RULE_EXPLAINATION
        
    elif name == KNIGHT:
        if not knight_movement_successful(row_change, col_change):
            return KNIGHT_RULE_EXPLAINATION
        
    else:
        movement = pawn_movement_successful(ini_row, ini_col,\
            new_row, new_col, row_change, col_change, round, board)
        if not movement:
            return PAWN_RULE_EXPLAINATION
        elif movement == EN_PASSANT:
            en_pass_move = SUCCESS
    
    # Check if the position is taken by a piece on the same side.
    if new_position != EMPTY:
        if ini_position[SIDE_IDX] == new_position[SIDE_IDX]:
            return POSITION_TAKEN
        
    if not simulate_movement:
        return SUCCESS
    # Check if the movement could cause the king directly being attacked.
    # Simulate the new chess board.
    # Keep track of the king and rook movementm for castling.
    king_moved = 0
    rook_moved = 0
    new_board = copy.deepcopy(board)

    process_movement(ini_row, ini_col, new_row, new_col, new_board)
    piece = new_board[new_row][new_col]
    side = piece[SIDE_IDX]
    oppo_side = opposite_side(side)
    name = piece[NAME_IDX]

    if player_movement:
        # Keep track of conditions for king movement and castling.
        if name == KING:     
            king_moved = 1
            conditions[piece][MOVED] += 1

        elif name == ROOK:
            rook_moved = 1
            conditions[piece][MOVED] += 1

    # Process Enpassant, remove the pawn being attacked.
    if en_pass_move:
        if side == WHITE:
            new_board[new_row + POSITIVE_STEP][new_col] = EMPTY
        else:
            new_board[new_row + NEGATIVE_STEP][new_col] = EMPTY

    # Check if king in potential positions of pieces from the other side.
    potential_positions = find_potential_positions(new_board,\
                            oppo_side, round, ATTACK_MOVEMENT)
    temp_king_position = find_king_position(new_board, side)

    if temp_king_position in potential_positions:

        if king_moved or rook_moved:
            conditions[piece][MOVED] -= 1

        return KING_ATTACK
    
    if not player_movement:
        return SUCCESS
    
    # If a pawn movement was successful, check if promotion applies.
    if name == PAWN and (new_row == MIN_RAN or new_row == MAX_RAN):
            
            print(PROMO_MESSAGE)
            new_piece = EMPTY

            while new_piece not in [QUEEN, ROOK, BISHOP, KNIGHT]:
                new_piece = input(PROMOTION)

            new_name = ' ' + new_piece + ini_position[SIDE_IDX] + '0 '
            chess_board[ini_row][ini_col] = new_name

    # Process the rook's castle movement:
    if castle_move:
        if col_change == TWO_P_STEP:
            process_movement(ini_row, MIN_RAN, ini_row,\
                    new_col + POSITIVE_STEP, chess_board)
        else:
            process_movement(ini_row, MAX_RAN, ini_row,\
                    MAX_RAN + TWO_N_STEP, chess_board)

    # Process enpassant attack
    if en_pass_move:
        if side == WHITE:
            board[new_row + POSITIVE_STEP][new_col] = EMPTY
        else:
            board[new_row + NEGATIVE_STEP][new_col] = EMPTY

    return SUCCESS

# Change position of a piece on the board.
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

# Notify player of the illegal movement.
def print_failure_rule(rule_str):
    print(ILLEGAL_MOVE + rule_str + TRY_AGAIN)
    return

# Check if king movement legal, including:
# - General movement of king moving one step adjacent to it.
# - Castling of king that never moved before moving two step
#   towards a rook that havn't moved before as well.
#   During movement, there shall be no pieces in between 
#   and the king must not be under attack.
def king_movement_successful(ini_row, ini_col, row_change,\
                    col_change, board, check_castle):

    # General movement
    if row_change <= POSITIVE_STEP and row_change >= NEGATIVE_STEP\
        and col_change <= POSITIVE_STEP and col_change >= NEGATIVE_STEP:
        return SUCCESS
    
    if not check_castle:
        return NOT_SUCCESS
    
    # Compute possible king and queenside rook positions relative to king.
    # If found the correct relative position between king and rook,
    # further check conditions before and during castling.
    elif row_change == 0 and (col_change == TWO_N_STEP or\
                            col_change == TWO_P_STEP):

        # All pairs of king and rook that satisfies castling.
        pairs = under_castle_condition(conditions)
        
        if ini_col == 5: # Ensure index not out of range.

            king_side_rook_col = ini_col - col_change + POSITIVE_STEP
            king_side_rook = chess_board[ini_row][king_side_rook_col]
            
            queen_side_rook_col = ini_col - col_change + TWO_N_STEP
            queen_side_rook = chess_board[ini_row][queen_side_rook_col]

            king = chess_board[ini_row][ini_col]

            if king_side_rook != EMPTY and king_side_rook[NAME_IDX] == ROOK:

                if castle_check(king, king_side_rook, pairs,\
                                king_side_rook_col, board, ini_row, ini_col):
                    return CASTLE_SUCCESS
               
            if queen_side_rook != EMPTY and queen_side_rook[NAME_IDX] == ROOK:

                if castle_check(king, queen_side_rook, pairs, \
                            queen_side_rook_col, board, ini_row, ini_col):
                    return CASTLE_SUCCESS
    
    return NOT_SUCCESS

# Return a list with all king rook pair that haven't moved previously.
def under_castle_condition(conditions):
    king_rook_pair = []
    for king in [' kb1 ', ' kw1 ']:
        if conditions[king][MOVED] == 0:
            for rook in [' rb1 ', ' rb2 ', ' rw1 ', ' rw2 ']:
                if conditions[rook][MOVED] == 0:
                    king_rook_pair.append([king, rook])
    return king_rook_pair

# For castle movement, check there's nothing in between,
# and king will not be attacked while moving.
def castle_check(king, rook, pairs, rook_col, board, ini_row, ini_col):

    # King-rook pair must be in the provided pairs list
    king_rook_pair = [king, rook]
    if king_rook_pair in pairs:
         
        step = calc_step(ini_col, rook_col)
        for col in range(ini_col, rook_col, step):

            # No piece in between.
            if board[ini_row][col] != EMPTY and col != ini_col:
                return NOT_SUCCESS
                        
            # King is not under, and will not be under attack.
            new_board = copy.deepcopy(board)
            new_board[ini_row][col] = new_board[ini_row][ini_col]
            new_board[ini_row][ini_col] = EMPTY
            side = opposite_side(king[SIDE_IDX])
            potential_positions = find_potential_positions(board,\
                                    side, round, ATTACK_MOVEMENT)
            current_king_position = new_board[ini_row][col]

            if current_king_position in potential_positions:
                return NOT_SUCCESS
            
        return SUCCESS

# The queen moves any number of vacant squares
# horizontally, vertically, or diagonally, with nothing in between.
def queen_movement_successful(board, ini_row, ini_col,\
                new_row, new_col, row_change, col_change):
    
    if rook_movement_successful(board, ini_row, ini_col,\
                new_row, new_col, row_change, col_change):
        return SUCCESS
    
    elif bishop_movement_successful(board, ini_row, ini_col,\
                    new_row, new_col, row_change, col_change):
        return SUCCESS
    
    else:
        return NOT_SUCCESS

# A rook moves any number of vacant squares
# horizontally or vertically, with nothing in between.
def rook_movement_successful(board, ini_row, ini_col, new_row,\
                             new_col, row_change, col_change):
    # Must be a straight line
    if row_change and col_change:
        return NOT_SUCCESS
    
    # Check whether the rook is moving in row or column
    if row_change:
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

# A bishop moves any number of vacant squares diagonally,
# with nothing in between.
def bishop_movement_successful(board, ini_row, ini_col, new_row,\
                               new_col, row_change, col_change):
    # A bishop moves any number of vacant squares diagonally.
    if abs(row_change) != abs(col_change):
        return NOT_SUCCESS
    
    # Check if there's any piece in the way
    row_step = calc_step(ini_row, new_row)
    col_step = calc_step(ini_col, new_col)
    temp_row = ini_row
    temp_col = ini_col
    max_row = row_change - POSITIVE_STEP
    for i in range(1, abs(row_change)):
        temp_row += row_step
        temp_col += col_step
        if board[temp_row][temp_col] != EMPTY:
            return NOT_SUCCESS
    return SUCCESS

# A knight moves to one of the nearest squares not on the same rank,
# file, or diagonal.
def knight_movement_successful(row_change, col_change):
    if (row_change == NEGATIVE_STEP or row_change == POSITIVE_STEP)\
        and (col_change == TWO_N_STEP or col_change == TWO_P_STEP):
        return SUCCESS
    elif (row_change == TWO_N_STEP or row_change == TWO_P_STEP)\
        and (col_change == NEGATIVE_STEP or col_change == POSITIVE_STEP):
        return SUCCESS
    return NOT_SUCCESS

def pawn_movement_successful(ini_row, ini_col, new_row, new_col,\
                            row_change, col_change, round, board):

    side = board[ini_row][ini_col][SIDE_IDX]
    new_pos = board[new_row][new_col]
    if side == WHITE:
        one_row_change = POSITIVE_STEP
        two_row_change = TWO_P_STEP
        start_row = MAX_RAN + NEGATIVE_STEP

    else:
        one_row_change = NEGATIVE_STEP
        two_row_change = TWO_N_STEP
        start_row = MIN_RAN + POSITIVE_STEP

    oppo_side = opposite_side(side)
    last_round = round - 1
    # Check regular movement.
    if row_change == one_row_change and not col_change and\
                    new_pos == EMPTY:
        return SUCCESS
        
    # Check attack
    elif row_change == one_row_change and \
        (col_change == POSITIVE_STEP or col_change == NEGATIVE_STEP):
        if new_pos != EMPTY:
            return SUCCESS
        
        # En passant attack
        elif last_round in en_passant[ROUND_LIST]:
            e_p_idx = len(en_passant[PAWN_LIST]) - 1
            e_p_position = en_passant[PAWN_LIST][e_p_idx]
            if new_pos == e_p_position:
                return EN_PASSANT
        
    # Check special first movement.
    elif ini_row == start_row and\
            row_change == two_row_change and\
            new_pos == EMPTY and\
            board[new_row + one_row_change][new_col] == EMPTY\
            and not col_change:

            # Check if En Passant applicable, 
            # if so, memorize information about this step.
            right_col = new_col + POSITIVE_STEP
            left_col = new_col + NEGATIVE_STEP
            if board[new_row][right_col] == EMPTY and\
                board[new_row][left_col] == EMPTY:
                return SUCCESS
            
            find_enpassant_pawn(new_row, right_col, new_col, board,\
                                oppo_side, one_row_change, round)
            find_enpassant_pawn(new_row, left_col, new_col, board,\
                                oppo_side, one_row_change, round)
            return SUCCESS
            
    return NOT_SUCCESS

def find_enpassant_pawn(row, col, new_col, board, oppo_side,\
                        one_row_change, round):
    if board[row][col] != EMPTY and\
        board[row][col][NAME_IDX] == PAWN\
        and board[row][col][SIDE_IDX] == oppo_side:
            
            new_row = row + one_row_change

            en_passant[ROUND_LIST].append(round)
            en_passant[PAWN_LIST].append(board[new_row][new_col])
    return

# Print the instruction when need.
def help_func():
    print(HELP_STR_1)
    print(HELP_STR_2)
    print(HELP_STR_3)
    print(HELP_STR_4)
    print(HELP_STR_5)
    return

# Check if input are valid, process raw input.
def valid_input(raw_position):
    ini_row = raw_position[ROW_IDX]
    ini_col = raw_position[COL_IDX]
    new_row = raw_position[NEW_ROW_IDX]
    new_col = raw_position[NEW_COL_IDX]

    if not (ini_row.isdigit() and ini_col.isdigit()\
            and new_row.isdigit() and new_col.isdigit()):
        return NOT_SUCCESS

    ini_row = int(ini_row)
    ini_col = int(ini_col)
    new_row = int(new_row)
    new_col = int(new_col)

    return ini_row, ini_col, EMPTY, new_row, new_col

# Find all potential positions of the pieces from the specific side.
def find_potential_positions(board, side, round, simulate_movement):
    alive_list = find_all_alive(board, side)

    potential_positions = []
    for piece in alive_list:
        for row in range(MIN_RAN , MAX_RAN + POSITIVE_STEP):
            for col in range(MIN_RAN, MAX_RAN + POSITIVE_STEP):

                if movement_successful(piece[ROW_IDX], piece[COL_IDX],\
                    row, col, board, round, simulate_movement, \
                    POTENTIAL_MOVEMENT) == SUCCESS and\
                    [row, col] not in potential_positions:

                    potential_positions.append([row, col])

    return potential_positions

def find_all_alive(board, side):
    alive_list = []
    for row in range(MIN_RAN , MAX_RAN + POSITIVE_STEP):
        for col in range(MIN_RAN , MAX_RAN + POSITIVE_STEP):
            if board[row][col] != EMPTY and\
                board[row][col][SIDE_IDX] == side:
                alive_list.append([row, col])
    return alive_list
            

# Store the two king's position in a dictionary as lists.
def update_king_position(dict, board):
    found = 0
    for row in board:
        for piece in row:
            if piece != EMPTY and piece[NAME_IDX] == KING:
                dict[piece[SIDE_IDX]] = \
                    [board.index(row), row.index(piece)]
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
    potential_positions = find_potential_positions(chess_board, side,\
                                            round, ATTACK_MOVEMENT)
    update_king_position(king_position, chess_board)

    if king_position[oppo_side] in potential_positions:
        check = SUCCESS
        print(CHECK, end = EMPTY)

    potential_positions = find_potential_positions(chess_board,\
                            oppo_side, round + 1, SIMULATE_MOVEMENT)
    if potential_positions == []:
        if check:
            print(CHECK_MATE)
        else:
            print(SALE_MATE)
        return 0
        
    print(EMPTY)
    return 1
    
# Give the opposite side of the current side
def opposite_side(side):
    if side == WHITE:
        return BLACK
    else:
        return WHITE

king_alive = 1
round = 1
memorize_movement(memory, round, chess_board, conditions, en_passant)
print(WELCOME)
print_chess_board(chess_board)
update_king_position(king_position, chess_board)
help_func()

while king_alive:
    raw_position = input(NEXT_MOVE)
    if raw_position == HELP:
        help_func()
        continue
    elif raw_position == CHANGE_ROUND:
        round_num = input(ENTER_ROUND_NUM)
        if not round_num.isdigit():
            print(INVALID_ROUND)
            continue
        round_num = int(round_num)

        new = go_to_memory(memory, round_num)
        if new:
            chess_board = new[BOARD_IDX]
            conditions = new[CONDITION_IDX]
            en_passant = new[EN_PASS_IDX]
            round = new[ROUND_IDX]
            print_chess_board(chess_board)

    elif len(raw_position) != 5:
        print(INVALID_INPUT)
        continue

    else:
        input_positions = valid_input(raw_position)

        if not input_positions:
            print(INVALID_INPUT)
            continue
        else:
            ini_row = input_positions[ROW_IDX]
            ini_col = input_positions[COL_IDX]
            new_row = input_positions[NEW_ROW_IDX]
            new_col = input_positions[NEW_COL_IDX]

        if (not valid_position(ini_row, ini_col)) or \
            (not valid_position(new_row, new_col)):
            continue

        piece = chess_board[ini_row][ini_col]

        out = movement_successful(ini_row, ini_col, new_row, new_col,\
                chess_board, round, SIMULATE_MOVEMENT, PLAYER_MOVEMENT)
        
        if  out != SUCCESS:
            print_failure_rule(out)
            continue
        else:
            process_movement(ini_row, ini_col, new_row, new_col, chess_board)
            print(ROUND + f'{round}')
            print_chess_board(chess_board)

            king_alive = check_or_check_mate(new_row, new_col, round)
            memorize_movement(memory, round, chess_board, conditions,\
                            en_passant)
            round += 1