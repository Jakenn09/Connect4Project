import pygame
import numpy as np
import random

#Initialize all variables
ROW_COUNT = 6
COLUMN_COUNT = 7
SECTIONS = 100
RADIUS = int(SECTIONS/2-5)
game_width = COLUMN_COUNT * SECTIONS
game_height = (ROW_COUNT+1) * SECTIONS
screen = pygame.display.set_mode((game_width, game_height))

class Board:

    def create_board():
        board = np.zeros((ROW_COUNT,COLUMN_COUNT))
        return board
    
    def fill_space(board, row, col, disc):
        board[row][col] = disc
    
    def check_empty_space(board, col):
        return board[ROW_COUNT-1][col] == 0
    
    def get_next_open_row(board, col):
        for r in range(ROW_COUNT):
            if board[r][col] == 0:
                return r
    
    def print_board(board):
        print(np.flip(board, 0))
    
    def check_for_win(board, disc):
        # Check for horizontal win
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT):
                if board[r][c] == disc and board[r][c+1] == disc and board[r][c+2] == disc and board[r][c+3] == disc:
                    return True
    
        # Check for vertical win
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT-3):
                if board[r][c] == disc and board[r+1][c] == disc and board[r+2][c] == disc and board[r+3][c] == disc:
                    return True
    
        # Check for positive diagonal wins
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT-3):
                if board[r][c] == disc and board[r+1][c+1] == disc and board[r+2][c+2] == disc and board[r+3][c+3] == disc:
                    return True
    
        # Check for negative diagonal wins
        for c in range(COLUMN_COUNT-3):
            for r in range(3, ROW_COUNT):
                if board[r][c] == disc and board[r-1][c+1] == disc and board[r-2][c+2] == disc and board[r-3][c+3] == disc:
                    return True
        # Draw the main blue and black board of Connect Four
        
    def checkfortie(board):
        return np.all(board)
    
    def draw_board(board):
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                pygame.draw.rect(screen, "Blue", (c*SECTIONS, r*SECTIONS+SECTIONS, SECTIONS, SECTIONS))
                pygame.draw.circle(screen, "Black", (int(c*SECTIONS+SECTIONS/2), int(r*SECTIONS+SECTIONS+SECTIONS/2)), RADIUS)
        # Draw the players disc that they will use
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):      
                if board[r][c] == 1:
                    pygame.draw.circle(screen, "Red", (int(c*SECTIONS+SECTIONS/2), game_height-int(r*SECTIONS+SECTIONS/2)), RADIUS)
                elif board[r][c] == 2: 
                    pygame.draw.circle(screen, "Yellow", (int(c*SECTIONS+SECTIONS/2), game_height-int(r*SECTIONS+SECTIONS/2)), RADIUS)
        pygame.display.update()
    
    @staticmethod
    def goes_first():
        return random.randint(0, 1)


