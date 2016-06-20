import time

import pygame

from settings import colour, fonts


class BaseModule(object):
    def __init__(self):
        self.width, self.height = pygame.display.get_surface().get_size()
        self.colour = colour[2]
        self.font = [pygame.font.Font(ttf, int(pt * self.height)) for ttf, pt in fonts]
        self.updatedelay = 10
        self.nextupdatetime = time.time()

    def need_update(self):
        if time.time() >= self.nextupdatetime:
            self.nextupdatetime = time.time() + self.updatedelay
            return True
        else:
            return False
