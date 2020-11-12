import subprocess
import signal
import time
import json
import pprint
from pathlib import Path
from const import *
import utils
import strs
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
def menu() -> int:
  userin = ""
  num_commands = len(COMMANDS) - 1
  funcs = globals()
  index = 0

  subprocess.run(CLEAR_C)
  while True:
    print(strs.TITLE)
    print("Options:", *OPTIONS, sep = OPTIONS_STYLE)
    userin = input(PROMPT)
    if userin == EXIT: exit(0)
    for command in COMMANDS:
      index = command.index
      if userin == command:
        funcs[command]()
        continue
      elif index == num_commands:
        print(userin + ":", strs.E_BAD_C)
        subprocess.run(CLEAR_C)
  return 0
    


def chk_dir() -> int:
  p: Path = None
  userIn: str = "" 
  settings: dict = utils.safe_json_loads(Path(SETTINGS_PATH))

  if settings == None:
    print(strs.E_SET_LOAD)
    exit(1)
  try:
    p = Path(settings[K_DIR])
  except KeyError as err:
    print(strs.E_KEY.format(err, SETTINGS_PATH))
  if p.exists():
    return 0
  
  print(strs.NO_DIR.format(p))
  while True:
    userIn = str(input(strs.ENTER_DIR.format(DEFAULT_PATH)))
    if(userIn == EXIT): return 1
    if(userIn == NONE): userIn = DEFAULT_PATH

    p = Path(userIn).expanduser()
    try:
      p.mkdir()
    except FileExistsError as err:
      print(strs.E_DIR_EXISTS.format(err))
      continue
    except FileNotFoundError as err:
      print(strs.E_MKDIR.format(err))
      continue

    settings[K_DIR] = str(p)
    if utils.safe_json_dumps(Path(SETTINGS_PATH), settings):
      return 1
    break
  return 0


def chk_settings() -> int:
  p: Path = Path(SETTINGS_PATH)
  test_json: dict = None

  if not p.exists(): 
    print(strs.SET_NEXIST)
  else:
    test_json = utils.safe_json_loads(p)
    if test_json != None:
      try:
        test_json[K_DIR]
      except KeyError as err:
        print(strs.E_KEY.format(err, p)) 
        print(strs.E_SET_LOAD) 
      else:
        return 0

  chk = utils.yes_no(strs.SET_GEN)
  if chk == 1:
    if utils.safe_json_dumps(p, INIT_SETTINGS):
      print(strs.E_SET_INIT)
      return 1
  else:
    print(strs.SET_EDIT)
    return 1
  

def main() -> int:
  signal.signal(signal.SIGINT, utils.sig_handler)
  if chk_settings(): return 1
  if chk_dir(): return 1
  if menu(): return 1
  return 0
  
if __name__ == "__main__":
  main()
