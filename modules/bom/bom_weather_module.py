# -*- coding: UTF-8 -*-

import time
import pygame
try:
    from urllib.request import Request, urlopen, URLError
except ImportError:
    from urllib2 import Request, urlopen, URLError
    # For python2.7 compatability:
    FileNotFoundError = None
import config.settings as settings
import config.translations as translations
from debug_output import timestamp


def fetch_weather_info():
    '''
    fetch_weather_info() -> parse_weather_info()
    See _parse_weather_info for more details on return type.

    Fetches weather info and manages request frequency and data saving.
    To get weather info call this function, not _parse_weather_info unless
    you know what you're doing and don't require flood control or saved
    data return.
    '''

    # Planned features:
    #  - Ability to use multiple services
    #  - Try again on network failure

    timestamp("Fetching weather...")
    save_path = settings.saved_weather_data_path
    connection_attempts = 0
    try:
        with open(save_path, "r") as save_data:
            # Get elapsed time since update and check against update delay:
            time_since_check = time.time() - int(save_data.readline())
            if time_since_check > settings.weather_update_delay:
                # Raises to trigger data update in except clause:
                raise IOError
            else:
                result = str(save_data.read())
    # Exception if weather_data can't be opened:
    except(IOError, FileNotFoundError):
        # Fetch data from a URL and save it to weather_data,
        # then call self:
        with open(save_path, "w") as save_data:
            current_time = str(int(time.time()))
            try:
                bom_data = urlopen(Request(
                    settings.weather_url)).read().decode("utf-8")
            except URLError:
                connection_attempts += 1
                if connection_attempts != settings.attempts:
                    timestamp("Failed to connect, trying again in 5 seconds.")
                    time.sleep(5)
                    return fetch_weather_info()
                else:
                    timestamp("Failed to connect {} times. Quitting...").format(
                        settings.attempts
                    )
                    pygame.quit()
                    quit()
            save_data.write("{}\n{}".format(current_time, bom_data))
        return fetch_weather_info()
    except ValueError:
        timestamp("Error in file, deleting and retrying download.")
        remove(save_path)
        return fetch_weather_info()
    # Return resulting weather data after parsing:
    timestamp("Completed fetching weather...")
    return parse_weather_info(settings.weather_city, result)


def parse_weather_info(city, data):
    '''parse_weather_info(city, data) -> (city, temperature, description, icon)

    Parses bureau of meteorology IDA00100.dat file from their FTP server and
    returns city name, temperature, current conditions and the appropriate
    icon to represent the weather. Call through fetch_weather_info().
    '''

    # Planned features:
    #  - 7-day forecast
    #  - Merge with fetch_weather_info()

    string, result, index = "", [], data.find(city.title())
    while True:
        string = string + data[index]
        index += 1
        if string[-1] == "#":
            result.append(string[0:-1])
            string = ""
            continue
        if string[-1] == "\n":
            break
    description = result[-1].lower()
    condition = [condition for condition in translations.conditions
                 if description.find(condition) != -1]
    if len(condition) > 0:
        condition = translations.conditions[condition[0]]
    else:
        condition = u""
    temperature, description = result[-2], result[-1].title()
    return (city, temperature, description, condition)