##**Magic Mirror**

![Screenshot](/screenshot.png)
Supports weather data from the Australian Bureau of Meteorology and news from Reddit.

####Requirements:
    - pygame
    - praw

####Usage:
>python main.py [--display mode]

######Display modes:
    - fullscreen
    - hwfullscreen
    - doublebuffered
    - noframe
    - windowed
--noframe gives a border-less window, --hwfullscreen is the same as fullscreen on all platforms I have tested
the rest should be self-explanatory

Tested on Raspbian (on a RPi 3) and Mac OS X, submit an issue if it fails to run on your system
and I will attempt to address it.

This program is provided under the MIT license and as such it comes without any warranty,
express or implied and any issues or damages lie solely as the responsibility of the user and no one else.
Anybody redistributing this program must include the license file in their program.
