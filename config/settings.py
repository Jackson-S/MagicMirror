# -*- coding: UTF-8 -*-

#############################################################################
# All settings in this file are user-changable. Don't change the formatting #
# or you may cause weird bugs. I will not toubleshoot issues if you have    #
# modified this file and don't include it in the bug report! Please note    #
# the comments above settings as there are some bugs caused by changing     #
# settings I am already aware of and they are all listed in the comments.   #
#############################################################################

'''Main Settings'''
version = "0.2"

autodetect_resolution = False

resolution = (800, 480)

# True = black on white, False = white on black
invert_colours = False

# Default display mode:
def_disp_mode = "--window"

# Allows mouse to be visible on the window
mouse_visible = False

# Print activity to stdout:
show_debug = True

# Retry connection # times:
attempts = 5

# Sets font options and sizes, TTF fonts only, number is scale factor (multlied
# with resolution height):
# 0 = Loading font,
# 1 = City/Time font,
# 2 = Temperature title,
# 3 = Weather description/News story/FPS counter,
# 4 = Subreddit heading,
# 5 = Weather icon font,
# 6 = Alt news title,
# 7 = Alt news text
fonts = [
        ("resources/font-heavy.ttf", 0.14),
        ("resources/font-heavy.ttf", 0.086),
        ("resources/font-heavy.ttf", 0.067),
        ("resources/font-light.ttf", 0.037),
        ("resources/font-regular.ttf", 0.05),
        ("resources/weather-icons.ttf", 0.25),
        ("resources/font-regular.ttf", 0.08),
        ("resources/font-light.ttf", 0.047)
        ]

# Change the colours around if you'd like. (R, G, B)
colour = [
         (0, 0, 0),        # Background
         (128, 128, 128),  # Grey-text
         (255, 255, 255)   # Foreground
         ]

'''BOMWeatherModule Settings'''
# URL for bom weather data. Do not touch:
weather_url = "ftp://ftp2.bom.gov.au/anon/gen/fwo/IDA00100.dat"

# City to get weather for, Australian capitol cities only:
weather_city = "Sydney"

# Delay before updating old data in seconds, BOM has a flood detection:
weather_update_delay = 3600

saved_weather_data_path = "resources/weather_data"


'''RedditModule Settings'''
reddit_update_delay = 3600

# Items to display for each subreddit:
item_count = 10

# Subreddits to fetch data from:
subreddits = [
              "raspberry_pi",
              "Australia",
              "Worldnews",
              "Sydney"
              ]

# Changed to a fade-in/out bottom feed.
# To get original list behaviour set to false:
bottom_feed = True

# Time between story changes, requires bottom_feed
# setting to be enabled to have any effect:
refresh_time = 6

# User agent string for praw:
useragent = "{}:MagicMirror/Jackson-S/com.github:{} (by /u/plainchips)"


'''TimeModule Settings'''
# 0 = 24hr
# 1 = 12hr
time_format = 0
# for a leading 0 in the month and day use "{d:02d}-{m:02d}-{y}":
date_format = "{d:02d}-{m:02d}-{y}"