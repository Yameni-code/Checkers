from .constant import PLAYER2, PLAYER1, KING1, KING2, Y
from .table import get_all_pieces


def check_move_piece(array, n1, m1, n, m, piece, ob_move):
    # This function checks if the piece move is valid
    # for a piece move to be valid, it should be at an element of the possibles moves and it should of max 2 squares
    if piece == KING2 or piece == KING1:
        if n - n1 > 0 and m - m1 > 0:
            for i in range(Y):
                for ele in array:
                    if ele == (n - i, m - i):
                        if (n1, m1) == ele:
                            return True
                        if array[(n - i, m - i)] != 0:
                            return False
        elif m - m1 < 0 < n - n1:
            for i in range(Y):
                for ele in array:
                    if ele == (n - i, m + i):
                        if (n1, m1) == ele:
                            return True
                        if array[(n - i, m + i)] != 0:
                            return False
        elif n - n1 < 0 and m - m1 < 0:
            for i in range(Y):
                for ele in array:
                    if ele == (n + i, m + i):
                        if (n1, m1) == ele:
                            return True
                        if array[(n + i, m + i)] != 0:
                            return False
        elif m - m1 > 0 > n - n1:
            for i in range(Y):
                for ele in array:
                    if ele == (n + i, m - i):
                        if (n1, m1) == ele:
                            return True
                        if array[(n + i, m - i)] != 0:
                            return False

    if piece == PLAYER1 or piece == PLAYER2:
        if ob_move and abs(n - n1) != 2:
            return False
        for ele in array:
            # n - n1 == 2 capture, == 1 normal piece move
            if (n1, m1) == ele and (abs(n - n1) == 2 or abs(n - n1) == 1):
                return True
    return False


def king_turn(king):
    # This function change the turn of the king
    if king == KING1:
        king = KING2
    else:
        king = KING1
    return king


def player_turn(player):
    # this changes the turn of the player
    if player == PLAYER1:
        player = PLAYER2
    else:
        player = PLAYER1
    return player


def execute_move(pos1, pos2, array, position):
    # this function execute a giving move
    capture = False
    array[pos2[0]][pos2[1]] = array[pos1[0]][pos1[1]]
    array[pos1[0]][pos1[1]] = 0

    if position != 0:
        array[position[0]][position[1]] = 0
        capture = True

    return array, capture


def game_status(param):
    # This function checkers if the game is over or not
    all_moves = []
    for piece in get_all_pieces(param, PLAYER1):
        poss = possible_moves(piece[0], piece[1], param)
        all_moves.append(poss)
    if len(all_moves) == 1 and all_moves[0] == {}:
        return PLAYER2, False
    all_moves.clear()

    for piece in get_all_pieces(param, PLAYER2):
        poss = possible_moves(piece[0], piece[1], param)
        all_moves.append(poss)
    if len(all_moves) == 1 and all_moves[0] == {}:
        return PLAYER1, False
    all_moves.clear()

    counter1 = counter2 = 0
    for i in range(Y):
        for j in range(Y):
            if param[i][j] == PLAYER1 or param[i][j] == KING1:
                counter1 += 1
            if param[i][j] == PLAYER2 or param[i][j] == KING2:
                counter2 += 1
    if counter1 != 0 and counter2 != 0:
        return 0, True
    elif counter1 == 0:
        return PLAYER2, False
    elif counter2 == 0:
        return PLAYER1, False


def crowing_king(board):
    for i in range(Y):
        if board[0][i] == PLAYER2:
            board[0][i] = KING2
        if board[Y-1][i] == PLAYER1:
            board[Y-1][i] = KING1
    return board


