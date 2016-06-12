# -*- coding: UTF-8 -*-

import time
from os import remove
import pygame
try:
    from urllib.request import Request, urlopen, URLError
# For python2.7 compatability:
except ImportError:
    from urllib2 import Request, urlopen, URLError
    FileNotFoundError = None
import config.settings as settings
import config.translations as translations
from debug_output import timestamp


class BOMWeatherModule():
    def __init__(self, width, height, colour):
        timestamp("Initialising BOMWeatherModule module...")
        self.url = "ftp://ftp2.bom.gov.au/anon/gen/fwo/IDA00100.dat"
        fonts = [pygame.font.Font(ttf, int(size*height)) for ttf, size in settings.fonts]
        self.width, self.height = width, height
        self.colour = colour
        self.tempfont = fonts[2]
        self.cityfont = fonts[1]
        self.iconfont = fonts[5]
        self.descfont = fonts[3]
        self.conditiondict = translations.conditions
        self.delay = settings.weather_update_delay
        self.savepath = settings.saved_weather_data_path
        self.weatherdata = None
        self.city = settings.weather_city
        self.temp, self.desc, self.icon = "", "", ""
        self.bominfo = ""
        self.connectionattempts = 0
        self.nextupdatetime = time.time()

    def update(self):
        return self.parse_weather_info()

    def need_update(self):
        if time.time() >= self.nextupdatetime:
            self.nextupdatetime = time.time() + self.delay
            return True
        else:
            return False

    def parse_weather_info(self):
        '''Parses the weather from the BOM data file'''

        # Planned features:
        #  - Ability to use multiple services
        #  - Try again on network failure

        try:
            with open(self.savepath, "r") as save_data:
                # Get elapsed time since update and check against update delay:
                last_check = self.nextupdatetime - float(save_data.readline())
                if last_check > self.delay:
                    # Raises to trigger data update in except clause:
                    raise IOError
                else:
                    self.bominfo = str(save_data.read())
        # Exception if weather_data can't be opened:
        except(IOError, FileNotFoundError):
            self.ioerror()
            return self.parse_weather_info()
        except ValueError:
            remove(self.savepath)
            self.ioerror()
            return self.parse_weather_info()
        string, result = "", []
        index = self.bominfo.find(self.city.title())
        while True:
            string = string + self.bominfo[index]
            index += 1
            if self.bominfo[index] == "#":
                result.append(string[1:])
                string = ""
            if self.bominfo[index] == "\n":
                break
        desc = result[-1].lower()
        condition = [item for item in self.conditiondict if desc.find(item) != -1]
        if len(condition) > 0:
            self.icon = self.conditiondict[condition[0]]
        else:
            self.icon = u""
        self.temp = result[-2]
        self.desc = result[-1].title()
        item = (
            self.cityfont.render(self.city, 1, self.colour),
            self.iconfont.render(self.icon[0], 1, self.colour),
            self.descfont.render(self.desc, 1, self.colour),
            self.tempfont.render("{}\xb0c".format(self.temp), 1, self.colour)
            )
        heights = (
            item[0].get_rect(left=0, top=0)[3],
            item[1].get_rect(left=0, top=0)[3]*0.8,
            item[2].get_rect(left=0, top=0)[3],
            item[3].get_rect(left=0, top=0)[3]
            )
        itempos = (
            item[0].get_rect(left=self.width/100, top=0),
            item[1].get_rect(left=self.width/100, top=heights[0]*0.5),
            item[2].get_rect(left=self.width/100, top=sum(heights[0:2])),
            item[3].get_rect(left=self.width/100, top=sum(heights[0:3]))
            )
        return(
              (item[0], itempos[0]),
              (item[1], itempos[1]),
              (item[2], itempos[2]),
              (item[3], itempos[3])
              )

    def ioerror(self):
        timestamp("Save file read error occurred. Trying again.")
        with open(self.savepath, "w") as save_data:
            self.weatherdata = urlopen(Request(self.url))
            self.weatherdata = self.weatherdata.read().decode("utf-8")
            save_data.write(str(self.nextupdatetime))
            save_data.write("\n{}".format(self.weatherdata))
