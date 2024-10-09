import sys
from settings import *
from game import Game

class Application: #Application class
    def __init__(self):
        pg.init() #Initialise pygame
        pg.display.set_caption("Tetris") #Set title for application window
        self.window = pg.display.set_mode(WINDOW_RESOLUTION) #Set window resolution
        self.clock = pg.time.Clock() #Create clock for the app

        self.game = Game() #Create instance of game object

    def update(self):
        self.clock.tick(FPS) #Tick clock with FPS value

    #Draw function to update window display
    def draw(self):
        self.window.fill(LITE_GREY) #Fill window background with colour
        self.game.run() 
        pg.display.update() 

    #Check event loop 
    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT: #checking for quit event
                pg.quit() #quit pygame
                sys.exit() #close window

    def run(self):
        while True: #Running loop
            self.check_events()
            self.update()
            self.draw()


if __name__ == "__main__":
    app = Application()
    app.run()


