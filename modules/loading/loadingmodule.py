# -*- coding: UTF-8 -*-
"""Displays a loading screen while other modules load"""

from modules.BaseModule import BaseModule


class LoadingModule(BaseModule):
    """Displays the loading screen at the start of the program"""

    def __init__(self):
        super(LoadingModule, self).__init__()

    def update(self):
        """called when update is triggered. return next item"""
        text = self.font[0].render("Loading...", 1, self.colour)
        textpos = text.get_rect(left=0, bottom=self.height)
        return text, textpos
