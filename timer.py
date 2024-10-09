from pygame.time import get_ticks

class Timer:
    def __init__(self, time, repeated = False, function = None):
        self.repeated = repeated
        self.function = function
        self.time = time

        self.start_time = 0
        self.active = False

    def activate_timer(self):
        self.active = True
        self.start_time = get_ticks()

    def deactivate_timer(self):
        self.active = False
        self.start_time = 0

    def update(self):
        current_time = get_ticks()
        if current_time - self.start_time >= self.time and self.active:

            #call a function
            if self.function and self.start_time != 0:
                self.function()

            #reset timer
            self.deactivate_timer()

            #repeat timer
            if self.repeated:
                self.activate_timer()