def possible_moves(n, m, array, capture=False, old_n=Y, old_m=Y):
    possible = {}
    if array[n][m] == PLAYER1:
        if n + 1 <= Y - 1 and m + 1 <= Y - 1:
            if array[n + 1][m + 1] == 0 and not capture:
                possible[(n+1, m+1)] = 0

        if n + 1 <= Y - 1 and m - 1 >= 0:
            if array[n + 1][m - 1] == 0 and not capture:
                possible[(n+1, m-1)] = 0

        if n + 2 <= Y - 1 and m + 2 <= Y - 1:
            if array[n + 2][m + 2] == 0 and (array[n + 1][m + 1] == PLAYER2 or array[n + 1][m + 1] == KING2):
                possible[(n + 2, m + 2)] = (n + 1, m + 1)

        if n + 2 <= Y - 1 and m - 2 >= 0:
            if array[n + 2][m - 2] == 0 and (array[n + 1][m - 1] == PLAYER2 or array[n + 1][m - 1] == KING2):
                possible[(n + 2, m - 2)] = (n + 1, m - 1)

        if n - 2 >= 0 and m - 2 >= 0:
            if array[n - 2][m - 2] == 0 and (array[n - 1][m - 1] == PLAYER2 or array[n - 1][m - 1] == KING2):
                possible[(n - 2, m - 2)] = (n - 1, m - 1)

        if n - 2 >= 0 and m + 2 <= Y - 1:
            if array[n - 2][m + 2] == 0 and (array[n - 1][m + 1] == PLAYER2 or array[n - 1][m + 1] == KING2):
                possible[(n - 2, m + 2)] = (n - 1, m + 1)

    elif array[n][m] == PLAYER2:
        if n - 1 >= 0 and m - 1 >= 0:
            if array[n - 1][m - 1] == 0 and not capture:
                possible[(n-1, m-1)] = 0

        if n - 1 >= 0 and m + 1 <= Y - 1:
            if array[n - 1][m + 1] == 0 and not capture:
                possible[(n-1, m+1)] = 0

        if n + 2 <= Y - 1 and m + 2 <= Y - 1:
            if array[n + 2][m + 2] == 0 and (array[n + 1][m + 1] == PLAYER1 or array[n + 1][m + 1] == KING1):
                possible[(n + 2, m + 2)] = (n + 1, m + 1)

        if n + 2 <= Y - 1 and m - 2 >= 0:
            if array[n + 2][m - 2] == 0 and (array[n + 1][m - 1] == PLAYER1 or array[n + 1][m - 1] == KING1):
                possible[(n + 2, m - 2)] = (n + 1, m - 1)

        if n - 2 >= 0 and m - 2 >= 0:
            if array[n - 2][m - 2] == 0 and (array[n - 1][m - 1] == PLAYER1 or array[n - 1][m - 1] == KING1):
                possible[(n - 2, m - 2)] = (n - 1, m - 1)

        if n - 2 >= 0 and m + 2 <= Y - 1:
            if array[n - 2][m + 2] == 0 and (array[n - 1][m + 1] == PLAYER1 or array[n - 1][m + 1] == KING1):
                possible[(n - 2, m + 2)] = (n - 1, m + 1)

    elif array[n][m] == KING1:
        con4 = con2 = con3 = con1 = True
        if old_n != Y and old_m != Y:
            if old_n - n < 0 and old_m - m < 0:
                con1 = False
            elif old_m - m < 0 < old_n - n:
                con3 = False
            elif old_n - n > 0 and old_m - m > 0:
                con4 = False
            elif old_m - m > 0 > old_n - n:
                con2 = False

        for i in range(Y):
            if n - i >= 0 and m - i >= 0 and con1:
                if array[n - i][m - i] == 0:
                    if not capture:
                        possible[(n - i, m - i)] = 0

                    if array[n - i + 1][m - i + 1] == PLAYER2 or array[n - i + 1][m - i + 1] == KING2:
                        possible[(n - i, m - i)] = (n - i + 1, m - i + 1)
                        con1 = False

                elif array[n - i][m - i] == PLAYER1 or (n - i == 0 or m - i == 0):
                    con1 = False
                elif array[n - i][m - i] == PLAYER2:
                    if array[n - i - 1][m - i - 1] != 0:
                        con1 = False

            if n - i >= 0 and m + i <= Y - 1 and con2:
                if array[n - i][m + i] == 0:
                    if not capture:
                        possible[(n - i, m + i)] = 0

                    if array[n - i + 1][m + i - 1] == PLAYER2 or array[n - i + 1][m + i - 1] == KING2:
                        possible[(n - i, m + i)] = (n - i + 1, m + i - 1)
                        con2 = False

                elif array[n - i][m + i] == PLAYER1 or (n - i == 0 or m + i == Y - 1):
                    con2 = False
                elif array[n - i][m + i] == PLAYER2:
                    if array[n - i - 1][m + i + 1] != 0:
                        con2 = False

            if n + i <= Y - 1 and m + i <= Y - 1 and con4:
                if array[n + i][m + i] == 0:
                    if not capture:
                        possible[(n + i, m + i)] = 0

                    if array[n + i - 1][m + i - 1] == PLAYER2 or array[n + i - 1][m + i - 1] == KING2:
                        possible[(n + i, m + i)] = (n + i - 1, m + i - 1)
                        con4 = False

                elif array[n + i][m + i] == PLAYER1 or (n + i == Y - 1 or m + i == Y - 1):
                    con4 = False
                elif array[n + i][m + i] == PLAYER2:
                    if array[n + i + 1][m + i + 1] != 0:
                        con4 = False

            if n + i <= Y - 1 and m - i >= 0 and con3:
                if array[n + i][m - i] == 0:
                    if not capture:
                        possible[(n + i, m - i)] = 0

                    if array[n + i - 1][m - i + 1] == PLAYER2 or array[n + i - 1][m - i + 1] == KING2:
                        possible[(n + i, m - i)] = (n + i - 1, m - i + 1)
                        con3 = False

                elif array[n + i][m - i] == PLAYER1 or (n + i == Y - 1 or m - i == 0):
                    con3 = False
                elif array[n + i][m - i] == PLAYER2:
                    if array[n + i + 1][m - i - 1] != 0:
                        con3 = False

    elif array[n][m] == KING2:
        con1 = con2 = con3 = con4 = True
        if old_n != Y and old_m != Y:
            if old_n - n < 0 and old_m - m < 0:
                con1 = False
            elif old_m - m < 0 < old_n - n:
                con3 = False
            elif old_n - n > 0 and old_m - m > 0:
                con4 = False
            elif old_m - m > 0 > old_n - n:
                con2 = False

        for i in range(Y):
            if n - i >= 0 and m - i >= 0 and con1:
                if array[n - i][m - i] == 0:
                    if not capture:
                        possible[(n - i, m - i)] = 0

                    if array[n - i + 1][m - i + 1] == PLAYER1 or array[n - i + 1][m - i + 1] == KING1:
                        possible[(n - i, m - i)] = (n - i + 1, m - i + 1)
                        con1 = False

                elif array[n - i][m - i] == PLAYER2 or (n - i == 0 or m - i == 0):
                    con1 = False
                elif array[n - i][m - i] == PLAYER1:
                    if array[n - i - 1][m - i - 1] != 0:
                        con1 = False

            if n - i >= 0 and m + i <= Y - 1 and con2:
                if array[n - i][m + i] == 0:

                    if not capture:
                        possible[(n - i, m + i)] = 0

                    if array[n - i + 1][m + i - 1] == PLAYER1 or array[n - i + 1][m + i - 1] == KING1:
                        possible[(n - i, m + i)] = (n - i + 1, m + i - 1)
                        con2 = False

                elif array[n - i][m + i] == PLAYER2 or (n - i == 0 or m + i == Y - 1):
                    con2 = False
                elif array[n - i][m + i] == PLAYER1:
                    if array[n - i - 1][m + i + 1] != 0:
                        con2 = False

            if n + i <= Y - 1 and m + i <= Y - 1 and con4:
                if array[n + i][m + i] == 0:
                    if not capture:
                        possible[(n + i, m + i)] = 0

                    if array[n + i - 1][m + i - 1] == PLAYER1 or array[n + i - 1][m + i - 1] == KING1:
                        possible[(n + i, m + i)] = (n + i - 1, m + i - 1)
                        con4 = False

                elif array[n + i][m + i] == PLAYER2 or (n + i == Y - 1 or m + i == Y - 1):
                    con4 = False
                elif array[n + i][m + i] == PLAYER1:
                    if array[n + i + 1][m + i + 1] != 0:
                        con4 = False

            if n + i <= Y - 1 and m - i >= 0 and con3:
                if array[n + i][m - i] == 0:
                    if not capture:
                        possible[(n + i, m - i)] = 0

                    if array[n + i - 1][m - i + 1] == PLAYER1 or array[n + i - 1][m - i + 1] == KING1:
                        possible[(n + i, m - i)] = (n + i - 1, m - i + 1)
                        con3 = False

                elif array[n + i][m - i] == PLAYER2 or (n + i == Y - 1 or m - i == 0):
                    con3 = False
                elif array[n + i][m - i] == PLAYER1:
                    if array[n + i + 1][m - i - 1] != 0:
                        con3 = False

    return possible


def ob_capture(board, player):
    for piece in get_all_pieces(board, player):
        piece_moves = possible_moves(piece[0], piece[1], board)
        for move in piece_moves:
            if piece_moves[move] != 0:
                return True
    return False
