# -*- coding: UTF-8 -*-
'''Displays a loading screen while other modules load'''
import pygame


class LoadingModule(object):
    '''Displays the loading screen at the start of the program'''
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def update(self):
        '''called when update is triggered. return next item'''
        font = pygame.font.Font("resources/font-heavy.ttf", int(self.height*0.14))
        text = font.render("Loading...", 1, (255, 255, 255))
        textpos = text.get_rect(left=0, bottom=self.height)
        return (text, textpos)
