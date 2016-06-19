# -*- coding: UTF-8 -*-
""" Shows weather conditions for the current day from the Australian
    Bureau of Meteorology
"""

from os import remove

from modules.BaseModule import BaseModule
from config.settings import (saved_weather_data_path,
                             weather_update_delay,
                             weather_city,
                             )
from config.translations import conditions, offset
from debug_output import timestamp


class BOMWeatherModule(BaseModule):
    """Displays weather data from the Australian Bureau of Meteorology"""
    def __init__(self):
        timestamp("Initialising BOMWeatherModule module...")
        super(BOMWeatherModule, self).__init__()
        self.url = "ftp://ftp2.bom.gov.au/anon/gen/fwo/IDA00100.dat"
        self.savepath = saved_weather_data_path
        self.updatedelay = weather_update_delay
        self.weatherdata = None
        self.connectionattempts = 0

    def update(self):
        """Returns updated weather display"""
        # Catch errors from python 2
        try:
            FileNotFoundError
        except NameError:
            FileNotFoundError = IOError
        try:
            with open(saved_weather_data_path, "r") as save_data:
                # Get elapsed time since update and check against update delay:
                last_check = self.nextupdatetime - float(save_data.readline())
                if last_check > weather_update_delay:
                    # Raises to trigger data update in except clause:
                    raise FileNotFoundError("Old file")
                else:
                    self.weatherdata = str(save_data.read())
        # Exception if weather_data can't be opened:
        except FileNotFoundError:
            self.ioerror()
            return self.update()
        except ValueError:
            remove(saved_weather_data_path)
            self.ioerror()
            return self.update()
        string, result = "", []
        index = self.weatherdata.find(weather_city.title())
        while True:
            string += self.weatherdata[index]
            index += 1
            if self.weatherdata[index] == "#":
                result.append(string[1:])
                string = ""
            if self.weatherdata[index] == "\n":
                break
        desc = result[-1].lower()
        condition = [item for item in conditions
                     if desc.find(item) != -1]
        if len(condition) > 0:
            icon = conditions[condition[-1]]
        else:
            icon = u""
        temp = result[-2]
        desc = result[-1].title()
        item = (
            self.font[1].render(weather_city, 1, self.colour),
            self.font[5].render(icon[0], 1, self.colour),
            self.font[3].render(desc, 1, self.colour),
            self.font[2].render("{}\xb0c".format(temp), 1, self.colour)
        )
        heights = (
            item[0].get_rect(left=0, top=0)[3] * offset[icon][0],
            item[1].get_rect(left=0, top=0)[3] * offset[icon][1],
            item[2].get_rect(left=0, top=0)[3],
            item[3].get_rect(left=0, top=0)[3]
        )
        itempos = (
            item[0].get_rect(left=self.width / 100, top=0),
            item[1].get_rect(left=self.width / 100, top=heights[0]),
            item[2].get_rect(left=self.width / 100, top=sum(heights[0:2])),
            item[3].get_rect(left=self.width / 100, top=sum(heights[0:3]))
        )
        timestamp("Completed updating BOM module...")
        return (
            (item[0], itempos[0]),
            (item[1], itempos[1]),
            (item[2], itempos[2]),
            (item[3], itempos[3])
        )

    def ioerror(self):
        """Called in the case of a file read error. Re-downloads the file"""
        timestamp("Save file read error occurred. Trying again.")
        try:
            from urllib.request import Request, urlopen, URLError
        # For python 2 compatibility:
        except ImportError:
            from urllib2 import Request, urlopen, URLError
        try:
            with open(saved_weather_data_path, "w") as save_data:
                weatherurl = urlopen(Request(self.url))
                self.weatherdata = weatherurl.read().decode("utf-8")
                save_data.write(str(self.nextupdatetime))
                save_data.write("\n{}".format(self.weatherdata))
        except URLError:
            self.ioerror()
