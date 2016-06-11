import time
from debug_output import timestamp


class FramerateModule():
    def __init__(self, width, height, colour, font, clock):
        self.width = width
        self.height = height
        self.clock = clock
        self.font = font
        self.colour = colour
        self.nextupdatetime = time.time()

    def update(self):
        '''called when update is triggered. return next item'''
        fps = self.font.render("{} fps. Press Esc to quit.".format(
            int(round(self.clock.get_fps()))), 1, self.colour)
        fps_pos = fps.get_rect(right=self.width*0.995, top=0)
        fps2 = self.font.render(":)", 1, self.colour)
        fps2_pos = fps2.get_rect(right=0, top=0)
        return [[fps, fps_pos]]

    def need_update(self):
        if time.time() >= self.nextupdatetime:
            self.nextupdatetime = time.time() + 1
            return True
        else:
            return False