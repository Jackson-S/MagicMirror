# -*- coding: UTF-8 -*-
from settings import resolution
import pygame

###########################################################################
# The strings in this file can all be translated into another language if #
# someone is kind enough to volunteer and keep it up to date.             #
# Non-latin character sets excluding cyrillic may not render correctly    #
# due to font errors.                                                     #
###########################################################################

# Conditions are searched through by the weather parser and the keys
# are the icon in unicode and the offset required by the weather icon.
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

# These are the command line launch options. Feel free to translate them,
# but don't change the pygame.* values as this will likely break things.
modes = {
         "--fullscreen": pygame.FULLSCREEN,
         "--hwacceleration": pygame.DOUBLEBUF | pygame.HWSURFACE,
         "--hwfullscreen": pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.FULLSCREEN,
         "--doublebuffered": pygame.DOUBLEBUF,
         "--noframe": pygame.NOFRAME,
         "--window": 0,
         "--pi": pygame.FULLSCREEN
         }

# Text displayed at launch
loading_text = "Loading..."