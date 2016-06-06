#!/usr/bin/env/python
# -*- coding: UTF-8 -*-

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
' Python based magic mirror application, based on pygame  '
' library as well as Reddit and BOM weather data. No      '
' license as of yet, unfinished work.                     '
'                                                         '
'                                  Jackson Sommerich 2016 '
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

from __future__ import print_function
from urllib2 import Request, urlopen
from sys import argv
from platform import system

import time
import pygame
import praw

# Import external settings files:
import settings
import weather_data
import display


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
    #  - Change save file location

    try:
        with open("resources/saved_weather_data", "r") as save_data:
            # Get elapsed time since update and check against update delay:
            time_since_check = time.time() - float(save_data.readline())
            if time_since_check > settings.weather_update_delay:
                # Raises to trigger data update in except clause:
                raise IOError
            else:
                result = str(save_data.read())

    # Exception if saved_weather_data can't be opened:
    except IOError:
        # Fetch data from a URL and save it to saved_weather_data,
        # then call self:
        with open("resources/saved_weather_data", "w") as save_data:
            current_time = str(time.time())
            bom_data = str(urlopen(Request(settings.weather_url)).read())
            save_data.write("{}\n{}".format(current_time, bom_data))
        return fetch_weather_info()
    # Return resulting weather data after parsing:
    return parse_weather_info(settings.weather_city, result)


def parse_weather_info(city, data):
    '''parse_weather_info(city, data) ->
    (city, temperature, description, icon)

    Parses bureau of meteorology IDA00100.dat file from their FTP server and
    returns city name, temperature, current conditions and the appropriate
    icon to represent the weather. Call through fetch_weather_info().'''

    # Planned features:
    #  - distinguising between night and day
    #  - 7-day forecast

    # Initialise variables, index = position of the city in the string,
    # also acts as the cursor to the string:
    string, result, index = "", [], data.find(city)

    while True:
        # Add the next letter to the string and increment the cursor by 1:
        string = string + data[index]
        index += 1

        # "#" is the seperator character in the IDX00100.dat file supplied
        # by the ABS. This seperates each data entry.
        if string[-1] == "#":
            result.append(string[0:-1])
            string = ""
            continue

        # Newline indicaates moving to the next city:
        if string[-1] == "\n":
            break

    # Converts the description (last entry in the IDA00100.dat file) to
    # lower-case, an array of weather conditions is then used to find
    # a single-word descriptor of the current weather for use as a
    # weather icon as none is supplied.
    # Typical...
    description = result[-1].lower()
    condition = [condition for condition in weather_data.conditions
                 if description.find(condition) != -1]

    # Format the condition for a picture descriptor by looking in a
    # predefined dictionary (located in weather settings), which
    # contains the appropriate icon for the found descriptor
    if len(condition) != 0:
        condition = "{}.png".format(weather_data.translation[condition[0]])

    # If the description doesn't contain relevant info then use
    # a gigantic question mark picture because again, no single
    # word weather info is supplied.
    else:
        condition = "unknown.png"
    temperature, description = result[-2], result[-1].title()

    return (city, temperature, description, condition)


def get_news(subreddit):
    '''get_news(subreddit: str) -> news: [str]'''
    user_agent = settings.user_agent.format(system(), settings.version)
    reddit, result = praw.Reddit(user_agent=user_agent), {}
    submission = reddit.get_subreddit(subreddit).get_top_from_day(limit=settings.item_count)
    result = []
    for story in submission:
        result.append(story.title)
    return result


def truncate(content, title=False, length=65, suffix='...'):
    '''truncate(content, [title: bool], [length: int], [suffix: str])
    -> unicode'''
    if title:
        content = content.title()
    if len(content) <= length:
        return unicode(content)
    else:
        return unicode(' '.join(content[:length+1].split(' ')[0:-1]) + suffix)


