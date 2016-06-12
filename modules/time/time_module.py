# -*- coding: UTF-8 -*-
'''Module to display a clock with the current time and date'''

import time
import config.settings as settings
from debug_output import timestamp


class TimeModule(object):
    '''Displays the time and date'''
    def __init__(self, width, height, colour, font):
        timestamp("Initialising time module")
        self.width = width
        self.height = height
        self.colour = colour
        self.font = font
        self.nextupdatetime = time.time()
        self.tformat = settings.time_format
        self.dformat = settings.date_format

    def update(self):
        '''Updates the time and date when called'''
        year, month, day, hour, minute = time.localtime()[0:5]
        date_string = self.dformat.format(y=year, m=month, d=day)
        if self.tformat == 0:
            time_string = "{h:02d}:{m:02d}".format(h=hour, m=minute)
        else:
            if hour > 12:
                period = "pm"
            else:
                period = "am"
            hour = hour % 13 + 1
            time_string = "{h}:{m:02d} {p}".format(h=hour, m=minute, p=period)
        date_disp = self.font.render(date_string, 1, self.colour)
        time_disp = self.font.render(time_string, 1, self.colour)
        date_pos = date_disp.get_rect(
            right=self.width*0.98,
            top=self.height*0.01
            )
        time_pos = time_disp.get_rect(
            right=self.width*0.98,
            top=self.height*0.01 + date_pos[3]
            )
        return((date_disp, date_pos), (time_disp, time_pos))

    def need_update(self):
        '''Returns true is update is required'''
        if time.time() >= self.nextupdatetime:
            self.nextupdatetime = time.time() + 10
            return True
        else:
            return False
