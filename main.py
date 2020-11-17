import subprocess
import signal
import time
import json
import pprint
from pathlib import Path
from const import *
import utils
import strs
from jmgr import JarManager


def help():
  # to do
  print("help")

def kill():
  # to do
  print("kill")

def launch(p: Path):
  
  print(p)
  input()
  # to do
  

# Prints a main menu and launches functions associated
# with the commands that a user enters.
def menu(p: Path) -> int:
  userin = ""
  num_commands = len(COMMANDS) - 1
  funcs = globals()
  index = 0

  while True:
    subprocess.run(CLEAR_C)
    print(strs.TITLE)
    print("Options:", *OPTIONS, sep = OPTIONS_STYLE)
    userin = input(PROMPT)
    if userin == EXIT: exit(0)
    for command in COMMANDS:
      index = command.index
      if userin == command:
        funcs[command](p)
        continue
      elif index == num_commands:
        print(userin + ":", strs.E_BAD_C)
  return 0
    

def chk_server(p: Path) -> int:
  jar_path = Path(str(p) + JAR_DIR)
  servers_path = Path(str(p) + SERVER_DIR)
  mgr = JarManager()
  latest: str = ""

  if not servers_path.exists() and utils.safe_mkdir(servers_path): return 2
  if not jar_path.exists() and utils.safe_mkdir(jar_path): return 2
  latest = mgr.get_latest_id()
  if latest is None: return 1
  latest = latest + mgr.extension
  for entry in jar_path.iterdir():
    if entry.name == latest:
      print("Latest jar already installed")
      return 0

  print("Downloading new server version {0}".format(latest))
  if mgr.get_jar(str(jar_path)): return 1
  return 0
  

def chk_dir(p: Path) -> Path:
  userIn: str = "" 

  if p.exists():
    return p
  while True:
    userIn = str(input(strs.ENTER_DIR.format(DEFAULT_PATH)))
    if(userIn == EXIT): return None
    if(userIn == NONE): userIn = DEFAULT_PATH

    p = Path(userIn).expanduser()
    if utils.safe_mkdir(p):
      print(strs.E_MKDIR.format(str(p)))
      continue
    break
    
  if utils.safe_json_update(Path(SETTINGS_PATH), {K_DIR: str(p)}):
    print(strs.E_SET_INIT)
    return None
  return p


def chk_settings() -> Path:
  p: Path = Path(SETTINGS_PATH)
  if not p.exists(): 
    print(strs.SET_NEXIST)
  else:
    SETTINGS = utils.safe_json_loads(p)
    if SETTINGS != None:
      try:
        p = Path(SETTINGS[K_DIR])
      except KeyError as err:
        print(strs.E_KEY.format(err, p)) 
        print(strs.E_SET_LOAD) 
      else:
        return p

  chk = utils.yes_no(strs.SET_GEN)
  if chk == 1:
    if utils.safe_json_dumps(p, INIT_SETTINGS):
      print(strs.E_SET_INIT)
      return None
  else:
    print(strs.SET_EDIT)
    return None
  return Path(DEFAULT_PATH)


def main() -> int:
  signal.signal(signal.SIGINT, utils.sig_handler)
  p = chk_settings()
  if p is None: return 1
  p = chk_dir(p)
  if p is None: return 1
  if chk_server(p) == 2: return 1
  return 0
  
if __name__ == "__main__":
  main()
