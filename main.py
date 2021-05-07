import pygame, numpy as np, sys, random

board_size = 3
BORDER_SIZE = 3
SQUARE_SIZE = 100

width = board_size * SQUARE_SIZE
height = board_size * SQUARE_SIZE
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
board = None
game_over = False
player_turn = 1
ai_piece = None
player_piece = None
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


fontname = pygame.font.match_font("times")


def write_text(surf, text, size, x, y, color):
    font = pygame.font.Font(fontname, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def create_board():
    global board
    board = np.zeros((board_size, board_size))

def valid_location(board, row, col):
    if board[row][col] == 0:
        return True
    return False

def drop_piece(board, row, col, piece):
    board[row][col] = piece
    return board


def check_win(player, board):
    # Check horizontal win
    for r in range(board_size):
        if board[r][0] == player and board[r][1] == player and board[r][2] == player:
            return True

    # Check vertical win
    for c in range(board_size):
        if board[0][c] == player and board[1][c] == player and board[2][c] == player:
            return True

    # Check negatively sloped diagonal win
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True

    # Check positively sloped diagonal win
    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True


def render_board():
    for c in range(board_size):
        for r in range(board_size):
            pygame.draw.rect(screen, WHITE, (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.rect(screen, BLACK, (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, BORDER_SIZE))
            pygame.draw.rect(screen, BLACK, (c * SQUARE_SIZE, r * SQUARE_SIZE, BORDER_SIZE, SQUARE_SIZE))
            pygame.draw.rect(screen, BLACK,
                             (c * SQUARE_SIZE + SQUARE_SIZE - 3, r * SQUARE_SIZE, BORDER_SIZE, SQUARE_SIZE))
            pygame.draw.rect(screen, BLACK,
                             (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE - 3, SQUARE_SIZE, BORDER_SIZE))
            if board[r][c] == 1:
                write_text(screen, "X", 70, c * SQUARE_SIZE + SQUARE_SIZE//2, r * SQUARE_SIZE + SQUARE_SIZE//7, BLACK)
            elif board[r][c] == 2:
                write_text(screen, "O", 70, c * SQUARE_SIZE + SQUARE_SIZE//2, r * SQUARE_SIZE + SQUARE_SIZE//7, BLACK)

    pygame.display.update()


def game_end():
    if draw(board):
        print("draw")
    else:
        print("Game Over")
        print("Player", player_turn, "wins")


def process_event():
    global game_over, player_turn, board, player_piece
    if ai_piece == 1:
        player_piece = 2
    else:
        player_piece = 1
    if player_turn == player_piece and not game_over:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                selected_x, selected_y = pygame.mouse.get_pos()
                selected_x = selected_x // SQUARE_SIZE
                selected_y = selected_y // SQUARE_SIZE
                if valid_location(board, selected_y, selected_x):
                    drop_piece(board, selected_y, selected_x, player_turn)
                    if check_win(player_turn, board):
                        game_over = True
                    elif draw(board):
                        game_over = True
                    else:
                        player_turn = ai_piece

            # print(board)
            render_board()

            if event.type == pygame.QUIT:
                sys.exit()

    if player_turn == ai_piece and not game_over:
        value, spot = minimax(board, 3, True)
        board = drop_piece(board, spot[0], spot[1], player_turn)
        if check_win(player_turn, board):
            print('Player loses')
            game_over = True
        elif draw(board):
            game_over = True
        else:
            player_turn = player_piece

        # print(board)
        render_board()



def get_valid_locations(board):
    valid_locations = []
    for row in range(board_size):
        for col in range(board_size):
            if board[row][col] == 0:
                valid_locations.append([row, col])

    return valid_locations


def draw(board):
    if len(get_valid_locations(board)) == 0:
        return True
    return False


def score_position(board, piece):
    score = 0
    ai_piece = piece
    if piece == 1:
        player_piece = 2
    elif piece == 2:
        player_piece = 1

    #horizontal
    for row in range(board_size):
        window = [int(i) for i in list(board[row, :])]
        if window.count(ai_piece) == 3:
            score += 1000000
        elif window.count(ai_piece) == 2 and window.count(0) == 1:
            score += 1000
        elif window.count(ai_piece) == 1 and window.count(0) == 2:
            score += 30
        elif window.count(player_piece) == 2 and window.count(0) == 1:
            score -= 100000

    # vertical
    for col in range(board_size):
        window = [int(i) for i in list(board[:, col])]
        if window.count(ai_piece) == 3:
            score += 1000000
        elif window.count(ai_piece) == 2 and window.count(0) == 1:
            score += 1000
        elif window.count(ai_piece) == 1 and window.count(0) == 2:
            score += 30
        elif window.count(player_piece) == 2 and window.count(0) == 1:
            score -= 100000


    #negative slope
    window = []
    for i in range(board_size):
        window.append(board[i][i])

    if window.count(ai_piece) == 4:
        score += 100000
    elif window.count(ai_piece) == 3 and window.count(0) == 1:
        score += 1000
    elif window.count(ai_piece) == 2 and window.count(0) == 2:
        score += 30
    elif window.count(player_piece) == 3 and window.count(0) == 1:
        score -= 1000

    window = []
    for i in range(board_size):
        window.append(board[i][(board_size-1) - i])

    if window.count(ai_piece) == 4:
        score += 100000
    elif window.count(ai_piece) == 3 and window.count(0) == 1:
        score += 1000
    elif window.count(ai_piece) == 2 and window.count(0) == 2:
        score += 30
    elif window.count(player_piece) == 3 and window.count(0) == 1:
        score -= 1000

    if board[1][1] == ai_piece:
        score += 10

    return score

def pick_move(board, piece):
    best_score = -1000000000000000000000
    valid_locations = get_valid_locations(board)
    for spot in valid_locations:
        temp_board = board.copy()
        row = spot[0]
        col = spot[1]
        temp_board = drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_spot = spot
            best_score = score

    return best_spot


def is_terminal_node(board):
    return check_win(1, board) or check_win(2, board) or len(get_valid_locations(board)) == 0


def minimax(board, depth, maxplayer):
    valid_locations = get_valid_locations(board)
    terminal_node = is_terminal_node(board)
    if depth == 0 or terminal_node:
        if terminal_node:
            if check_win(ai_piece, board):
                return float("inf"), None
            elif check_win(player_piece, board):
                return float("-inf"), None
            #games tie
            else:
                return 0, None
        else:
            return score_position(board, ai_piece), None
    elif maxplayer:
        value = float("-inf")
        best_spot = random.choice(valid_locations)
        for spot in valid_locations:
            temp_board = board.copy()
            temp_board = drop_piece(temp_board, spot[0], spot[1], ai_piece)
            new_score = minimax(temp_board, depth - 1, False)[0]
            if new_score > value:
                value = new_score
                best_spot = spot
        return value, best_spot
    else:
        value = float("inf")
        best_spot = random.choice(valid_locations)
        for spot in valid_locations:
            temp_board = board.copy()
            temp_board = drop_piece(temp_board, spot[0], spot[1], player_piece)
            new_score = minimax(temp_board, depth - 1, True)[0]
            if new_score < value:
                value = new_score
                best_spot = spot
        return value, best_spot


if __name__ == '__main__':
    pygame.init()
    create_board()

    ai_piece = random.randint(1,2)
    while not game_over:
        process_event()

    game_end()

