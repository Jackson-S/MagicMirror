'''UI Settings'''
version = "0.1"
# 16:9 (or close to) resolutions only at the moment.
resolution = (1024, 600)
fps_limit = 0
def_disp_mode = "--window"
display_framerate = True
mouse_visible = False
update_delay = 1800

'''Weather Settings'''
# URL for bom weather data. Do not touch:
weather_url = "ftp://ftp2.bom.gov.au/anon/gen/fwo/IDA00100.dat"
# City to get weather for, Australian capitol cities only:
weather_city = "Sydney"
# Delay before updating old data in seconds, BOM has a flood detection:
weather_update_delay = 3600
saved_weather_data_path = "resources/weather_data"

'''News Settings'''
# User agent string for praw:
user_agent = "{}:com.personalproject.magicmirror:{} (by /u/plainchips)"
# Items to display for each subreddit:
item_count = 6
# Subreddits to fetch data from
subreddits = ["worldnews", "australia", "sydney"]