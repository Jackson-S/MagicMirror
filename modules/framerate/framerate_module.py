# -*- coding: UTF-8 -*-
""" Displays the framerate, kind of useless now, since the
    program has dynamic framerate based on current needs, but
    I'm leaving it in here anyway
"""

from modules.BaseModule import BaseModule

from debug_output import timestamp


class FramerateModule(BaseModule):
    """Displays the framerate"""

    def __init__(self, clock):
        timestamp("Initialising FramerateModule...")
        super(FramerateModule, self).__init__()
        self.clock = clock
        self.updatedelay = 1

    def update(self):
        """called when update is triggered. return next item"""
        fps = self.font.render("{} fps. Press Esc to quit.".format(
            int(round(self.clock.get_fps()))), 1, self.colour)
        fps_pos = fps.get_rect(right=self.width * 0.995, top=0)
        return [[fps, fps_pos]]
