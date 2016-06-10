#############################################################################
# All settings in this file are user-changable. Don't change the formatting #
# or you may cause weird bugs. I will not toubleshoot issues if you have    #
# modified this file and don't include it in the bug report! Please note    #
# the comments above settings as there are some bugs caused by changing     #
# settings I am already aware of and they are all listed in the comments.   #
#############################################################################

'''Main Settings'''
version = "0.2"

autodetect_resolution = True

# 16:9 (or close to) resolutions only at the moment.
resolution = (1024, 640)

# Framerate limit, 0 for unlimited:
fps_limit = 30

# True = black on white, False = white on black
invert_colours = False

# Display framerate in corner:
display_framerate = True

# Default display mode:
def_disp_mode = "--fullscreen"

# Allows mouse to be visible on the window
mouse_visible = False

# Update delay for the program, note that weather has
# a different delay setting that should be equal to
# or a multiple of this:
update_delay = 1800

# Print activity to stdout:
timestamp = False

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

'''Weather Settings'''
# URL for bom weather data. Do not touch:
weather_url = "ftp://ftp2.bom.gov.au/anon/gen/fwo/IDA00100.dat"

# City to get weather for, Australian capitol cities only:
weather_city = "Sydney"

# Delay before updating old data in seconds, BOM has a flood detection:
weather_update_delay = 3600

saved_weather_data_path = "resources/weather_data"

'''News Settings'''
# Items to display for each subreddit:
item_count = 10

# Subreddits to fetch data from:
subreddits = [
              "worldnews",
              "news",
              "australia",
              "sydney",
              "raspberry_pi",
              "gaming",
              "science",
              "programming"
              ]

# Changed to a fade-in/out bottom feed.
# To get original list behaviour set to false:
bottom_feed = True

# Time between story changes, requires bottom_feed
# setting to be enabled to have any effect:
refresh_time = 6

# User agent string for praw:
user_agent = "{}:MagicMirror/Jackson-S/com.github:{} (by /u/plainchips)"