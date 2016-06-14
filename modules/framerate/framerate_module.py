# -*- coding: UTF-8 -*-
""" Displays the framerate, kind of useless now, since the
    program has dynamic framerate based on current needs, but
    I'm leaving it in here anyway
"""

import time

from debug_output import timestamp


class FramerateModule(object):
    """Displays the framerate"""

    def __init__(self, width, height, colour, font, clock):
        timestamp("Initialising FramerateModule...")
        self.width = width
        self.height = height
        self.clock = clock
        self.font = font
        self.colour = colour
        self.nextupdatetime = time.time()

    def update(self):
        """called when update is triggered. return next item"""
        fps = self.font.render("{} fps. Press Esc to quit.".format(
            int(round(self.clock.get_fps()))), 1, self.colour)
        fps_pos = fps.get_rect(right=self.width * 0.995, top=0)
        return [[fps, fps_pos]]

    def need_update(self):
        """Returns true if update required"""
        if time.time() >= self.nextupdatetime:
            self.nextupdatetime = time.time() + 1
            return True
        else:
            return False
