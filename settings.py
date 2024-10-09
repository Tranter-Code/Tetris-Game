import pygame as pg

#Colour settings
RED = "#e51b20"
BLUE = "#275bbf"
GREEN = "#3fcc01"
YELLOW = "#ffc410"
PURPLE = "#7b217f"
CYAN = "#6cc6d9"
ORANGE = "#f07e13"
WHITE = "#ffffff"
BLACK = "#000000"
DARK_GREY = "#1E1E1E"
LITE_GREY = "#333333"

#Game settings
FPS = 60 #Frames per second for timing
TIMER_INTERVAL = 300
MOVE_DELAY = 150
ROTATE_DELAY = 150

#Grid
COL_NUMBER = 10
ROW_NUMBER = 20
CELL_SIZE = 35 #Sets the size of each cell in the grid
GRID_WIDTH = COL_NUMBER * CELL_SIZE
GRID_HEIGHT = ROW_NUMBER * CELL_SIZE
GRID_RESOLUTION = GRID_WIDTH, GRID_HEIGHT

#Window 
WINDOW_PADDING = 20
WINDOW_WIDTH = GRID_WIDTH + WINDOW_PADDING * 2
WINDOW_HEIGHT = GRID_HEIGHT + WINDOW_PADDING * 2
WINDOW_RESOLUTION = WINDOW_WIDTH, WINDOW_HEIGHT

#Shapes
TETROMINOS = {
    'O' : {'shape' : [(0, 0), (0, -1), (1, 0), (1, -1)], 'sprite' : YELLOW},
    'T' : {'shape' : [(0, 0), (-1, 0), (1, 0), (0, -1)], 'sprite' : PURPLE},
    'S' : {'shape' : [(0, 0), (-1, 0), (0, -1), (1, -1)], 'sprite' : GREEN},
    'Z' : {'shape' : [(0, 0), (1, 0), (0, -1), (-1, -1)], 'sprite' : RED},
    'L' : {'shape' : [(0, 0), (0, -1), (0, 1), (1, 1)], 'sprite' : BLUE},
    'J' : {'shape' : [(0, 0), (0, -1), (0, 1), (-1, 1)], 'sprite' : ORANGE},
    'I' : {'shape' : [(0, 0), (0, -1), (0, -2), (0, 1)], 'sprite' : CYAN},
}