# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 11:09:29 2022

@author: piSky
"""

import numpy as np
import pygame
import sys
import math
from random import choice
import time 

#################
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 8
COLUMN_COUNT = 9 
#################

#####Variables Minimax#####
INF_POS = np.inf
INF_NEG = -np.inf
###########################

###########################
COMP_TURN = 0
USER_TURN = 1

COMP_PIECE = 1
USER_PIECE = 20

turno = 0
DEPTH = 6
###########################

########################################## Minimax alfabeta ##########################################

def is_over (board):
    return winning_move(board, USER_PIECE) or winning_move(board, COMP_PIECE) or len(valid_movements(board)) == 0


def minimax(actual_board, depth, alpha, beta, isMaximizing):
    movements = valid_movements(actual_board)
    if winning_move(actual_board, COMP_PIECE):
        return (None,999999999999)
    elif winning_move(actual_board, USER_PIECE):
        return (None,-999999999999)
    if len(valid_movements(board)) == 0:
        return (None,0)
    if depth==0:
        return (None, (sum_score(actual_board, COMP_PIECE)))

    if isMaximizing:
        maxEval = INF_NEG
        rand_col = choice(movements)
        for c in movements:
            row = get_next_open_row(actual_board, c)
            board_tmp = actual_board.copy()
            drop_piece(board_tmp, row, c, COMP_PIECE)
            c_,currentEval = minimax(board_tmp, depth - 1, alpha, beta, False)
            if currentEval > maxEval:
                maxEval=currentEval
                rand_col = c
            alpha = max(alpha,maxEval)

            if beta <= alpha:
                break
        return (rand_col,maxEval)

    else:
        minEval = INF_POS
        rand_col = choice(movements) 
        for c in movements:
            row = get_next_open_row(actual_board, c)
            board_tmp = actual_board.copy()
            drop_piece(board_tmp, row, c, USER_PIECE)
            c_,currentEval = minimax(board_tmp, depth - 1, alpha, beta, True)
            if currentEval < minEval:
                minEval = currentEval
                rand_col = c
                
            beta = min(beta,minEval)
            if beta <= alpha:
                break
        return (rand_col,minEval)

def valid_movements(board):
    valid = []
    for c in range(COLUMN_COUNT):
        if is_valid_location(board,c):
            valid.append(c)
    return valid
########################################## Minimax alfabeta Ended ##########################################
# def ai_turn(board,player):
#     board_array = [] 
#     for h in range(COLUMN_COUNT):     
#         board_tmp = board.copy()
#         row = get_next_open_row(board, h)
#         drop_piece(board_tmp, row, h, player)
#         board_array.append(board_tmp)
#     return board_array

def score_by_turn(board,player):
    return vertical_check(board,player)+horizontal_check(board,player)+diagonal_check(board,player)

def sum_score(checkbox,player):
    # opponent = COMP_PIECE if player == USER_PIECE else USER_PIECE 
    
    score=0
    if np.count_nonzero(checkbox == 1) == 2 and np.count_nonzero(checkbox == 0) == 2:  
        score+=5
    elif np.count_nonzero(checkbox == 1) == 3 and np.count_nonzero(checkbox == 0) == 1:
        score+=10
    elif np.count_nonzero(checkbox == 20) == 3 and np.count_nonzero(checkbox == 0) == 1:
        score-=20
    elif np.count_nonzero(checkbox == 1) == 4:    
        score+=100    
    return score


def vertical_check(board,player):
    # possibility_vector=np.zeros(COLUMN_COUNT,dtype=int)
    board_tmp = board.copy().T
    score=0
    try:
        checkbox=[]
        for r in range(len(board_tmp)):
                checkbox=[]
                # if not np.all(board_tmp[r]==0) and not np.all(board_tmp[r] != 0):
                for c in range(len(board_tmp[r])-3):
                    checkbox = board_tmp[r][c:c+4].copy()
                    score += sum_score(checkbox,player)
                    # if np.count_nonzero(checkbox == player) == 2 and np.count_nonzero(checkbox == 0) == 2:  
                    #     score+=2
                    #     # possibility_vector[r] = 20 if possibility_vector[r] < 20 else possibility_vector[r]
                    # elif np.count_nonzero(checkbox == player) == 3 and np.count_nonzero(checkbox == 0) == 1:
                    #     score+=5
                    #     # possibility_vector[r] = 50 if possibility_vector[r] < 100 else possibility_vector[r]  
                    # elif np.count_nonzero(checkbox == 20) == 3 and np.count_nonzero(checkbox == 0) == 1:
                    #     score-=4
                    #     # possibility_vector[r] = -100 if possibility_vector[r] > -50 else possibility_vector[r]  
                    # elif np.count_nonzero(checkbox == player) == 4:    
                    #     score+=100
                    #     # possibility_vector[r] = 9999 if possibility_vector[r] < 9999 else possibility_vector[r]
                
    except Exception as e:
        print(e)
        pass
    return score

def horizontal_check(board,player):
    # possibility_vector=np.zeros(COLUMN_COUNT,dtype=int)
    # possibility_vector_sum=np.zeros(COLUMN_COUNT,dtype=int)
    board_tmp= board.copy()    
    score=0
    try:
        for r in range((ROW_COUNT)):
            checkbox=[]
            # if not np.all(board_tmp[r]==0) and not np.all(board_tmp[r] != 0):
            for c in range(COLUMN_COUNT-3):
                checkbox = board_tmp[r][c:c+4].copy()
                score += sum_score(checkbox, player)
                    
                    #SE REVISA EL TABLERO Y ADEMAS SI EXISTE UNA FICHA COMO SOPORTE PARA FORMAR LA HORIZONTAL
                    # if r>0:
                    #     checkbox_check = board_tmp[r-1][c:c+4].copy()
                    # else:
                    #     checkbox_check = [1,1,1,1]
                    # if np.count_nonzero(checkbox == player) == 2 and np.count_nonzero(checkbox == 0) == 2:# and np.all(checkbox_check != 0):    
                    #     score+=2
                    #     # for i in range(len(checkbox)):
                    #     #     checkbox[i] = 20 if checkbox[i] == 0 else 0 
                    #     # possibility_vector[c:c+4] = checkbox    
                    #     # possibility_vector_sum = np.sum([possibility_vector_sum,possibility_vector],axis=0)

                    # elif np.count_nonzero(checkbox == player) == 3 and np.count_nonzero(checkbox == 0) == 1:# and np.all(checkbox_check != 0):    
                    #     score+=5
                    #     # for i in range(len(checkbox)):
                    #     #     checkbox[i] = 50 if checkbox[i] == 0 else 0 
                    #     # possibility_vector[c:c+4] = checkbox    
                    #     # possibility_vector_sum = np.sum([possibility_vector_sum,possibility_vector],axis=0)
                    # elif np.count_nonzero(checkbox == 20) == 3 and np.count_nonzero(checkbox == 0) == 1:# and np.all(checkbox_check != 0):    
                    #     score-=4

                    #     # for i in range(len(checkbox)):
                    #     #     checkbox[i] = -100 if checkbox[i] == 0 else 0 
                    #     # possibility_vector[c:c+4] = checkbox    
                    #     # possibility_vector_sum = np.sum([possibility_vector_sum,possibility_vector],axis=0)

                    # elif np.count_nonzero(checkbox == player) == 4:# and np.all(checkbox_check != 0):    
                    #     # for i in range(len(checkbox)):
                    #     #     checkbox[i] = 100 if checkbox[i] == 0 else 0 
                    #     score+=100
    
                    #     # possibility_vector[c:c+4] = checkbox    
                    #     # possibility_vector_sum = np.sum([possibility_vector_sum,possibility_vector],axis=0)
                    #     # return possibility_vector_sum 
                    # # elif np.count_nonzero(checkbox == 20) == 4 and np.all(checkbox_check != 0):    
                    # #     for i in range(len(checkbox)):
                    # #         checkbox[i] = -9999 if checkbox[i] == 0 else 0 
                    # #     possibility_vector[c:c+4] = checkbox    
                    # #     possibility_vector_sum = np.sum([possibility_vector_sum,possibility_vector],axis=0)
                    # #     return possibility_vector_sum 
                     
    except Exception as e:
        print(e)
        pass
    return score

def diagonal_check(board,player):
    # possibility_vector=np.zeros(COLUMN_COUNT,dtype=int)
    # possibility_vector_sum=np.zeros(COLUMN_COUNT,dtype=int)
    board_tmp= board.copy()
    score=0
    for r in range(ROW_COUNT-3):
        checkbox = np.zeros(4)
        checkbox_inv = np.zeros(4)
        for c in range(COLUMN_COUNT-3):
            # if not np.all(board_tmp[r]==0):
            checkbox = np.array([board_tmp[r+n][c+n].copy() for n in range(4)])
            checkbox_inv =  np.array([board_tmp[r+n][c+3-n].copy() for n in range(4)])
                
            score += sum_score(checkbox,player)
            score += sum_score(checkbox_inv,player)
                #codigo para revisar mas meticulosamente las jugadas sabiendo si es posible o no generar una diagonal
                # # if r>0:
                # #     checkbox_check = np.array([board_tmp[r+n-1][c+n].copy() for n in range(4)])
                # #     checkbox_check_inv = np.array([board_tmp[r+n-1][c+3-n].copy() for n in range(4)]) 
                # # else:
                    
                # #     checkbox_check = np.array([board_tmp[r+n][c+n+1].copy() for n in range(3)])
                # #     checkbox_check_inv = np.array([board_tmp[r+n][c+3-n-1].copy() for n in range(3)])
                    
                
                # if np.count_nonzero(checkbox == player) == 2 and np.count_nonzero(checkbox == 0) == 2:# and np.all(checkbox_check != 0):
                #     # for i in range(len(checkbox)):
                #     #     checkbox[i] = 20 if checkbox[i] == 0 else 0
                #     score+=2
                #     # possibility_vector[c:c+4] = checkbox    
                #     # possibility_vector_sum = np.sum([possibility_vector_sum,possibility_vector],axis=0)
                # elif np.count_nonzero(checkbox == player) == 3 and np.count_nonzero(checkbox == 0) == 1: #and np.all(checkbox_check != 0):
                #     score+=5
                #     # for i in range(len(checkbox)):
                #     #        checkbox[i] = 50 if checkbox[i] == 0 else 0 
                #       # possibility_vector[c:c+4] = checkbox    
                #       # possibility_vector_sum = np.sum([possibility_vector_sum,possibility_vector],axis=0)
                # elif np.count_nonzero(checkbox == player) == 4:# and np.all(checkbox_check != 0):
                #       # for i in range(len(checkbox)):
                #       #      checkbox[i] = 9999 if checkbox[i] == 0 else 0 
                #       score+=100
                # #       possibility_vector[c:c+4] = checkbox    
                # #       possibility_vector_sum = np.sum([possibility_vector_sum,possibility_vector],axis=0)
                # # # elif np.count_nonzero(checkbox == 20) == 4 and np.all(checkbox_check != 0):
                # #       for i in range(len(checkbox)):
                # #           checkbox[i] = -9999 if checkbox[i] == 0 else 0 
                # #       possibility_vector[c:c+4] = checkbox    
                # #       possibility_vector_sum = np.sum([possibility_vector_sum,possibility_vector],axis=0)
                
                # elif np.count_nonzero(checkbox == 20) == 3 and np.count_nonzero(checkbox == 0) == 1:# and np.all(checkbox_check != 0):
                #       score-=4
  
                #       # for i in range(len(checkbox)):
                #       #     checkbox[i] = -100 if checkbox[i] == 0 else 0 
                #       # possibility_vector[c:c+4] = checkbox    
                #       # possibility_vector_sum = np.sum([possibility_vector_sum,possibility_vector],axis=0)
                
                # if np.count_nonzero(checkbox_inv == player) == 2 and np.count_nonzero(checkbox_inv == 0) == 2:# and np.all(checkbox_check_inv != 0):
                #     # for i in range(len(checkbox)):
                #     #     checkbox_inv[i] = 20 if checkbox_inv[i] == 0 else 0
                #     score+=2
                #     # possibility_vector[c:c+4] = np.flip(checkbox_inv)   
                #     # possibility_vector_sum = np.sum([possibility_vector_sum,possibility_vector],axis=0)
                # elif np.count_nonzero(checkbox_inv == player) == 3 and np.count_nonzero(checkbox_inv == 0) == 1:# and np.all(checkbox_check_inv != 0):
                #      # for i in range(len(checkbox_inv)):
                #      #      checkbox_inv[i] = 50 if checkbox_inv[i] == 0 else 0
                #      score+=5
                #      # possibility_vector[c:c+4] = np.flip(checkbox_inv) 
                #      # possibility_vector_sum = np.sum([possibility_vector_sum,possibility_vector],axis=0)
                # elif np.count_nonzero(checkbox_inv == player) == 4:# and np.all(checkbox_check_inv != 0):
                #       # for i in range(len(checkbox_inv)):
                #       #      checkbox_inv[i] = 9999 if checkbox_inv[i] == 0 else 0 
                #       score+=100
                #       # possibility_vector[c:c+4] = np.flip(checkbox_inv)     
                #       # possibility_vector_sum = np.sum([possibility_vector_sum,possibility_vector],axis=0)
                # elif np.count_nonzero(checkbox_inv == 20) == 3 and np.count_nonzero(checkbox_inv == 0) == 1:# and np.all(checkbox_check_inv != 0):
                #       # for i in range(len(checkbox_inv)):
                #       #     checkbox_inv[i] = -100 if checkbox_inv[i] == 0 else 0 
                #       score-=4
                #       # possibility_vector[c:c+4] = np.flip(checkbox_inv) 
                #       # possibility_vector_sum = np.sum([possibility_vector_sum,possibility_vector],axis=0)
                # # elif np.count_nonzero(checkbox_inv == 20) == 4 and np.all(checkbox_check_inv != 0):
                # #      for i in range(len(checkbox_inv)):
                # #          checkbox_inv[i] = -9999 if checkbox_inv[i] == 0 else 0 
                # #      possibility_vector[c:c+4] = np.flip(checkbox_inv)     
                # #      possibility_vector_sum = np.sum([possibility_vector_sum,possibility_vector],axis=0)
    return score

########################################## Game ##########################################


def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board
 
def drop_piece(board, row, col, piece):
    board[row][col] = piece
 
def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0
 
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r
 
def print_board(board):
    print(np.flip(board, 0))
 
def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
 
    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
 
    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
 
    # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
 
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
     
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):      
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 20: 
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()
 
 
board = create_board()
# print_board(board)
game_over = False
turn = 0
 
#initalize pygame
pygame.init()
 
#define our screen size
SQUARESIZE = 100
 
#define width and height of board
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)
 
screen = pygame.display.set_mode(size)
#Calling function draw_board again
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

#funcion para probar si esta funcionando la heuristica
def test_movement(board, player):
    valid_locations = valid_movements(board)
    col = choice(valid_locations)
    maxscore = -np.inf
    for c in valid_locations:
        row = get_next_open_row(board, c)
        temp_board = board.copy()
        drop_piece(temp_board, row, c, player)
        score = score_by_turn(temp_board, player)
        if score > maxscore:
            maxscore = score
            col = c

    return col

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                game_over = False
                board = create_board()
                draw_board(board)
                pygame.display.update()
                win_list = []

        else:
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
                else: 
                    pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
            pygame.display.update()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                #print(event.pos)

               
                # # Ask for Player 2 Input
                if turn == USER_TURN:                
                    posx = event.pos[0]
                    col = int(math.floor(posx/SQUARESIZE))
                    
                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        # print(score_by_turn(board,1),'rojo')
                        drop_piece(board, row, col, 20) 

                        if winning_move(board, 20):
                            label = myfont.render("Player 2 wins!!", 1, YELLOW)
                            screen.blit(label, (40,10))
                            game_over = True
                            draw_board(board)
                            continue
                        print_board(board)
                        draw_board(board)
                        turn += 1
                        turn = turn % 2
    
    # Ask for Player 1 Input
    if turn == COMP_TURN:
        start = time.time()
        col,s  = minimax(board, DEPTH, INF_NEG, INF_POS, True)
        # col = test_movement(board, 1)
        # print(s)
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            # print(score_by_turn(board,20),'amarillo')
            drop_piece(board, row, col, 1)
            
    
            if winning_move(board, 1):
                label = myfont.render("Player 1 wins!!", 1, RED)
                screen.blit(label, (40,10))
                game_over = True
        end = time.time()
        print('tiempo de procesamiento para la jugada N',turno,' con',DEPTH,'de profundidad del agente adversario',(end-start)*100000//100,'[ms]')
        turno+=1
        print_board(board)
        draw_board(board)
        turn += 1
        turn = turn % 2
     ########################################## Game Ended ##########################################


