import pygame

WIDTH, HEIGHT = 600, 600
Y = X = 8
SQUARE_SIZE = HEIGHT // Y

GREY = (128, 128, 128)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 128, 128)

PLAYER1 = 1
PLAYER2 = 2

KING1 = 10
KING2 = 20

FPS = 60

# CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (44, 25))
CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (22, 12))
