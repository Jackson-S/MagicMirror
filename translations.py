# -*- coding: UTF-8 -*-
from settings import resolution
import pygame

conditions = {
             "sun": (u"", resolution[1]*0.047),
             "clear": (u"", resolution[1]*0.047),
             "cloud": (u"", 0),
             "rain": (u"", 0),
             "heavy rain": (u"", 0),
             "shower": (u"", 0),
             "storm": (u"", 0),
             "thunder": (u"", 0),
             "lightning": (u"", 0),
             "hail": (u"", 0),
             "snow": (u"", 0),
             "cyclone": (u"", 0),
             "wind": (u"", 0),
             "partly cloudy": (u"", 0),
             "light showers": (u"", 0),
             "tornado": (u"", 0),
             "overcast": (u"", 0)
             }

# Magic numbers from pygame.MODE settings
modes = {
         "--fullscreen": pygame.FULLSCREEN,
         "--hwacceleration": pygame.DOUBLEBUF | pygame.HWSURFACE,
         "--hwfullscreen": pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.FULLSCREEN,
         "--doublebuffered": pygame.DOUBLEBUF,
         "--noframe": pygame.NOFRAME,
         "--window": 0,
         }

# Sets the colour pallete for the program:
# 0 = black
# 1 = grey
# 2 = white
colour = [
         (0, 0, 0),
         (128, 128, 128),
         (255, 255, 255)
         ]

# Sets font options and sizes, TTF fonts only:
# 0 = Loading font
# 1 = City font
# 2 = Temperature title
# 3 = Weather description/News story/FPS counter
# 4 = Subreddit heading
fonts = [
        ("resources/font-heavy.ttf", int(0.14*resolution[1])),
        ("resources/font-heavy.ttf", int(0.086*resolution[1])),
        ("resources/font-heavy.ttf", int(0.067*resolution[1])),
        ("resources/font-light.ttf", int(0.037*resolution[1])),
        ("resources/font-regular.ttf", int(0.05*resolution[1])),
        ("resources/weather-icons.ttf", int(0.25*resolution[1]))
        ]

disp_err_str = '''Unknown mode {}, using default of "{}"
supported modes are fullscreen, doublebuffered, noframe and window'''

loading_text = "Loading..."