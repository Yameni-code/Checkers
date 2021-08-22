import pygame
from.constant import WHITE, RED, BLACK, BLUE, GREEN, PLAYER2, PLAYER1, SQUARE_SIZE, Y, X, WIDTH, HEIGHT, KING2, KING1,\
    CROWN, GREY

pygame.font.init()
# base_font_cp = pygame.font.Font('freesansbold.ttf', 50)
base_font_cp = pygame.font.Font('freesansbold.ttf', 25)


def get_all_pieces(board, player):
    """
    :param board:
    :param player:
    :return: positions of every pieces for the giving player on the board
    """

    pieces = []
    if player == PLAYER1:
        king = KING1
    else:
        king = KING2
    for i in range(Y):
        for j in range(Y):
            if board[i][j] == player or board[i][j] == king:
                pieces.append([i, j])
    return pieces


def draw_turn(win, player):
    """
    :param win: Window
    :param player: player
    :return: draw which player plays now beside the board
    """
    radius = SQUARE_SIZE * 0.3
    radius1 = radius + SQUARE_SIZE * 0.05
    if player == PLAYER1:
        pygame.draw.circle(win, BLUE, [WIDTH + SQUARE_SIZE//2, HEIGHT//2], radius1)
        pygame.draw.circle(win, GREEN, [WIDTH + SQUARE_SIZE//2, HEIGHT//2], radius)
    else:
        pygame.draw.circle(win, BLUE, [WIDTH + SQUARE_SIZE//2, HEIGHT // 2], radius1)
        pygame.draw.circle(win, RED, [WIDTH + SQUARE_SIZE//2, HEIGHT // 2], radius)


def creating_piece(table):
    """
    :param table: board
    :return: a matrix with the corresponding pieces to each player
    """
    # attributing each player his pawn
    for x in range(0, Y//2 - 1):
        k = 0
        while k < X:
            if x % 2 != 0:
                table[x][k] = PLAYER1
                k += 2
            else:
                table[x][k+1] = PLAYER1
                k += 2
    for x in range(Y//2 + 1, Y):
        k = 0
        while k < X:
            if x % 2 != 0:
                table[x][k] = PLAYER2
                k += 2
            else:
                table[x][k+1] = PLAYER2
                k += 2
    return table


def draw_board(win):
    """
    :param win: Window
    :return: draw the board on our window
    """
    win.fill(BLACK)
    for i in range(Y):
        for j in range(X):
            if i % 2 == 0 != j % 2:
                pygame.draw.rect(win, WHITE, (i * SQUARE_SIZE, j * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            elif i % 2 != 0 == j % 2:
                pygame.draw.rect(win, WHITE, (i * SQUARE_SIZE, j * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def draw_piece(win, table):
    """
    :param win: Window
    :param table: Board
    :return: draw the pieces on the board
    """
    draw_board(win)
    radius = SQUARE_SIZE * 0.3
    radius1 = radius + SQUARE_SIZE * 0.05
    for i in range(Y):
        for j in range(X):
            if table[i][j] == PLAYER1 or table[i][j] == KING1:
                pygame.draw.circle(win, BLUE, [SQUARE_SIZE * j + SQUARE_SIZE // 2, SQUARE_SIZE * i + SQUARE_SIZE // 2],
                                   radius1)
                pygame.draw.circle(win, GREEN, [SQUARE_SIZE*j + SQUARE_SIZE // 2, SQUARE_SIZE*i + SQUARE_SIZE//2],
                                   radius)
            elif table[i][j] == PLAYER2 or table[i][j] == KING2:
                pygame.draw.circle(win, BLUE, [SQUARE_SIZE * j + SQUARE_SIZE // 2, SQUARE_SIZE * i + SQUARE_SIZE // 2],
                                   radius1)
                pygame.draw.circle(win, RED, [SQUARE_SIZE*j + SQUARE_SIZE // 2, SQUARE_SIZE*i + SQUARE_SIZE//2],
                                   radius)
            if table[i][j] == KING1 or table[i][j] == KING2:
                win.blit(CROWN, (SQUARE_SIZE * j + SQUARE_SIZE // 2 - CROWN.get_width()//2, SQUARE_SIZE*i +
                                 SQUARE_SIZE//2 - CROWN.get_height()//2))
    draw_captured_pieces(win, table)


def draw_possible_moves(win, possible):
    """
    :param win: Window
    :param possible: possible moves of the chosen piece in an array
    :return: draw the moves in grey on the board
    """
    radius = SQUARE_SIZE * 0.2
    for element in possible:
        pygame.draw.circle(win, GREY, [SQUARE_SIZE * element[1] + SQUARE_SIZE // 2, SQUARE_SIZE * element[0]
                                       + SQUARE_SIZE // 2], radius)


def draw_captured_pieces(win, table):
    """
    :param win: Window
    :param table: game matrix
    :return: draw the captured pieces beside the game board
    """
    radius = SQUARE_SIZE * 0.3
    radius1 = radius + SQUARE_SIZE * 0.05
    captured_pieces_p1 = captured_pieces_p2 = 0

    for i in range(Y):
        for j in range(Y):
            if table[i][j] == PLAYER1 or table[i][j] == KING1:
                captured_pieces_p1 += 1
            elif table[i][j] == PLAYER2 or table[i][j] == KING2:
                captured_pieces_p2 += 1

    captured_pieces_p1 = (((Y // 2) - 1) * (X // 2)) - captured_pieces_p1
    captured_pieces_p2 = (((Y // 2) - 1) * (X // 2)) - captured_pieces_p2

    cp2 = base_font_cp.render(str(captured_pieces_p1), True, RED)
    cp1 = base_font_cp.render(str(captured_pieces_p2), True, GREEN)

    win.blit(cp1, (WIDTH + SQUARE_SIZE // 2, SQUARE_SIZE // 2 - 15))
    # win.blit(cp1, (WIDTH + SQUARE_SIZE//2 - 25, SQUARE_SIZE//2 - 50))
    win.blit(cp2, (WIDTH + SQUARE_SIZE//2 - 25, HEIGHT - SQUARE_SIZE//2))

    counter1 = counter2 = 0
    for i in range(captured_pieces_p2 + captured_pieces_p1):
        if counter2 < captured_pieces_p2:
            pygame.draw.circle(win, BLUE, [WIDTH + SQUARE_SIZE // 2, SQUARE_SIZE + (i*10)], radius1)
            pygame.draw.circle(win, RED, [WIDTH + SQUARE_SIZE // 2, SQUARE_SIZE + (i*10)], radius)
            counter2 += 1
        if counter1 < captured_pieces_p1:
            pygame.draw.circle(win, BLUE, [WIDTH + SQUARE_SIZE // 2, HEIGHT - (SQUARE_SIZE + (i*10))], radius1)
            pygame.draw.circle(win, GREEN, [WIDTH + SQUARE_SIZE // 2, HEIGHT - (SQUARE_SIZE + (i*10))], radius)
            counter1 += 1


def mouse_position(pos):
    """
    get the mouse position when clicked on and convert it to the corresponding position integers in our matrix
    :param: position of the mouse on the screen
    :return: matrix index
    """
    x, y = pos
    m = x // SQUARE_SIZE
    n = y // SQUARE_SIZE
    return n, m
