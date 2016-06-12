# -*- coding: UTF-8 -*-
from config.settings import resolution
import pygame

###########################################################################
# The strings in this file can all be translated into another language if #
# someone is kind enough to volunteer and keep it up to date.             #
# Non-latin character sets excluding cyrillic may not render correctly    #
# due to font errors.                                                     #
###########################################################################

# Conditions are searched through by the weather parser and the keys
# are the icon in unicode and the offset required by the weather icon.
conditions = {"sun": (u""),
              "clear": (u""),
              "cloud": (u""),
              "rain": (u""),
              "heavy rain": (u""),
              "shower": (u""),
              "storm": (u""),
              "thunder": (u""),
              "lightning": (u""),
              "hail": (u""),
              "snow": (u""),
              "cyclone": (u""),
              "wind": (u""),
              "partly cloudy": (u""),
              "light showers": (u""),
              "tornado": (u""),
              "overcast": (u"")
             }

# These are the command line launch options. Feel free to translate them,
# but don't change the pygame.* values as this will likely break things.
modes = {"--fullscreen": pygame.FULLSCREEN,
         "--hwacceleration": pygame.DOUBLEBUF | pygame.HWSURFACE,
         "--hwfullscreen": pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.FULLSCREEN,
         "--doublebuffered": pygame.DOUBLEBUF,
         "--noframe": pygame.NOFRAME,
         "--window": 0,
         "--pi": pygame.FULLSCREEN
        }