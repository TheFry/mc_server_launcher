# mc_server_launcher
Python program to launch and manage Minecraft servers on a unix-like system
This is a work in progress and it doesn't really do anything yet. I'm trying to
make this as modular as possible so functions can be reused in later projects. 
Currently this program only creates a default directory. I've written a class to
make downloading server/client jars pretty easy. I'm using a strs.py to hold
99% of the strings printed in this program. utils.py is the exception to this because it
is designed to be used in other projects.

REQUIRES PYTHON 3.9+
Uses pipenv/pyenv to manage dependencies
1.) Install pipenv from your system's package manager, or install it with pip.
2.) cd into mc_server_launcher and run pipenv install
3.) If it says that python 3.9 is not installed to your system, install pyenv
    to your system and and rerun pipenv install
4.) pipenv run python main.py

In progress:
Init the server
Add ability to launch/kill server

Future features:
Multiple world support
Server configuration
Specify server version
Interact with server via commands
curses interface


