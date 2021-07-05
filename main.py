"""
Checkers Game
By Yameni Bakam Gleen Karel
last edit: 23.03.2021
"""

import pygame
import numpy
from copy import deepcopy
from vision.machine_vision import test
from Dame.constant import WIDTH, HEIGHT, PLAYER2, PLAYER1, FPS, Y, X, KING2, SQUARE_SIZE, GREEN, RED
from Dame.table import mouse_position, creating_piece, draw_piece, draw_turn, draw_possible_moves
from Dame.logic import game_status, execute_move, crowing_king, possible_moves, player_turn,\
    check_move_piece, king_turn, ob_capture
from Dame.ai_logic import minimax

# initialize the font to display integers
pygame.font.init()

WIN = pygame.display.set_mode((WIDTH + SQUARE_SIZE, HEIGHT))
pygame.display.set_caption('Dame')
base_font = pygame.font.Font('freesansbold.ttf', 100)


def main():
    status_game = first_move = True
    quit_game = capture = False
    player, king, winner = PLAYER2, KING2, 0
    n = m = 0
    moves = {}
    ob_move_p = False
    clock = pygame.time.Clock()

    table = numpy.zeros([Y, X], dtype=int)
    table = creating_piece(table)
   
    while status_game:
        clock.tick(FPS)

        winner, status_game = game_status(table)

        if player == PLAYER1 and status_game:
            # pygame.time.delay(8000)
            evaluation, best, move_to, algo_table = minimax(table, 8, player)
            print(evaluation, best, move_to)
            print(numpy.matrix(algo_table))
            moves.clear()
            table = deepcopy(algo_table)
            table = crowing_king(table)
            player = player_turn(player)
            king = king_turn(king)
        """""
        if player == PLAYER2 and status_game:
            # pygame.time.delay(8000)
            evaluation, best, move_to, algo_table = minimax(table, 5, player)
            print(evaluation, best, move_to)
            print(numpy.matrix(algo_table))
            moves.clear()
            table = deepcopy(algo_table)
            table = crowing_king(table)
            player = player_turn(player)
            king = king_turn(king)
        """""  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                status_game = False
                quit_game = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if first_move:
                    pos = pygame.mouse.get_pos()
                    n, m = mouse_position(pos)
                    moves.clear()
                    moves = possible_moves(n, m, table, capture)
                    ob_move_p = ob_capture(table, player)
                    if table[n][m] == player or table[n][m] == king:
                        first_move = False
                else:
                    first_move = True
                    pos1 = pygame.mouse.get_pos()
                    n1, m1 = mouse_position(pos1)
                    if check_move_piece(moves, n1, m1, n, m, table[n][m], ob_move_p):
                        table, capture = execute_move([n, m], [n1, m1], table, moves[(n1, m1)])
                        table = crowing_king(table)
                        moves.clear()
                        if capture:
                            moves = possible_moves(n1, m1, table, capture, n, m)
                            print(moves)
                        if moves:
                            n, m = n1, m1
                            first_move = False
                        if not moves:
                            player = player_turn(player)
                            king = king_turn(king)
                            moves.clear()
                            capture = False

        draw_piece(WIN, table)
        draw_possible_moves(WIN, moves)
        draw_turn(WIN, player)
        pygame.display.update()

    text_surface = base_font.render("", True, GREEN)
    if winner == PLAYER1:
        text_surface = base_font.render("GREEN WON", True, GREEN)
    elif winner == PLAYER2:
        text_surface = base_font.render("RED WON", True, RED)

    while not status_game and not quit_game:
        draw_piece(WIN, table)
        WIN.blit(text_surface, (WIDTH // 4 - SQUARE_SIZE, HEIGHT // 2 - 50))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                status_game = True


main()

# test()
