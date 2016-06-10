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
from platform import system
import time
try:
    from urllib.request import Request, urlopen, URLError
except ImportError:
    from urllib2 import Request, urlopen, URLError
    # For python2.7 compatability:
    FileNotFoundError = None
import pygame
import praw
import settings
import translations


def timestamp(activity):
    '''Prints timestamps of functions'''
    if TIMESTAMP is True:
        if activity == "sysinfo":
            try:
                print("OS={}".format(
                    uname()[3]))
                print("PYGAME={}, BACKEND={}".format(
                    pygame.vernum, pygame.display.get_driver()))
                print("PYTHON={}".format(
                    pyver))
                print("VIDEO={}".format(
                    pygame.display.Info()))
                print("DIRECTX={}".format(
                    pygame.dx_version_string))
            except AttributeError:
                pass
        else:
            year, month, day, hour, minute, second = time.localtime()[0:6]
            print("{}/{}/{} {}:{}:{} - {}".format(
                year, month, day, hour, minute, second, activity))


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


def get_news(sub, limit=settings.item_count):
    '''get_news(subreddit: str) -> news: [str]'''
    connection_attempts = 0
    from requests.exceptions import ConnectionError
    try:
        timestamp("Getting news...")
        user_agent = settings.user_agent.format(system(), settings.version)
        reddit, result = praw.Reddit(user_agent=user_agent), {}
        submission = reddit.get_subreddit(sub).get_top_from_day(limit=limit)
        result = []
        for story in submission:
            result.append(story.title)
        timestamp("Completed getting news...")
        return result
    except ConnectionError:
        connection_attempts += 1
        if connection_attempts != settings.attempts:
            timestamp("Failed to connect, trying again in 5 seconds.")
            time.sleep(5)
            return get_news(sub)
        else:
            timestamp("Failed to connect {} times. Quitting...").format(
                settings.attempts
            )
            pygame.quit()
            quit()


def truncate(text, title=False, length=100):
    '''truncate(text, title: bool, length: int, suffix: str) -> unicode'''
    if title:
        text = text.title()
    if len(text) <= length:
        if (text[-1] != "?" or "." or "!" or ":") and not title:
            return u"{}{}".format(text, ".")
        else:
            return u"{}".format(text)
    else:
        return u" ".join(text[:length+1].split(" ")[:-1]) + u"…"


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
    news, stories, stories_pos, subreddit, subreddit_pos = [], [], [], [], []
    for sub in subs:
        news = []
        news.extend(get_news(sub))
        for story in news:
            stories.append(FONT[7].render(
                truncate(story), 1, COLOUR[2]))
            stories_pos.append(stories[-1].get_rect(
                left=WIDTH/100, bottom=HEIGHT-HEIGHT/200))
            subreddit.append(FONT[6].render(
                truncate(sub, title=True), 1, COLOUR[2]))
            subreddit_pos.append(subreddit[-1].get_rect(
                left=WIDTH/100, bottom=HEIGHT-stories_pos[-1][3]*0.8))
            story_right_edge = stories_pos[-1][2]
            # Check if the news item is wider than the screen edge:
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
    timestamp("Completed generating news display...")
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
    date_disp = (FONT[1].render("{}-{}-{}".format(
        day, month, year), 1, COLOUR[2]))
    # TO FIX:
    if minute < 10:
        time_disp = (FONT[1].render("{}:0{}".format(
            hour, minute), 1, COLOUR[2]))
    else:
        time_disp = (FONT[1].render("{}:{}".format(
            hour, minute), 1, COLOUR[2]))
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
    refresh, last_refresh_time = True, time.time()
    # Initialises the display
    # Enables clock, used for frame rate limiter:
    game_clock = pygame.time.Clock()
    pygame.mouse.set_visible(MOUSE_VISIBLE)
    SCREEN.fill(COLOUR[0])
    load_str = FONT[0].render(translations.loading_text, 1, COLOUR[2])
    SCREEN.blit(load_str, load_str.get_rect(centerx=WIDTH/2, centery=HEIGHT/2))
    pygame.display.flip()
    while True:
        time_since_refresh = time.time() - last_refresh_time
        # Sets the framerate (located in settings.py), 0 = no limit:
        if FPS_LIMIT > 0 or refresh is True:
            game_clock.tick(FPS_LIMIT)
        else:
            game_clock.tick()
        # Checks to see if the information needs to be refreshed:
        if refresh is True:
            last_refresh_time, refresh = time.time(), False
            # Fetch the weather and news:
            weather, weather_pos = get_weather_display()
            if settings.bottom_feed:
                sub, sub_pos, story, story_pos = get_news_display()
                story_number, story_disp_time = 0, time.time()
            else:
                story, story_pos = get_alt_news_display()
        # Get the time:
        clock_disp, clock_disp_pos = get_time()
        # Checks for keyboard events (quit), no return:
        check_events(pygame.event.get())
        # Draws the background:
        SCREEN.fill(COLOUR[0])
        # Blits each element to the screen:
        for item, item_pos in zip(weather, weather_pos):
            SCREEN.blit(item, item_pos)
        for item, item_pos in zip(clock_disp, clock_disp_pos):
            SCREEN.blit(item, item_pos)
        if settings.bottom_feed:
            if time.time() - story_disp_time >= settings.refresh_time:
                story_number = (story_number + 1) % settings.item_count
                story_disp_time = time.time()
            SCREEN.blit(sub[story_number], sub_pos[story_number])
            SCREEN.blit(story[story_number], story_pos[story_number])
        else:
            for item, item_pos in zip(story, story_pos):
                SCREEN.blit(item, item_pos)
        # Renders the fps counter:
        if SHOW_FPS is True:
            fps, fps_pos = get_framerate(game_clock)
            SCREEN.blit(fps, fps_pos)
        # Checks if a refresh is required:
        if time_since_refresh > settings.update_delay:
            refresh = True
        # Renders the total display:
        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    # Mode specifically for my personal setup. Feel free to ignore it/remove it:
    if len(argv) > 1:
        if argv[1] == "--pi":
            RESOLUTION = WIDTH, HEIGHT = (1024, 600)
            SCREEN = pygame.display.set_mode((1024, 600), pygame.FULLSCREEN)
            FPS_LIMIT = 1
            MOUSE_VISIBLE = False
            TIMESTAMP = True
            SHOW_FPS = False
    # if above remove change this from elif to if:
    elif settings.autodetect_resolution is False:
        RESOLUTION = WIDTH, HEIGHT = settings.resolution
        SCREEN = pygame.display.set_mode(RESOLUTION, get_display_mode())
        FPS_LIMIT = settings.fps_limit
        MOUSE_VISIBLE = settings.mouse_visible
        TIMESTAMP = settings.timestamp
        SHOW_FPS = settings.display_framerate
    else:
        SCREEN = pygame.display.set_mode((0, 0), get_display_mode())
        RESOLUTION = WIDTH, HEIGHT = SCREEN.get_width(), SCREEN.get_height()
        FPS_LIMIT = settings.fps_limit
        MOUSE_VISIBLE = settings.mouse_visible
        TIMESTAMP = settings.timestamp
        SHOW_FPS = settings.display_framerate
    if TIMESTAMP is True:
        timestamp("sysinfo")
    # Initialise the fonts and colours from translations.py:
    if settings.invert_colours:
        COLOUR = [(255, 255, 255), (0, 0, 0), (0, 0, 0)]
    else:
        COLOUR = [(0, 0, 0), (128, 128, 128), (255, 255, 255)]
    FONT = [pygame.font.Font(ttf, int(size*HEIGHT))
            for ttf, size in settings.fonts]
    main()
