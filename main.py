#!/usr/bin/env/python3
# -*- coding: UTF-8 -*-

###########################################################
# Python based magic mirror application, based on pygame  #
# library as well as Reddit and BOM weather data.         #
# Licensed under MIT license.                             #
#                                                         #
#                              (c) Jackson Sommerich 2016 #
###########################################################

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from sys import argv, version as pyver
from os import remove, uname
import time
import pygame
import config.settings as settings
import config.translations as translations
from modules.debug_output import timestamp
from modules.weather.weather import fetch_weather_info, parse_weather_info
import modules.time.time_module as time_module
import modules.news.news as news_module


def truncate(text, title=False, length=100):
    '''truncate(text, title: bool, length: int, suffix: str) -> unicode'''
    if title:
        text = text.title()
    try:
        if len(text) <= length:
            if (text[-1] != "?" or "." or "!" or ":") and not title:
                return u"{}{}".format(text, ".")
            else:
                return u"{}".format(text)
        else:
            return u" ".join(text[:length+1].split(" ")[:-1]) + u"…"
    except UnicodeError:
        return "Error parsing string"


def get_weather_display():
    '''returns the imagery and text for the weather display'''
    timestamp("Generating weather display...")
    # fetches data for weather info:
    weather_info = fetch_weather_info()
    # Sets text for weather info, (text, antialiasing, colour, [background]):
    # city_text, temp_text, condition_text, weather_icon then positions
    weather_text = (
        FONT[1].render(weather_info[0], 1, COLOUR[2]),
        FONT[5].render(weather_info[3][0], 1, COLOUR[2]),
        FONT[3].render(str(weather_info[2]), 1, COLOUR[2]),
        FONT[2].render("{}\xb0c".format(weather_info[1]), 1, COLOUR[2]),
        )
    heights = (
        weather_text[0].get_rect(left=0, top=0)[3],
        weather_text[1].get_rect(left=0, top=0)[3],
        weather_text[2].get_rect(left=0, top=0)[3],
        weather_text[3].get_rect(left=0, top=0)[3]
        )
    weather_text_pos = (
        weather_text[0].get_rect(left=WIDTH/100, top=0),
        weather_text[1].get_rect(left=WIDTH/100, top=heights[0]),
        weather_text[2].get_rect(left=WIDTH/100, top=sum(heights[0:2])),
        weather_text[3].get_rect(left=WIDTH/100, top=sum(heights[0:3]))
        )
    timestamp("Completed generating weather display...")
    return (weather_text, weather_text_pos)


def get_news_display():
    '''returns news text and rects'''
    timestamp("Generating news display...")
    subs = settings.subreddits
    stories, stories_pos, subreddit, subreddit_pos = [], [], [], []
    for sub in subs:
        item = []
        newsagent = news.News(sub)
        item.extend(newsagent.get_news())
        for story in item:
            stories.append(FONT[7].render(
                truncate(story), 1, COLOUR[2]))
            stories_pos.append(stories[-1].get_rect(
                left=WIDTH/100, bottom=HEIGHT-HEIGHT/200))
            subreddit.append(FONT[6].render(
                truncate(sub, title=True), 1, COLOUR[2]))
            subreddit_pos.append(subreddit[-1].get_rect(
                left=WIDTH/100, bottom=HEIGHT-stories_pos[-1][3]*0.8))
            story_right_edge = stories_pos[-1][2]
            # Check if the item item is wider than the screen edge:
            if story_right_edge > WIDTH:
                cuts = 0
                # Repeatedly truncate() the text until it fits:
                while story_right_edge > WIDTH:
                    stories[-1] = FONT[7].render(
                        truncate(story, length=len(story)-cuts), 1, COLOUR[2])
                    stories_pos[-1] = stories[-1].get_rect(
                        left=WIDTH/100, bottom=HEIGHT-HEIGHT/200)
                    story_right_edge = (stories_pos[-1][2] + 10)
                    cuts += 1
    timestamp("Completed generating item display...")
    return (subreddit, subreddit_pos, stories, stories_pos)


def get_alt_news_display():
    '''returns news text and rects'''
    timestamp("Generating news display...")
    subs = settings.subreddits
    sub_offset, news, stories, stories_pos = -10, [], [], []
    for sub in subs:
        news = []
        news.extend(get_news(sub))
        sub_offset += int(HEIGHT*0.017)
        stories.append(FONT[4].render(
            truncate(sub, title=True), 1, COLOUR[2]))
        stories_pos.append(stories[-1].get_rect(
            left=WIDTH*0.27, top=sub_offset))
        sub_offset += int(HEIGHT*0.057)
        for story in news:
            stories.append(FONT[3].render(
                truncate(story), 1, COLOUR[2]))
            stories_pos.append(stories[-1].get_rect(
                left=WIDTH/3.41, top=sub_offset))
            story_right_edge = (stories_pos[-1][2] + WIDTH * 0.26)
            # Check if the news item is wider than the screen edge:
            if story_right_edge > WIDTH*0.975:
                cuts = 0
                # Repeatedly truncate() the text until it fits:
                while story_right_edge > WIDTH*0.975:
                    stories[-1] = FONT[3].render(
                        truncate(story, length=(len(story)-cuts)), 1, COLOUR[2])
                    stories_pos[-1] = stories[-1].get_rect(
                        left=WIDTH/3.41, top=sub_offset)
                    story_right_edge = (stories_pos[-1][2] + WIDTH/3.41)
                    cuts += 1
            sub_offset += int(HEIGHT*0.043)
            # Check if the next news item will run off the screen:
            if sub_offset >= HEIGHT*0.96:
                break
    timestamp("Completed generating news display...")
    return (stories, stories_pos)


