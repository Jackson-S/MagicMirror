# -*- coding: UTF-8 -*-
"""Shows a scrolling news headline ticker from reddit.com"""
import time
from platform import system
import praw
from modules.BaseModule import BaseModule
from config.settings import (reddit_item_count,
                             reddit_refresh_delay,
                             reddit_subreddits,
                             reddit_text_display_time,
                             version
                             )
from debug_output import timestamp


class RedditModule(BaseModule):
    """Fetches headlines from reddit.com"""
    def __init__(self):
        timestamp("Initialising reddit module...")
        super(RedditModule, self).__init__()
        self.stories = self.fetch_news()
        self.count = 0
        self.updatedelay = reddit_text_display_time
        self.nextrefreshtime = 0

    def update(self):
        """called when update is triggered. return next item"""
        timestamp("Updating Reddit module...")
        if self.nextrefreshtime < time.time():
            self.nextrefreshtime = time.time() + reddit_refresh_delay
            self.stories = self.fetch_news()
            self.fetch_news()
            self.count = 0
        self.count += 1
        result = self.stories[self.count % len(self.stories)]
        timestamp("Completed updating Reddit module...")
        return result

    def fetch_news(self):
        """Gets new stories when called"""
        stories = []
        for subreddit in reddit_subreddits:
            timestamp("Fetching subreddit - {}...".format(subreddit))
            useragent = ("{}:MagicMirror/Jackson-S/com.github:{} " +
                         "(by /u/plainchips)"
                         )
            useragent = useragent.format(system(), version)
            prawagent = praw.Reddit(user_agent=useragent)
            sub = prawagent.get_subreddit(subreddit)
            sub = sub.get_top_from_day(limit=reddit_item_count)
            for item in sub:
                body = self.font[7].render(
                    self.truncate(item.title),
                    1, self.colour)
                body_pos = body.get_rect(
                    left=self.width / 100,
                    bottom=self.height * 0.99
                    )
                title = self.font[6].render(
                    subreddit.title(),
                    1, self.colour
                    )
                title_pos = title.get_rect(
                    left=self.width / 100,
                    bottom=self.height * 0.99 - body_pos[3]
                    )
                stories.append([[body, body_pos], [title, title_pos]])
        return stories

    def truncate(self, text):
        """Truncates text passed in if it is too wide for screen"""
        try:
            textwidth = self.font[7].render(text, 0, self.colour)
            textwidth = textwidth.get_rect(left=self.width / 100, top=0)
            if textwidth[2] < self.width * 0.99:
                return u"{}".format(text)
            else:
                length = len(text)
                while textwidth[2] > self.width * 0.99:
                    length -= 1
                    text = u" ".join(text[:length + 1].split(" ")[:-1]) + u"…"
                    textwidth = self.font[7].render(text, 0, self.colour)
                    textwidth = textwidth.get_rect(left=self.width / 100, top=0)
                return text
        except UnicodeError:
            timestamp("Error shortening string")
            return ""
