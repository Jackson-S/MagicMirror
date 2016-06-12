# -*- coding: UTF-8 -*-

import time
from platform import system
import pygame
import praw
import config.settings as settings
from debug_output import timestamp


class RedditModule:
    # TODO: Cropping, Error handling
    def __init__(self, width, height, colour, titlefont, bodyfont):
        timestamp("Initialising news module...")
        self.subreddits = settings.subreddits
        self.limit = settings.item_count
        self.titlefont = titlefont
        self.bodyfont = bodyfont
        self.colour = colour
        self.width = width
        self.height = height
        useragent = settings.useragent.format(system(), settings.version)
        self.praw_agent = praw.Reddit(user_agent=useragent)
        self.stories = []
        self.fetch_news()
        self.count = 0
        self.nextupdatetime = 0
        self.nextrefreshtime = time.time() + settings.reddit_update_delay

    def update(self):
        if self.nextrefreshtime < time.time():
            self.fetch_news()
            self.count = 0
        self.count += 1
        return self.stories[self.count % len(self.stories)]

    def need_update(self):
        if time.time() >= self.nextupdatetime:
            self.nextupdatetime = time.time() + settings.refresh_time
            return True
        else:
            return False

    def fetch_news(self):
        for subreddit in self.subreddits:
            timestamp("Fetching subreddit - {}...".format(subreddit))
            sub = self.praw_agent.get_subreddit(subreddit)
            sub = sub.get_top_from_day(limit=self.limit)
            for item in sub:
                body = self.bodyfont.render(self.truncate(item.title), 1, self.colour)
                body_pos = body.get_rect(left=0, bottom=self.height)
                title = self.titlefont.render(subreddit.title(), 1, self.colour)
                title_height = self.height-body_pos[3]
                title_pos = title.get_rect(left=0, bottom=title_height)
                self.stories.append(((body, body_pos), (title, title_pos)))

    def truncate(self, text):
        try:
            textwidth = self.bodyfont.render(text, 0, self.colour)
            textwidth = textwidth.get_rect(left=0, top=0)
            if textwidth[2] < self.width:
                return u"{}".format(text)
            else:
                length = len(text)
                while textwidth[2] > self.width*0.99:
                    length -= 1
                    text = u" ".join(text[:length+1].split(" ")[:-1]) + u"…"
                    textwidth = self.bodyfont.render(text, 0, self.colour)
                    textwidth = textwidth.get_rect(left=0, top=0)
                return text
        except UnicodeError:
            timestamp("Error shortening string")
            return ""