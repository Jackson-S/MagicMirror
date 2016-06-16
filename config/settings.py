# -*- coding: UTF-8 -*-

""" All settings in this file are user-changeable. Don't change the formatting
    or you may cause weird bugs. I will not troubleshoot issues if you have
    modified this file and don't include it in the bug report! Please note
    the comments above settings as there are some bugs caused by changing
    settings I am already aware of and they are all listed in the comments.
"""

from os import path

'''Main Settings'''
version = "0.5"

# Allows mouse to be visible on the window, if you want that for some reason:
mouse_visible = False

# Show debug activity of stdout, useful for module creation, and debugging:
show_debug = False

# If the network connection is lost this is the amount of tries to re-download
# data after failure:
attempts = 5

# Sets font options and sizes, TTF fonts only, number is scale factor (multiplied
# with resolution height):
# 0 = Loading font,
# 1 = City/Time font,
# 2 = Temperature title,
# 3 = Weather description/News story/FPS counter,
# 4 = Subreddit heading,
# 5 = Weather icon font,
# 6 = Alt news title,
# 7 = Alt news text
fonts = [("resources/font-heavy.ttf", 0.14),
         ("resources/font-heavy.ttf", 0.086),
         ("resources/font-heavy.ttf", 0.067),
         ("resources/font-light.ttf", 0.037),
         ("resources/font-regular.ttf", 0.05),
         ("resources/weather-icons.ttf", 0.25),
         ("resources/font-regular.ttf", 0.08),
         ("resources/font-light.ttf", 0.047)
         ]

# Change the colours around if you'd like. (R, G, B):
colour = [(0, 0, 0),  # Background
          (128, 128, 128),  # Grey-text
          (255, 255, 255)  # Foreground
          ]

'''BOMWeatherModule Settings'''
# City to get weather for, Australian capitol cities only:
weather_city = "Sydney"

# Delay before allowing a  data update in seconds,
# Do not flood BOM, it's only current/next day weather data anyway:
weather_update_delay = 3600

saved_weather_data_path = "resources/weather_data"

'''RedditModule Settings'''
reddit_refresh_delay = 3600

# Items to display for each subreddit:
reddit_item_count = 10

# Time between story changes, requires bottom_feed
# setting to be enabled to have any effect:
refresh_time = 6

# Subreddits to get headlines from:
reddit_subreddits = [
                     "worldnews"
                     ]

'''TimeModule Settings'''
# 0 = 24hr
# 1 = 12hr
time_format = 1
# for a leading 0 in the month and day use "{d:02d}-{m:02d}-{y}":
date_format = "{d:02d}-{m:02d}-{y}"
# select if you want the date to display or not:
display_date = True

'''Picture Display Settings'''
picture_delay_time = 10
picturepath = path.join("resources", "images")
