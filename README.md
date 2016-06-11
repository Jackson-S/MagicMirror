##**Magic Mirror**
Modular magic mirror display written in python.
![Screenshot](/screenshots/screenshot1.png)


####Requirements:
    - pygame
    - praw (for reddit module)

####Usage:
>python main.py [--display mode]

######Display modes:
    - fullscreen
    - hwfullscreen
    - doublebuffered
    - noframe
    - windowed
--noframe gives a border-less window, --hwfullscreen is the same as fullscreen on all platforms I have tested
the rest should be self-explanatory.

Fonts can be customised, however expect some issues with overlap as this is not supported.

Tested on Raspbian (on a RPi 3 and RPi0) and Mac OS X, submit an issue if it fails to run on your system
and I will attempt to address it.

This program is provided under the MIT license and as such it comes without any warranty,
express or implied and any issues or damages lie solely as the responsibility of the user and no one else.
Anybody redistributing this program must include the license file in their program.
All fonts used in this program are under the SIL 1.1 Open Font License, license details can be found under
/resources/font.
