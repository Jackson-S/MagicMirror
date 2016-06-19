# -*- coding: UTF-8 -*-
""" The strings in this file can all be translated into another language if
    someone is kind enough to volunteer and keep it up to date.
    Non-latin character sets excluding cyrillic may not render correctly
    due to font errors.
"""

# Conditions are searched through by the weather parser and the keys
# are the icon in unicode and the offset required by the weather icon.
conditions = {"sun": u"",
              "clear": u"",
              "cloud": u"",
              "rain": u"",
              "heavy rain": u"",
              "shower": u"",
              "storm": u"",
              "thunder": u"",
              "lightning": u"",
              "hail": u"",
              "snow": u"",
              "cyclone": u"",
              "wind": u"",
              "partly cloudy": u"",
              "light showers": u"",
              "light rain": u"",
              "tornado": u"",
              "overcast": u""
              }

# The offset on the top and bottom required by each symbol to
# display without overlapping.
offset = {u"": [0.7, 0.9],
          u"": [0.3, 0.8],
          u"": [0.3, 1],
          u"": [0.3, 1],
          u"": [0.3, 1],
          u"": [0.3, 1],
          u"": [0.3, 1],
          u"": [0.3, 1],
          u"": [0.3, 0.92],
          u"": [0.3, 0.85],
          u"": [0.3, 0.9],
          u"": [0.35, 0.8],
          u"": [-0.2, 0.7]
          }
