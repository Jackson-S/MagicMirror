# -*- coding: UTF-8 -*-
""" Shows weather conditions for the current day from the Australian
    Bureau of Meteorology
"""

from os import remove

from modules.BaseModule import BaseModule
from modules.VerboseOutput import timestamp
from settings import (saved_weather_data_path,
                      weather_update_delay,
                      weather_city,
                      )


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
            condition = conditions[condition[-1]]
        else:
            condition = conditions[unknown]
        temp = result[-2]
        desc = result[-1].title()
        item = (
            self.font[1].render(weather_city, 1, self.colour),
            self.font[5].render(condition[0], 1, self.colour),
            self.font[3].render(desc, 1, self.colour),
            self.font[2].render("{}\xb0c".format(temp), 1, self.colour)
        )
        heights = (
            item[0].get_rect(left=0, top=0)[3] * condition[1][0],
            item[1].get_rect(left=0, top=0)[3] * condition[1][1],
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


conditions = {"sun": (u"", [0.7, 0.9]),
              "clear": (u"", [0.7, 0.9]),
              "cloud": (u"", [0.3, 0.8]),
              "rain": (u"", [0.3, 1]),
              "heavy rain": (u"", [0.3, 1]),
              "shower": (u"", [0.3, 1]),
              "storm": (u"", [0.3, 1]),
              "thunder": (u"", [0.3, 1]),
              "lightning": (u"", [0.3, 1]),
              "hail": (u"", [0.3, 1]),
              "snow": (u"", [0.3, 1]),
              "cyclone": (u"", [0.3, 1]),
              "wind": (u"", [0.3, 0.92]),
              "partly cloudy": (u"", [0.3, 0.85]),
              "light showers": (u"", [0.3, 0.9]),
              "light rain": (u"", [0.3, 0.9]),
              "tornado": (u"", [0.35, 0.8]),
              "overcast": (u"", [0.3, 0.8]),
              "unknown": (u"", [-0.2, 0.7])
              }
