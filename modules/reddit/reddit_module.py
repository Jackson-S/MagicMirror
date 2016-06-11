import time
import pygame
import praw
import config.settings as settings
from debug_output import timestamp
from platform import system


class RedditModule:
    # TODO: Cropping, Error handling
    def __init__(self, display, colour, titlefont, bodyfont):
        timestamp("Initialising news module...")
        subreddits = settings.subreddits
        limit = settings.item_count
        useragent = settings.useragent.format(system(), settings.version)
        praw_agent = praw.Reddit(user_agent=useragent)
        width = display.get_width()
        height = display.get_height()
        self.stories = []
        for subreddit in subreddits:
            timestamp("Fetching {}".format(subreddit))
            sub = praw_agent.get_subreddit(subreddit)
            sub = sub.get_top_from_day(limit=limit)
            for item in sub:
                body = bodyfont.render(item.title, 1, colour)
                body_pos = body.get_rect(left=width*0.01, bottom=height)
                title = titlefont.render(subreddit.title(), 1, colour)
                title_pos = title.get_rect(left=width*0.01, bottom=height-body_pos[3])
                self.stories.append(((body, body_pos), (title, title_pos)))
        self.count, self.nextupdatetime = 0, 0

    def update(self):
        self.count += 1
        return self.stories[self.count % len(self.stories)]

    def need_update(self):
        if time.time() >= self.nextupdatetime:
            #self.nextupdatetime = time.time() + settings.refresh_time
            return True
        else:
            return True
