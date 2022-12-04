import pygame.time


class Timer:

    def __init__(self, duration_in_ms, func_to_be_executed_when_timer_stops = None):
        self.duration_in_ms = duration_in_ms
        self.func_to_be_executed_when_timer_stops = func_to_be_executed_when_timer_stops
        self.start_time = 0
        self.current_time = 0
        self._is_active = False

    @property
    def is_timer_active_read_only(self):
        return self._is_active

    @property
    def elapsed_time_read_only(self):
        if self.start_time != 0:
            return self.current_time - self.start_time
        return 0

    def activate(self):
        self._is_active = True
        self.start_time = pygame.time.get_ticks()

    def deactivate(self):
        self._is_active = False
        self.start_time = 0

    def update(self):
        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.start_time > self.duration_in_ms:
            self.deactivate()
            if self.func_to_be_executed_when_timer_stops: # if the is any
                self.func_to_be_executed_when_timer_stops()