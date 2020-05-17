import pygame
from initializeVariables import *

pygame.font.init()

def drawWindow(screen,grid):    
    screen.fill((0,0,0))
    # Tetris Title
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('TETRIS', 1, (255,255,255))
   
 
    screen.blit(label, (top_left_x + width / 2 - (label.get_width() / 2), 30))
 
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(screen, grid[i][j], (top_left_x + j* 30, top_left_y + i * 30, 30, 30), 0)
 
    # draw grid and border
    drawGrid(screen, 20, 10)
    pygame.draw.rect(screen, (255, 0, 0), (top_left_x, top_left_y, width, height), 5)
    # pygame.display.update()


def drawGrid(screen, row, col):
    sx = top_left_x
    sy = top_left_y
    for i in range(row):
        pygame.draw.line(screen, (128,128,128), (sx, sy+ i*30), (sx + width, sy + i * 30))  # horizontal lines
        for j in range(col):
            pygame.draw.line(screen, (128,128,128), (sx + j * 30, sy), (sx + j * 30, sy + height))  # vertical lines

def createGrid(locked_positions={}):
    grid = [[(0,0,0) for x in range(10)] for x in range(20)]
 
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j,i) in locked_positions:
                c = locked_positions[(j,i)]
                grid[i][j] = c
    return grid
 
