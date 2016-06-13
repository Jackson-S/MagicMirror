# -*- coding: UTF-8 -*-
'''Displays a loading screen while other modules load'''
import pygame


class LoadingModule(object):
    '''Displays the loading screen at the start of the program'''
    def __init__(self, width, height, colour, font):
        self.width = width
        self.height = height
        self.colour = colour
        self.font = font

    def update(self):
        '''called when update is triggered. return next item'''
        text = self.font.render("Loading...", 1, self.colour)
        textpos = text.get_rect(left=0, bottom=self.height)
        return (text, textpos)
