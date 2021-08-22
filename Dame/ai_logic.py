# import numpy
import math
from copy import deepcopy
from .table import get_all_pieces
from .logic import game_status, possible_moves, execute_move, ob_capture
from .constant import Y, X, PLAYER1, PLAYER2, KING2, KING1

a_moves = []


def recur(r_board, n_play, p0, p1, piece):
    for move in n_play:
        rtemp_board = deepcopy(r_board)
        rnew_board, cap = execute_move([p0, p1], move, rtemp_board, n_play[move])
        if cap:
            n1_play = possible_moves(move[0], move[1], rnew_board, cap, p0, p1)
            if n1_play:
                recur(rnew_board, n1_play, move[0], move[1], piece)
            else:
                a_moves.append([rnew_board, piece, move])
        else:
            a_moves.append([rnew_board, piece, move])
    return a_moves


def get_key(valid_moves):
    for move in valid_moves:
        if valid_moves[move] == 0:
            return move
    return 0


def all_possible_move(player, board, ob_move):
    """
    :param player: player
    :param board: board
    :param ob_move: obligatory move
    :return: return
    """
    all_moves = []
    for piece in get_all_pieces(board, player):
        valid_moves = possible_moves(piece[0], piece[1], board)
        if ob_move:
            for i in range(len(valid_moves)):
                if get_key(valid_moves) != 0:
                    valid_moves.pop(get_key(valid_moves))
                if not valid_moves:
                    break

        for move in valid_moves:
            temp_board = deepcopy(board)
            new_board, cap = execute_move(piece, move, temp_board, valid_moves[move])
            if cap:
                next_play = possible_moves(move[0], move[1], new_board, cap, piece[0], piece[1])
                if next_play:
                    a_moves.clear()
                    sub_all_moves = recur(new_board, next_play, move[0], move[1], piece)
                    for ele in sub_all_moves:
                        all_moves.append(ele)
                else:
                    all_moves.append([new_board, piece, move])
            else:
                all_moves.append([new_board, piece, move])
        valid_moves.clear()

    return all_moves


def weight_calc(table):
    # Evaluates the board

    pieces1 = pieces2 = king1 = king2 = 0
    for i in range(Y):
        for j in range(Y):
            if table[i][j] == PLAYER1:
                pieces1 += 1
            elif table[i][j] == PLAYER2 or table[i][j] == KING2:
                pieces2 += 1
            elif table[i][j] == KING1:
                king1 += 2
            elif table[i][j] == KING2:
                king2 += 2
    return pieces1 - pieces2 + (king1 - king2)


def minimax(board, depth, player, alpha=-math.inf, beta=math.inf):
    """
    :param board: board
    :param depth: searching depth
    :param player: player
    :param alpha: helping variable
    :param beta: helping variable
    :return: evaluation, index for the best move, index of the next move, board
    """
    game = []
    _, game_over = game_status(board)

    if depth == 0 or (not game_over):
        return weight_calc(board), [], {}

    if player == PLAYER1:
        max_weight = - ((Y//2 - 1) * X//2) - 1
        best_move = None
        move_to = None
        for element in all_possible_move(player, board, ob_capture(board, PLAYER1)):
            child_weight = minimax(element[0], depth - 1, PLAYER2, alpha, beta)[0]
            max_weight = max(max_weight, child_weight)
            if beta <= alpha:
                break
            if max_weight == child_weight:
                game = element[0]
                best_move = element[1]
                move_to = element[2]
            alpha = max(alpha, max_weight)

        return max_weight, best_move, move_to, game

    else:
        min_weight = ((Y // 2 - 1) * X // 2) + 1
        best_move = None
        move_to = None
        for element in all_possible_move(player, board, ob_capture(board, PLAYER2)):
            child_weight = minimax(element[0], depth - 1, PLAYER1, alpha, beta)[0]
            min_weight = min(min_weight, child_weight)
            if beta <= alpha:
                break
            if min_weight == child_weight:
                best_move = element[1]
                move_to = element[2]
                game = element[0]
            beta = min(beta, min_weight)

        return min_weight, best_move, move_to, game