def get_display_mode():
    '''returns the desired display mode integer'''
    try:
        mode = argv[1]
    except IndexError:
        return translations.modes[settings.def_disp_mode]
    try:
        return translations.modes[mode]
    except KeyError:
        print(translations.disp_err_str.format(mode, settings.def_disp_mode))
        return translations.modes[settings.def_disp_mode]


def get_framerate(clock):
    '''Returns framerate font item and rect item'''
    fps = FONT[3].render("{} fps. Press Esc to quit.".format(
        int(round(clock.get_fps()))), 1, COLOUR[1])
    fps_pos = fps.get_rect(right=WIDTH-WIDTH/100, top=0)
    return (fps, fps_pos)


def check_events(events):
    '''Checks for keyboard events and quits if necessary'''
    for event in events:
        # 2 = pygame.KEYDOWN, 27 = pygame.K_ESCAPE
        if event.type == 2 and event.key == 27:
            timestamp("Quitting...")
            pygame.quit()
            quit()


def get_time():
    '''Gets the time and date, date format is D/M/Y'''
    year, month, day, hour, minute, second = time.localtime()[0:6]
    if hour > 12:
        am_pm = "pm"
    else:
        am_pm = "am"
    date_disp = FONT[1].render("{}-{}-{}".format(
        year, month, day), 1, COLOUR[2])
    # TO FIX:
    if minute < 10:
        time_disp = FONT[1].render("{}:0{} {}".format(
            hour % 12, minute, am_pm), 1, COLOUR[2])
    else:
        time_disp = FONT[1].render("{}:{}".format(
            hour, minute), 1, COLOUR[2])
    date_disp_pos = date_disp.get_rect(
        right=WIDTH*0.98, top=HEIGHT*0.01)
    time_disp_pos = time_disp.get_rect(
        right=WIDTH*0.98, top=HEIGHT*0.01+date_disp_pos[3])
    return((date_disp, time_disp), (date_disp_pos, time_disp_pos))


def main():
    '''main() -> None
    UI of the program, calls all other modules.
    '''

    # Planned features:
    #  - Multiple weather sources
    #  - Automatic on/off based on motion/light sensor

    timestamp("Initialising main program...")
    # Initialises the display
    # Enables clock, used for frame rate limiter:
    game_clock = pygame.time.Clock()
    pygame.mouse.set_visible(MOUSE_VISIBLE)
    modules = [
        news_module.NewsModule(SCREEN, COLOUR[2], FONT[6], FONT[7]),
        time_module.TimeModule(WIDTH, HEIGHT, COLOUR[2], FONT[1])
        ]
    module_display = [None]*len(modules)
    while True:
        SCREEN.fill(COLOUR[0])
        for module_no, module in enumerate(modules):
            if module.need_update() is True:
                module_display[module_no] = module.update()
        for module in module_display:
            for item, item_pos in module:
                SCREEN.blit(item, item_pos)
        game_clock.tick()
        check_events(pygame.event.get())
        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    # Mode specifically for my personal setup. Feel free to ignore it/remove it:
    if len(argv) > 1:
        # If running on a raspberry pi use --pi:
        if argv[1] == "--pi":
            RESOLUTION = WIDTH, HEIGHT = (1024, 600)
            SCREEN = pygame.display.set_mode((1024, 600), pygame.FULLSCREEN)
        # If using any other --option:
        else:
            if settings.autodetect_resolution is True:
                SCREEN = pygame.display.set_mode((0, 0), get_display_mode())
                RESOLUTION = WIDTH, HEIGHT = SCREEN.get_width(), SCREEN.get_height()
            else:
                RESOLUTION = WIDTH, HEIGHT = settings.resolution
                SCREEN = pygame.display.set_mode(RESOLUTION, get_display_mode())
    # If no arguments are passed:
    else:
        if settings.autodetect_resolution is True:
            SCREEN = pygame.display.set_mode((0, 0), get_display_mode())
            RESOLUTION = WIDTH, HEIGHT = SCREEN.get_width(), SCREEN.get_height()
        else:
            RESOLUTION = WIDTH, HEIGHT = settings.resolution
            SCREEN = pygame.display.set_mode(RESOLUTION, get_display_mode())
        # Generic settings
    FPS_LIMIT = settings.fps_limit
    MOUSE_VISIBLE = settings.mouse_visible
    TIMESTAMP = settings.timestamp
    SHOW_FPS = settings.display_framerate

    # Initialise the fonts and colours from translations.py:
    if settings.invert_colours:
        COLOUR = [(255, 255, 255), (0, 0, 0), (0, 0, 0)]
    else:
        COLOUR = [(0, 0, 0), (128, 128, 128), (255, 255, 255)]

    FONT = [pygame.font.Font(ttf, int(size*HEIGHT))
            for ttf, size in settings.fonts]
    timestamp("sysinfo")
    main()
