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

disp_err_str = '''Unknown mode {}, using default of "{}"
supported modes are fullscreen, doublebuffered, noframe and window'''

loading_text = "Loading..."