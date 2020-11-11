import subprocess
import signal
import time
from pathlib import Path
import pprint
from constants import *
from update_jar import download_jar

def help():
  # to do
  print("help")

def kill():
  # to do
  print("kill")

def launch():
  # to do
  subprocess.run(["ls", "-1"])
  input()

# Prints a main menu and launches functions associated
# with the commands that a user enters.
def menu():
  userin = ""
  num_commands = len(COMMANDS) - 1
  funcs = globals()
  index = 0

  subprocess.run(CLEAR_C)
  while(userin != "exit"):
    print(TITLE)
    print("Options:", *OPTIONS, sep = OPTIONS_STYLE)
    userin = input(PROMPT)
    if userin == "exit": exit(0)
    for command in COMMANDS:
      index = command.index
      if userin == command:
        funcs[command]()
        continue
      elif index == num_commands:
        print(userin + ":", BAD_C)
        subprocess.run(CLEAR_C)
    

# Handle ^C
def sig_handler(signum, frame):
  sigint = 2
  if signum == sigint:
    print("\n", EXIT)
    exit(sigint)  


# Check if install directory exists.
# If it doesn't, create it and download the latest
# server.jar from mojang. Uses functions from 
# update_jar.py
def setup_dir():
  p = Path(PATH)
  f = None
  jar = None

  # Check for .mc_server_manager folder in home
  if not p.exists():
    print("Creating directory" + PATH)
    try:
      p.mkdir(exist_ok = True)
    except Exception as err:
      print("Could not create dir:", PATH)
      print(err)
      exit(1)
  
  # Check that server jar is in .mc_server_manager 
  p = Path(PATH + "server.jar")
  if not p.exists():
    print("Downloading latest server.jar")
    jar = download_jar(mode = S_TYPE)

    f = open(str(p), "wb")
    f.write(jar.content)
    jar.close()
    f.close()



def main():
  signal.signal(signal.SIGINT, sig_handler)
  setup_dir()
  menu()


if __name__ == "__main__":
  main()