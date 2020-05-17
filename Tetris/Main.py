'''
author : shubham
title : tetris game
library : pygame
language : python
'''

import pygame
from initializeVariables import *
from getWindow import *

icon = pygame.image.load("tetrisIcon.png")
pygame.display.set_icon(icon)

pygame.font.init()
 

import random
 
class Piece(object):
    rows = 20  # y
    columns = 10  # x
 
    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0  # number from 0-3
 

 
def convertShapeFormat(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]
 
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))
 
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)
 
    return positions
 
 
def validSpace(shape, grid):
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convertShapeFormat(shape)
 
    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
 
    return True
 
 
def checkLost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False
 
 
def getShape():
    global shapes, shape_colors
 
    return Piece(5, 0, random.choice(shapes))
 
 
def drawTextMiddle(text, size, color, screen):
    font = pygame.font.SysFont('retro', size, bold=True)
    label = font.render(text,1,color)
    screen.blit(label, (top_left_x + width//2 - (label.get_width() // 2), top_left_y + height//2 - label.get_height()//2))

 
 
def clearRows(grid, locked):
    # need to see if row is clear the shift every other row above down one
 
    inc = 0
    for i in range(len(grid)-1,-1,-1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            # add positions to remove from locked
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
 
 
def drawNextShape(shape, screen):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (255,255,255))
 
    sx = top_left_x + width + 50
    sy = top_left_y + height/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]
 
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(screen, shape.color, (sx + j*30, sy + i*30, 30, 30), 0)
 
    screen.blit(label, (sx + 10, sy- 30))
 
 
def main(score):
    global grid

 
    locked_positions = {}  # (x,y):(255,0,0)
    grid = createGrid(locked_positions)
 
    change_piece = False
    run = True
    current_piece = getShape()
    next_piece = getShape()
    clock = pygame.time.Clock()
    fall_time = 0
    
    while run:
        fall_speed = 0.27
    
        grid = createGrid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()
 
        # PIECE FALLING CODE
        if fall_time/1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (validSpace(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not validSpace(current_piece, grid):
                        current_piece.x += 1
 
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not validSpace(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_UP:
                    # rotate shape
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if not validSpace(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)
 
                if event.key == pygame.K_DOWN:
                    # move shape down
                    current_piece.y += 1
                    if not validSpace(current_piece, grid):
                        current_piece.y -= 1
 

                if event.key == pygame.K_SPACE:
                   while validSpace(current_piece, grid):
                       current_piece.y += 1
                   current_piece.y -= 1
                   print(convertShapeFormat(current_piece))
 
        shape_pos = convertShapeFormat(current_piece)
 
        # add piece to the grid for drawing
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color
 
        # IF PIECE HIT GROUND
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = getShape()
            change_piece = False
 
            # call four times to check for multiple clear rows
            clearRows(grid, locked_positions)
        
        drawWindow(win,grid)
        drawNextShape(next_piece, win)
    
        pygame.display.update()
        score = score + 0.01
        font = pygame.font.SysFont('comicsans', 30)
        label2= font.render('Score : '+str(int(score)),1,(255,255,255))
        win.blit(label2,(10,10))
        pygame.display.update()
 
        # Check if user lost
        if checkLost(locked_positions):
            run = False
 
    drawTextMiddle("You Lost", 40, (255,255,255), win)
    pygame.display.update()
    pygame.time.delay(2000)
 
 
def mainMenu():
    run = True
    while run:
        pygame.mixer.init()
        pygame.mixer.music.load('success.wav')
        pygame.mixer.music.play(-1)
        win.fill((255,150,0))
        drawTextMiddle('>>>> Press any key <<<<', 80, (0, 0, 0), win)
        font = pygame.font.SysFont('monospace',30)
        label = font.render('Author : Shubham ',1,(255,255,255))
        win.blit(label, (top_left_x + width//2 - (label.get_width() // 2), top_left_y + height//2 + 100  - label.get_height()//2))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
 
            if event.type == pygame.KEYDOWN:
                main(score)
    pygame.quit()
 
 
win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Let\'s Play Tetris')
 
if __name__ == '__main__':
    mainMenu()
