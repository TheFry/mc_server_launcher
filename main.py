import subprocess
import signal
import time
import requests
import json
import pprint
from pathlib import Path
from constants import *

HOME = str(Path.home()) + "/"

  
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
    
    
def sig_handler(signum, frame):
  sigint = 2
  if signum == sigint:
    print("\n", EXIT)
    exit(sigint)  

# Download the latest jar from mojang
def download_jar(path):
  mc_versions = json.loads(requests.get(VERSIONS_URL).text)
  latest = mc_versions["latest"]["release"]

  jar_url = None
  f = None
  r = None

  for version in mc_versions["versions"]:
    if version["id"] == latest:
      jar_url = version["url"]
  
  if(jar_url == None):
    print("Error, could not download server.jar")
    exit(1)

  r = requests.get(jar_url)
  f = open(path, "wb")
  f.write(r.content)
  r.close()
  f.close()


# Check if install directory exists and create if needed
# Download latest jar if no jar is found. This is not an update function
def check_dir():
  path_str = HOME + SERVER_DIR
  print(path_str)
  p = Path(path_str)

  if not p.exists():
    print("Creating directory" + path_str)
    p.mkdir()

  p = Path(path_str + "server.jar")
  if not p.exists():
    print("Downloading latest server.jar")
    download_jar(p)


def main():
  signal.signal(signal.SIGINT, sig_handler)
  check_dir()
  # menu()

if __name__ == "__main__":
  main()