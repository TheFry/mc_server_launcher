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


def help(p: Path):
  # to do
  print("help")

def kill(p: Path):
  # to do
  print("kill")


def check_eula(p: Path) -> int:
  chk: int = 1
  if not p.exists and utils.safe_mkdir(p):
    print("Could not create EULA")
  if utils.yes_no("{0}\n{1}".format(EULA_URL, strs.EULA_CHK)):
    try: p.write_text("eula=false")
    except Exception as err: 
      print(strs.E_WRITE_TEXT.format(p))
      print(err)
      input()
    return 1
  try: p.write_text("eula=true")
  except:
    print(strs.E_WRITE_TEXT.format(p))
    return 1
  return 0

def mk_srv_version(server_path: Path, jars_path: Path) -> int:
  link_path = Path("{0}/{1}".format(str(server_path), "server.jar"))
  userin: str = NONE

  while userin != EXIT:
    userin = str(input(strs.NEW_SRV_VER))
    if userin == EXIT: return 1
    if userin == NONE: userin = "latest"
    try: userin.index("/")
    except: pass
    else:
      print(strs.E_NAME_SLASH)
      continue
    filename = "{0}{1}".format(userin, JarManager.extension)
    jar_path = Path("{0}/{1}".format(jars_path, filename))
    if not utils.check_directory(jars_path, jar_path):
      if utils.safe_symlink(jar_path, link_path): 
        input()
        return 1
      break
    else:
      print("This version is not currently downloaded")
      input()
      return 1
  return 0


def mk_srv_name(servers_path: Path) -> Path:
  userin: str = NONE
  server_path: Path = None
  while userin != EXIT:
    userin = str(input(strs.NEW_SRV_NAME))
    if userin == EXIT: return None
    try: userin.index("/")
    except: pass
    else:
      print(strs.E_NAME_SLASH)
      continue
    server_path = Path("{0}/{1}".format(str(servers_path), userin))
    if not utils.check_directory(servers_path, server_path):
      print(strs.E_SRV_EXISTS.format(userin))
      continue
    server_path = Path("{0}/{1}".format(str(servers_path), userin))
    if utils.safe_mkdir(server_path): continue
    break
  return server_path
  
def create(p: Path) -> int:
  servers_path = Path(str(p) + SERVER_DIR)
  jars_path = Path(str(p) + JAR_DIR)
  server_path: Path = None
  jar_path: Path = None
  link_path: Path = None
  userin: str = NONE
  filename: str = NONE

  if not servers_path.exists() and utils.safe_mkdir(servers_path):
    input()
    return 1
  server_path = mk_srv_name(servers_path)
  if server_path is None:
    input()
    return 1
  if mk_srv_version(server_path, jars_path): return 1
  if check_eula(Path("{0}/{1}".format(server_path, "eula.txt"))): return 1

  print("Initializing server.properties")
  init_c = LAUNCH_C
  init_c.append("--initSettings")
  try: subprocess.run(init_c, cwd = server_path, check = True)
  except subprocess.CalledProcessError as err:
    print("Error initializing server: {0}".format(err))
    input()
    return 1
  return 0
  

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
  

def chk_latest(p: Path) -> int:
  downloaded = False
  latest_id: str = None
  latest_file: Path = None
  jars_path = Path(str(p) + JAR_DIR)
  latest_symlink = Path(str(jars_path) + LATEST_SLINK)
  mgr = JarManager()

  if not jars_path.exists() and utils.safe_mkdir(jars_path): return 1
  latest_id = mgr.get_latest_id()
  if latest_id is None: return 1
  latest_id = latest_id + mgr.extension
  for entry in jars_path.iterdir():
    if entry.name == latest_id:
      print(strs.LATEST_INSTALLED.format(entry.name))
      downloaded = True
      break
  
  latest_file = Path("{0}/{1}".format(str(jars_path), latest_id))
  if not downloaded:
    print(strs.DOWNLOAD_JAR.format(latest_id))
    latest_id = mgr.get_jar(str(jars_path))
    if latest_id is None: return 1
  if utils.safe_symlink(latest_file, latest_symlink, True): return 1
  return 0


def chk_servers(p: Path) -> int:
  jars_path: str = Path(str(p) + JAR_DIR)
  servers_path: str = Path(str(p) + SERVER_DIR)

  if not servers_path.exists() and utils.safe_mkdir(servers_path): return 2
  if not jars_path.exists() and utils.safe_mkdir(jars_path): return 2
  if chk_latest(p): return 1
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

  if not utils.yes_no(strs.SET_GEN):
    if utils.safe_json_dumps(p, INIT_SETTINGS):
      print(strs.E_SET_INIT)
      return None
  else:
    print(strs.SET_EDIT)
    return None
  return Path(DEFAULT_PATH)

# def test() -> int:
#   p = Path("/home/luke/.mc_servers/jars/1.16.4.jar")
#   p2 = Path("/home/luke/.mc_servers/jars/latest.jar")
#   utils.safe_symlink(p, p2)

def main() -> int:
  signal.signal(signal.SIGINT, utils.sig_handler)
  p = chk_settings()
  if p is None: return 1
  p = chk_dir(p)
  if p is None: return 1
  if chk_servers(p) == 2: return 1
  if menu(p): return 1

  return 0
  
if __name__ == "__main__":
  main()
