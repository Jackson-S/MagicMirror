import time
import pygame
import praw
import config.settings as settings
from debug_output import timestamp
from platform import system


class TimeModule():
    def __init__(self, width, height, colour, font):
        timestamp("Initialising time module")
        self.width = width
        self.height = height
        self.colour = colour
        self.font = font
        self.nextupdatetime = time.time()

    def update(self):
        year, month, day, hour, minute, second = time.localtime()[0:6]
        am_pm = "am"
        if hour > 12:
            am_pm = "pm"
        date_disp = self.font.render("{}-{}-{}".format(year, month, day), 1, self.colour)
        # TO FIX:
        if minute < 10:
            time_disp = self.font.render("{}:0{} {}".format(hour % 12, minute, am_pm), 1, self.colour)
        else:
            time_disp = self.font.render("{}:{}".format(hour, minute), 1, self.colour)
        date_pos = date_disp.get_rect(right=self.width*0.98, top=self.height*0.01)
        time_pos = time_disp.get_rect(right=self.width*0.98, top=self.height*0.01 + date_pos[3])
        return((date_disp, date_pos), (time_disp, time_pos))

    def need_update(self):
        if time.time() >= self.nextupdatetime:
            self.nextupdatetime = time.time() + 10
            return True
        else:
            return False