def main():
    '''main() -> None
    UI of the program, calls all other modules.'''

    # Planned features:
    #  - Auto-refresh
    #  - News
    #  - Multiple weather sources
    #  - Resolution independence (maybe)
    #  - Font options
    #  - Icons to text (using OW font)
    #  - Automatic on/off based on motion/light sensor

    # Init pygame display:
    pygame.init()
    # Resoltion, hardcoded, don't change, will probably break things:
    screen_size = settings.resolution
    # Pure black for background:
    background_colour = (0, 0, 0)
    # Pure white for main text:
    white_text_colour = (255, 255, 255)
    # 50% grey for weather icons and subtext:
    grey_text_colour = (128, 128, 128)
    # Sets display modes to be injected into set_mode:

    default = "window"
    if len(argv) == 2:
        try:
            modes = display.modes[argv[1]]

        # Exception for invalid key:
        except KeyError:
            print("Unknown mode, using default of \"{}\"".format(default))
            modes = display.modes[default]
            time.sleep(1)
    # If no mode is specified
    else:
        modes = display.modes[default]

    # Enables clock, used for frame rate limiter:
    game_clock = pygame.time.Clock()

    # Sets font options and sizes, TTF fonts only:
    font = pygame.font.Font("resources/font.ttf", 52)
    font2 = pygame.font.Font("resources/font.ttf", 40)
    font3 = pygame.font.Font("resources/font.ttf", 22)
    font4 = pygame.font.Font("resources/font.ttf", 30)

    # Initialises the display
    screen = pygame.display.set_mode(screen_size, modes)
    screen.fill(background_colour)
    loading_font = pygame.font.Font("resources/font.ttf", 80)
    loading_text = loading_font.render("Loading...", 1, white_text_colour)
    loading_text_pos = loading_text.get_rect(
        centerx=screen.get_width()/2, centery=screen.get_height()/2)
    screen.blit(loading_text, loading_text_pos)
    pygame.display.flip()

    # fetches data for weather info:
    weather_info = fetch_weather_info()

    # Sets text for weather info, (text, antialiasing, colour, [background]):
    city_text = font.render(weather_info[0], 1, white_text_colour)
    # \xb0 = º:
    temp_text = font2.render("{}\xb0C".format(weather_info[1])
                             , 1, white_text_colour)
    condition_text = font3.render(str(weather_info[2]), 1, white_text_colour)
    weather_icon = pygame.image.load("resources/{}".format(weather_info[3]))

    sub_offset, news, stories, stories_pos = -10, [], [], []
    for sub in settings.subreddits:
        news = []
        news.extend(get_news(sub))
        sub_offset += 10
        stories.append(font4.render(truncate(sub, True), 1, white_text_colour))
        stories_pos.append(stories[-1].get_rect(left=285, top=sub_offset))
        sub_offset += 34
        for story in news:
            stories.append(font3.render(truncate(story), 1, white_text_colour))
            height = sub_offset
            stories_pos.append(stories[-1].get_rect(left=300, top=(height)))
            sub_offset += 26

    # Gets size information for weather text for positioning:
    city_textpos = city_text.get_rect(left=10, top=0)
    temp_text_pos = temp_text.get_rect(right=250, top=170)
    condition_text_pos = condition_text.get_rect(right=250, top=220)
    weather_icon = pygame.transform.smoothscale(weather_icon, (250, 250))
    weather_icon_pos = weather_icon.get_rect(left=20, top=50)

    while True:
        # Checks for keyboard events and quits if necessary:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

        # Sets the framerate (located in settings.py):
        game_clock.tick(settings.fps_limit)
        # Draws the background:
        screen.fill(background_colour)

        # Blits each element to the screen (element, position):
        screen.blit(weather_icon, weather_icon_pos)
        screen.blit(city_text, city_textpos)
        screen.blit(temp_text, temp_text_pos)
        screen.blit(condition_text, condition_text_pos)
        for story, story_pos in zip(stories, stories_pos):
            screen.blit(story, story_pos)
        # Renders the fps counter:
        if settings.display_fps:
            fps = str(round(game_clock.get_fps()))
            fps = font3.render("{} fps. Press Esc to quit.".format(fps[0]),
                               1, grey_text_colour)
            screen.blit(fps, fps.get_rect(left=10, bottom=screen.get_height() - 10))
        pygame.display.flip()


if __name__ == '__main__':
    main()
