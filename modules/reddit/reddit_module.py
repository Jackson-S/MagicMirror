# -*- coding: UTF-8 -*-
'''Shows a scrolling news headline ticker from reddit.com'''
import time
from platform import system
import praw
import config.settings as settings
from debug_output import timestamp


class RedditModule(object):
    '''Fetches headlines from reddit.com'''
    def __init__(self, width, height, colour, font):
        timestamp("Initialising news module...")
        self.font = (font[0], font[1])
        self.colour = colour
        self.width = width
        self.height = height
        self.stories = []
        self.count = 0
        self.nextupdatetime = 0
        self.nextrefreshtime = 0

    def update(self):
        '''called when update is triggered. return next item'''
        if self.nextrefreshtime < time.time():
            self.nextrefreshtime = time.time() + settings.reddit_refresh_delay
            self.stories = []
            self.fetch_news()
            self.count = 0
        self.count += 1
        return self.stories[self.count % len(self.stories)]

    def need_update(self):
        '''Returns true if update required'''
        if time.time() >= self.nextupdatetime:
            self.nextupdatetime = time.time() + settings.refresh_time
            return True
        else:
            return False

    def fetch_news(self):
        '''Gets new stories when called'''
        for subreddit in settings.reddit_subreddits:
            timestamp("Fetching subreddit - {}...".format(subreddit))
            useragent = "{}:MagicMirror/Jackson-S/com.github:{} (by /u/plainchips)"
            useragent = useragent.format(system(), settings.version)
            prawagent = praw.Reddit(user_agent=useragent)
            sub = prawagent.get_subreddit(subreddit)
            sub = sub.get_top_from_day(limit=settings.reddit_item_count)
            for item in sub:
                body = self.font[1].render(self.truncate(item.title), 1, self.colour)
                body_pos = body.get_rect(left=0, bottom=self.height)
                title = self.font[0].render(subreddit.title(), 1, self.colour)
                title_height = self.height-body_pos[3]
                title_pos = title.get_rect(left=0, bottom=title_height)
                self.stories.append(((body, body_pos), (title, title_pos)))

    def truncate(self, text):
        '''Truancates text passed in if it is too wide for screen'''
        try:
            textwidth = self.font[1].render(text, 0, self.colour)
            textwidth = textwidth.get_rect(left=0, top=0)
            if textwidth[2] < self.width:
                return u"{}".format(text)
            else:
                length = len(text)
                while textwidth[2] > self.width*0.99:
                    length -= 1
                    text = u" ".join(text[:length+1].split(" ")[:-1]) + u"…"
                    textwidth = self.font[1].render(text, 0, self.colour)
                    textwidth = textwidth.get_rect(left=0, top=0)
                return text
        except UnicodeError:
            timestamp("Error shortening string")
            return ""
