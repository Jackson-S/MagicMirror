# -*- coding: UTF-8 -*-
''' This is a sample hello world module that can be used as a template to
    create new modules.
'''

# Required imports, any further imports
# that you require for your module should be placed
# below these:
import time
import pygame
from debug_output import timestamp


class SampleModule(object):
    '''Prints "hello" and "world" to each corner of the display'''
    def __init__(self, width, height, colour):
        '''Called once, create anything you require for future updates,
        and anything you require across more than one function here
        '''
        # Set the screen width and height:
        self.width, self.height = width, height

        # Set the colour:
        self.colour = colour

        # Set the font for the module, define the size of the font as the height
        # multiplied by the desired size to allow compatability with different
        # screen resolutions, must be defined as an integer however:
        self.font = pygame.font.Font("resources/font-light.ttf", int(self.height*0.1))

        # time before the module update function is called again,
        # to allow for the display to be updated (seconds).
        self.updatedelay = 10

        # Setting this will trigger the initial update time,
        # so have this set to either 0 or time.time()
        self.nextupdatetime = 0

    def update(self):
        '''called when update is triggered, and should return
        an array of arrays, each sub-array should contain one
        pygame object, and one pygame rect
        '''
        # Add a timestamp to stdout on each update call, priority
        # 0 ensures that it won't pop up constantly, priority=1
        # ensures output will be seen no matter what debug settings
        # are enabled, and should be used sparingly:
        timestamp("Updating HelloWorldModule...", priority=0)

        # Defines text objects hello and world,
        # any pygame object can be used:
        hello = self.font.render("Hello", 1, self.colour)
        world = self.font.render("World", 1, self.colour)

        # Places "hello" in the top left of the screen:
        hello_pos = hello.get_rect(left=0, top=0)

        # Places "world" in the bottom right of the screen:
        world_pos = world.get_rect(right=self.width, bottom=self.height)

        # Returns "hello" with position of hello,
        # and "world" with the position of the text:
        return [[hello, hello_pos], [world, world_pos]]

    def need_update(self):
        '''called once per frame, returns true if update() needs to be called,
        if true is returned update will be called while drawing the current
        frame, after calling need_update() on all installed modules.
        '''
        if time.time() >= self.nextupdatetime:
            self.nextupdatetime = time.time() + self.updatedelay
            return True
        else:
            return False


# FINALLY:
# To load your module add it to the import list of main.py,
# and then add it to the marked area of the main() function in
# main.py as shown.
