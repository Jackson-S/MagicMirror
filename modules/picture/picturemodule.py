# -*- coding: UTF-8 -*-
"""Displays pictures in the background"""

import time
from os import listdir, path
from random import shuffle

import pygame

from config.settings import picturepath, picture_delay_time

from debug_output import timestamp


class PictureModule(object):
    """Displays images in the background"""

    def __init__(self, width, height):
        """ Called once, create anything you require for future updates,
            and anything you require across more than one function here
        """
        self.width, self.height = width, height
        self.updatedelay = picture_delay_time
        self.nextupdatetime = 0
        self.counter = 0
        self.images = self.get_images()

    def update(self):
        """ called when update is triggered, and should return
            an array of arrays, each sub-array should contain one
            pygame object, and one pygame rect
        """
        timestamp("Updating picture module...")

        # Return image counter to 0 to properly scroll through images.
        if len(self.images) == 0:
            self.updatedelay = int(2e16)
            return []
        try:
            image, imagepos = self.resize(
                pygame.image.load(self.images[
                    self.counter % len(self.images)
                    ]))
            image.convert()
            image.set_alpha(128)
            self.counter += 1
        except pygame.error:
            # If something goes wrong (not a properly formed image for example)
            # retry on the next image:
            timestamp("Image update failed, trying again...")
            return self.update()
        timestamp("Completed updating picture module...")
        return [[image, imagepos]]

    def get_images(self):
        pictures = listdir(path=picturepath)
        result = [path.join(picturepath, "{}".format(item)) for item in pictures
                  if item.lower().endswith("jpg") or
                  item.lower().endswith("png") or
                  item.lower().endswith("bmp")]
        shuffle(result)
        return result

    def resize(self, image):
        """ Correctly resize the image for display, cropping edges to achieve
            a full screen sized image
        """
        size = image.get_rect(left=0, top=0)
        x, y = size[2], size[3]
        if y >= x:
            image = pygame.transform.smoothscale(
                image,
                (int((x / y) * self.height), self.height)
                )
        else:
            image = pygame.transform.smoothscale(
                image,
                (self.width, int((y / x) * self.width))
                )
        return image, image.get_rect(centerx=self.width / 2, centery=self.height / 2)

    def need_update(self):
        """ called once per frame, returns true if update() needs to be called,
            if true is returned update will be called while drawing the current
            frame, after calling need_update() on all installed modules.
        """
        if time.time() >= self.nextupdatetime:
            self.nextupdatetime = time.time() + self.updatedelay
            return True
        else:
            return False
