## **Magic Mirror**
Modular magic mirror display written in python.
![Screenshot](/screenshots/screenshot1.png)

#### Requirements:
    - pygame
    - praw (for reddit module)

#### Usage:
>python3 main.py [-h] [-f] [-r width height]

###### Options:
- -h help
- -f full-screen
- -r resolution (width height)

#### Settings:
Further settings can be customised in the config/settings.py file.
If you are having issues with your program then include this file in the bug report as well
as any arguments passed at launch.

#### Modules:
To create a new module follow the instructions laid out in the sample module, if you encounter any
issues that you believe are caused by the application and not your module then please add it to the
issue tracker and I will try and address it.

##### Image Module:
To disable background images just remove all pictures under resources/images or comment out where it's
loaded under main.py. 

#### Compatability:
Requires pygame, which can be obtained via brew on osx (via "brew install homebrew/python/pygame --with-python3") or
via apt-get (sudo apt-get install python-pygame) on most linux distributions. Note that some linux distributions
lack python3 pygame, you can run this program through python 2 (replace "python3" with "python" when launching) or
obtain pygame for python3 via some other means.

Tested on:
- Raspbian (Raspberry Pi Zero and Raspberry Pi 3)
- Linux Mint
- Mac OS X

Tested with python 2.7.11, python 3.5.1 and pypy 5.1.1 all with pygame 1.9.2

Submit an issue if it fails to run on your system with as much detail as possible
and I will attempt to address it.

#### License:
This program is provided under the MIT license and as such it comes without any warranty,
express or implied and any issues or damages lie solely as the responsibility of the user and no one else.
Anybody redistributing this program must include the license file in their program.
All fonts used in this program are under the SIL 1.1 Open Font License, license details for this program and
third party components can be found in LICENSE.md.
