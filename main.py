import subprocess
import signal
import time
from pathlib import Path
import pprint
from constants import *
from download import *

# from download import *


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


# def 
# # Return a 
# def get_versions(input = "latest"):
#   mc_json = None
#   jar_url = None
#   jar_json = None

#   # Download json file with list of all versions
#   try:
#     mc_json = json.loads(requests.get(VERSIONS_URL).text)
#   except Exception as err:
#     print("{0}\n{1}".format(D_MANUAL, err))
#     exit(1)
#   return mc_json

#   # Get URL for version specific json file
#   try: 
#     if input == "latest": input = mc_json["latest"]["release"]
#     versions = mc_json["versions"]
#     # The next two lines are just to test that the json file
#     # hasn't changed
#     versions[0]["id"]
#     versions[0]["url"]
#   except Exception as err:
#     print("{0}\n{1}".format(D_MANUAL, err))

#   for version in mc_json["versions"]:
#     if version["id"] == input:
#       jar_url = version["url"]
  
#   if jar_url == None:
#     print("Could not find version {0}. Check the name".format(input))

#   # download version specific json file
#   try:
#     jar_json = json.loads(requests.get(jar_url).text)
#   except Exception as err:
#     print("{0}\n{1}".format(D_MANUAL, err))
#   pprint.pprint(jar_url)
#   return jar_json
  

# Download a json file from mojang that contains urls
# to all of the different server versions. Downloads the
# latest version.
def download_server():
  path = PATH + "/server.jar"
  jar = download_server_jar()
  f = open(path, "wb")

  f.write(jar.content)
  jar.close()
  f.close()


# Check if install directory exists and create if needed
# Download latest jar if no jar is found. This is not an update function
def check_dir():
  p = Path(PATH)

  if not p.exists():
    print("Creating directory" + PATH)
    try:
      p.mkdir(exist_ok = True)
    except Exception as err:
      print("Could not create dir:", PATH)
      print(err)
      exit(1)

  p = Path(PATH + "server.jar")
  if not p.exists():
    print("Downloading latest server.jar")
    download_server()


def main():
  signal.signal(signal.SIGINT, sig_handler)
  check_dir()
  menu()

  

if __name__ == "__main__":
  main()