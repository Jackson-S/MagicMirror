from settings import resolution
conditions = ["sun",
              "cloud",
              "rain",
              "heavy rain",
              "shower",
              "storm",
              "thunder",
              "lightning",
              "hail",
              "snow",
              "cyclone",
              "wind"
              "partly cloudy",
              "light showers",
              "tornado"]

translation = {"sun": "sun",
               "cloud": "cloud",
               "rain": "rain",
               "heavy rain": "heavy_rain",
               "shower": "rain",
               "storm": "storm",
               "thunder": "storm",
               "lightning": "storm",
               "hail": "hail",
               "snow": "snow",
               "cyclone": "tornado",
               "wind": "wind",
               "partly cloudy": "cloud",
               "light showers": "rain",
               "tornado": "tornado"}

# Magic numbers from pygame.MODE settings
modes = {"--fullscreen": -2147483648,
         "--hwacceleration": 1,
         "--hwfullscreen": -2147483647,
         "--doublebuffered": 1073741824,
         "--noframe": 32,
         "--window": 0
         }

# Sets the colour pallete for the program, black, grey, white:
colour = [
         (0, 0, 0),
         (128, 128, 128),
         (255, 255, 255)
         ]

# Sets font options and sizes, TTF fonts only:
fonts = [
        ("resources/font.ttf", int(0.14*resolution[1])),
        ("resources/font.ttf", int(0.086*resolution[1])),
        ("resources/font.ttf", int(0.067*resolution[1])),
        ("resources/font.ttf", int(0.037*resolution[1])),
        ("resources/font.ttf", int(0.05*resolution[1]))
        ]

disp_err_str = '''Unknown mode {}, using default of "{}"
supported modes are fullscreen, doublebuffered, noframe and window'''

loading_text = "Loading..."