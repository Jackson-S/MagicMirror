'''UI Settings'''
version = "0.1"
delay_before_close = 60
resolution = (1024, 600)
fps_limit = 5
display_fps = True

'''Weather Settings'''
# URL for bom weather data. Do not touch:
weather_url = "ftp://ftp2.bom.gov.au/anon/gen/fwo/IDA00100.dat"
# City to get weather for, Australian cities only, ensure capitalisation:
weather_city = "Canberra"
# Delay before updating old data in seconds, BOM has a flood detection however:
weather_update_delay = 3600

'''News Settings'''
# User agent string for praw:
user_agent = "{}:com.personalproject.magicmirror:{} (by /u/plainchips)"
# Items to display for each subreddit:
item_count = 6
# Subreddits to fetch data from
subreddits = ["worldnews", "australia", "sydney"]