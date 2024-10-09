from settings import *
from random import choice
from timer import Timer
from sys import exit

#Game Class
class Game:
    def __init__(self): #Object initialiser function

        self.grid_container = pg.Surface((GRID_WIDTH, GRID_HEIGHT))
        self.window = pg.display.get_surface()
        self.border = self.grid_container.get_rect(topleft = (WINDOW_PADDING, WINDOW_PADDING))

        self.sprites = pg.sprite.Group()

        self.gridlines = self.grid_container.copy()
        self.gridlines.fill((0, 255, 0))
        self.gridlines.set_colorkey((0, 255, 0))
        self.gridlines.set_alpha(120)

        self.grid_data = [[0 for x in range(COL_NUMBER)] for y in range(ROW_NUMBER)]
        self.tetromino = Tetromino(choice(list(TETROMINOS.keys())), self.sprites, self.new_tetromino, self.grid_data)
        
        self.down_speed = TIMER_INTERVAL
        self.speed_multiplier = self.down_speed * 0.3
        self.down_pressed = False
        self.timers = {
            'vertical move' : Timer(self.down_speed, True, self.move_down),
            'horizontal move' : Timer(MOVE_DELAY),
            'rotate' : Timer(ROTATE_DELAY)
        }
        self.timers['vertical move'].activate_timer()

    def draw_grid(self): #Draw grid lines function
        for column in range(1, COL_NUMBER):
            x = column * CELL_SIZE
            pg.draw.line(self.gridlines, WHITE, (x, 0), (x, self.grid_container.get_height()), 1)
        
        for row in range(1, ROW_NUMBER):
            y = row * CELL_SIZE
            pg.draw.line(self.gridlines, WHITE, (0, y), (self.grid_container.get_width(), y), 1)

        self.grid_container.blit(self.gridlines, (0, 0))

    def new_tetromino(self): #Create new tetromino
        self.check_game_over() #check if game over condition is met
        self.check_complete_row() #check if a row is completed
        self.tetromino = Tetromino(choice(list(TETROMINOS.keys())), self.sprites, self.new_tetromino, self.grid_data) #create new tetromino

    def update_timer(self): #Update timer function
        for timer in self.timers.values():
            timer.update()

    def move_down(self): #Move block down function
        self.tetromino.move_down()

    def check_complete_row(self):
        complete_rows = [] #complete_rows is empty list

        #for every row in the grid, check if it is completed, then add completed row to completed_rows
        for i, row in enumerate(self.grid_data):
            if all(row):
                complete_rows.append(i)

        #if completed_rows is not empty, for every row in the list, kill every square object 
        if complete_rows:
            for completed_row in complete_rows:
                for square in self.grid_data[completed_row]:
                    square.kill()
                
                #for every row in grid_data, move all squares down by 1 square
                for row in self.grid_data:
                    for square in row:
                        if square and square.position.y < completed_row:
                            square.position.y += 1
            self.grid_data = [[0 for x in range(COL_NUMBER)] for y in range(ROW_NUMBER)] #update grid_data with new layout after all rows are moved down
            for square in self.sprites:
                self.grid_data[int(square.position.y)][int(square.position.x)] = square

    def input(self): #check for input to move pieces
        keys = pg.key.get_pressed()

        if not self.timers['horizontal move'].active:

            if keys[pg.K_LEFT] or keys[pg.K_a]:
                self.tetromino.move_horizontally(-1)
                self.timers['horizontal move'].activate_timer()
            if keys[pg.K_RIGHT] or keys[pg.K_d]:
                self.tetromino.move_horizontally(1)
                self.timers['horizontal move'].activate_timer()

        if not self.timers['rotate'].active:
            if keys[pg.K_UP] or keys[pg.K_w]:
                self.tetromino.rotate()
                self.timers['rotate'].activate_timer()
        
        if not self.down_pressed and keys[pg.K_DOWN]:
            self.down_pressed = True
            self.timers['vertical move'].time = self.speed_multiplier

        if self.down_pressed and not keys[pg.K_DOWN]:
            self.down_pressed = False
            self.timers['vertical move'].time = self.down_speed

    def check_game_over(self):
        for square in self.tetromino.squares:
            if square.position.y < 0:
                exit()

    def draw(self): #Draw to screen function
        self.grid_container.fill(LITE_GREY)
        self.sprites.draw(self.grid_container)

    def run(self): #Run the game
        self.input()
        self.update_timer()
        self.sprites.update()

        self.draw()
        self.draw_grid()
        self.window.blit(self.grid_container, (WINDOW_PADDING, WINDOW_PADDING))
        pg.draw.rect(self.window, WHITE, self.border, 2, 2)




#Square class for individual blocks
class Square(pg.sprite.Sprite):
    def __init__(self, group, position, sprite):
        super().__init__(group)
        self.image = pg.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill(sprite)

        self.position = pg.Vector2(position) + pg.Vector2(4, 1)
        x = self.position.x * CELL_SIZE
        y = self.position.y * CELL_SIZE

        self.rect = self.image.get_rect(topleft = (x, y))

    def rotate(self, pivot):
        distance = self.position - pivot
        rotated = distance.rotate(90)
        new_position = pivot + rotated
        return new_position

    def horizontal_collision(self, x, grid_data):
        if not 0 <= x < COL_NUMBER:
            return True
        
        if grid_data[int(self.position.y)][x]:
            return True
        
    def vertical_collision(self, y, grid_data):
        if not 0 <= y < ROW_NUMBER:
            return True
        
        if grid_data[y][int(self.position.x)]:
            return True

    def update(self):
        self.rect.topleft = self.position * CELL_SIZE



#Tetromino class made up of 4 squares
class Tetromino:
    def __init__(self, shape, group, new_tetromino, grid_data):
        self.shape = shape
        self.block_positions = TETROMINOS[shape]['shape']
        self.sprite = TETROMINOS[shape]['sprite']
        self.new_tetromino = new_tetromino
        self.grid_data = grid_data

        self.squares = [Square(group, position, self.sprite) for position in self.block_positions]

    #collisions
    def horizontal_boundary(self, squares, value):
        collisions = [square.horizontal_collision(int(square.position.x + value), self.grid_data) for square in squares]
        
        if any(collisions):
            return True
        else:
            return False
        
    def vertical_boundary(self, squares, value):
        collisions = [square.vertical_collision(int(square.position.y + value), self.grid_data) for square in squares]

        if any(collisions):
            return True
        else:
            return False

    def move_down(self):
        if not self.vertical_boundary(self.squares, 1):
            for square in self.squares:
                square.position.y += 1
        else:
            for square in self.squares:
                self.grid_data[int(square.position.y)][int(square.position.x)] = square
            self.new_tetromino()
    
    def move_horizontally(self, value):
        if not self.horizontal_boundary(self.squares, value):
            for square in self.squares:
                square.position.x += value

    def rotate(self):
        if self.shape != 'O':
            pivot = self.squares[0].position
            rotated_shape = [square.rotate(pivot) for square in self.squares]

            for position in rotated_shape:
                #horizontal checks
                if position.x < 0 or position.x >= COL_NUMBER:
                    return
            
                #field check
                if self.grid_data[int(position.y)][int(position.x)]:
                    return

                #vertical checks
                if position.y > ROW_NUMBER:
                    return

            for i, square in enumerate(self.squares):
                square.position = rotated_shape[i]

            