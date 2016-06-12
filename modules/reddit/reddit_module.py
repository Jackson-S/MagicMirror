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

    def update(self):
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
                body = self.bodyfont.render(item.title, 1, self.colour)
                body_pos = body.get_rect(left=0, bottom=self.height)
                title = self.titlefont.render(subreddit.title(), 1, self.colour)
                title_height = self.height-body_pos[3]
                title_pos = title.get_rect(left=0, bottom=title_height)
                self.stories.append(((body, body_pos), (title, title_pos)))

    def truncate(text):
        try:
            textwidth = self.bodyfont.render(text, 0, self.colour).get_rect(0, 0)[3]
            if textwidth < self.width:
                if (text[-1] != "?" or "." or "!" or ":") and not title:
                    return u"{}{}".format(text, ".")
                else:
                    return u"{}".format(text)
            else:
                while textwidth > self.width:
                    length -= 1
                    text = u" ".join(text[:length+1].split(" ")[:-1]) + u"…"
                    textwidth = self.bodyfont.render(text, 0, self.colour).get_rect(0, 0)[3]
                return text
        except UnicodeError:
            timestamp("Error shortening string")
            return ""