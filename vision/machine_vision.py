import copy
import time
import pygame
import cv2
import cv2.aruco as aruco
import numpy as np
from Dame.constant import X, Y, PLAYER1
from Dame.ai_logic import minimax
from Dame.table import draw_piece, creating_piece
from Dame.logic import execute_move


def get_piece_on_board():
    board = np.zeros([Y, X], dtype=int)
    for i in range(Y):
        for j in range(X):
            if i % 2 == 0 != j % 2:
                pass
            elif i % 2 != 0 == j % 2:
                pass
    return board


def board_vid(frame, coord):
    width = 600
    height = 600

    pts1 = np.float32([coord[2], coord[3], coord[1], coord[0]])
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])

    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    new_vid = cv2.warpPerspective(frame, matrix, (width, height))

    matrix = cv2.getRotationMatrix2D((width//2, height/2), 90, 1)
    new_vid = cv2.warpAffine(new_vid, matrix, (width, height))
    return new_vid


def detect_pieces(circles, board):
    # circles = [[[x, y, r],...]]
    # x is the pixel value in the x-axis
    # r is the radius of the circle
    for circle in circles[0]:
        m = int(circle[0]/75)
        if m == 8:
            m = 7
        n = int(circle[1]/75)
        if n == 8:
            n = 7
        board[n][m] = 2
    return board


def calc_bound(boxes):
    coord = []
    # Change the aruco markers and put new ones with correct orientation
    for box in boxes:
        if box[0][0][0] > 300 and box[0][0][1] > 300:
            x = box[0][2][0]
            y = box[0][2][1]
        elif box[0][0][0] < 300 < box[0][0][1]:
            x = box[0][1][0]
            y = box[0][1][1]
        elif box[0][0][0] < 300 and box[0][0][1] < 300:
            x = box[0][2][0]
            y = box[0][2][1]
        else:
            x = box[0][2][0]
            y = box[0][2][1]
        coord.append([x, y])

    return coord


def capture_piece(old_board, board):
    old_pos = new_pos = []
    for i in range(8):
        for j in range(8):
            if board[i][j] == 2 and old_board[i][j] == 0:
                new_pos = [i, j]
            if board[i][j] == 0 and old_board[i][j] == 2:
                old_pos = [i, j]

    if not new_pos:
        return old_pos, new_pos, 0

    if abs(new_pos[0] - old_pos[0]) == 1:
        return old_pos, new_pos, 0
    else:
        if new_pos[0] > old_pos[0] and new_pos[1] > old_pos[1]:
            capture_pos = [old_pos[0]+1, old_pos[1]+1]
        elif new_pos[0] < old_pos[0] and new_pos[1] < old_pos[1]:
            capture_pos = [old_pos[0] - 1, old_pos[1] - 1]
        elif new_pos[0] < old_pos[0] and new_pos[1] > old_pos[1]:
            capture_pos = [old_pos[0] - 1, old_pos[1] + 1]
        else:
            capture_pos = [old_pos[0] + 1, old_pos[1] - 1]
    return old_pos, new_pos, capture_pos


def aruco_marker(win):
    # think about separating this function into 2
    counter = 0
    # skip = 1
    old_board = board = algo_board = np.zeros([8, 8], dtype=int)
    # board = np.zeros([8, 8], dtype=int)
    algo_board = creating_piece(algo_board)
    cap = cv2.VideoCapture(1 )
    coord = []
    new_coord = [[], [], [], []]
    status = True
    numberOfPieces = 12
    while True:
        success, img = cap.read()
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        arucoDict = aruco.Dictionary_get(aruco.DICT_4X4_50)
        arucoParam = aruco.DetectorParameters_create()
        boxes, ids, rejected = aruco.detectMarkers(imgGray, arucoDict, parameters=arucoParam)

        if boxes and status:
            print(boxes)
            print(len(boxes))
            aruco.drawDetectedMarkers(img, boxes)
            cv2.imshow("Video", img)
            if len(boxes) > 3:
                coord = calc_bound(boxes)
                print(coord)
                status = False

                for coo in coord:
                    if coo[0] > 300 and coo[1] > 300:
                        new_coord[0] = coo
                    elif coo[0] < 300 < coo[1]:
                        new_coord[1] = coo
                    elif coo[0] < 300 and coo[1] < 300:
                        new_coord[2] = coo
                    else:
                        new_coord[3] = coo

        if coord:
            new_img = board_vid(img, new_coord)

            grey_vid = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)

            blur_vid = cv2.GaussianBlur(grey_vid, (21, 21), 1)

            circles = cv2.HoughCircles(blur_vid, cv2.HOUGH_GRADIENT, 1, 20,
                                       param1=50, param2=40, minRadius=16, maxRadius=100)

            if circles is not None:
                # print(circles)
                circles = np.uint16(np.around(circles))
                counter = counter + 1
                # print(counter)
                new_board = copy.deepcopy(board)
                board = detect_pieces(circles, new_board)

                # Draw the circles
                for i in circles[0, :]:
                    # draw the outer circle
                    cv2.circle(new_img, (i[0], i[1]), i[2], (0, 255, 0), 2)
                    # draw the center of the circle
                    cv2.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)

            if counter == 50:
                if np.sum(board) == numberOfPieces*2 and not (old_board == board).all():
                    old_pos, new_pos, capture_pos = capture_piece(old_board, board)
                    print(capture_pos)
                    if new_pos:
                        algo_board, xx = execute_move(old_pos, new_pos, algo_board, capture_pos)
                    for i in range(8):
                        for j in range(8):
                            if algo_board[i][j] == 2:
                                algo_board[i][j] = 0
                            if board[i][j] == 2:
                                algo_board[i][j] = 2

                    draw_piece(win, algo_board)
                    pygame.display.update()

                    print(board)

                    a1, a2, a3, algo_board = minimax(algo_board, 8, PLAYER1)

                    draw_piece(win, algo_board)
                    pygame.display.update()
                    old_board = np.zeros([8, 8], dtype=int)
                    piece = 0
                    for i in range(8):
                        for j in range(8):
                            if algo_board[i][j] == 2:
                                old_board[i][j] = 2
                                piece += 1

                    if numberOfPieces != piece:
                        time.sleep(5)
                        numberOfPieces = piece
                counter = 0
                board = np.zeros([8, 8], dtype=int)

            cv2.imshow("New Video", new_img)
        # skip += 1

        if cv2.waitKey(5) == 27:
            break
