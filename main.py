import subprocess
import signal
import time
import json
from math import pow
from pathlib import Path
from copy import deepcopy
from psutil import virtual_memory
from const import *
import utils
import strs
from jmgr import JarManager
from init import chk_settings, chk_dir, chk_servers


def mk_launch_cmd(mem: int = None, init: bool = False) -> str:
  GiB = pow(1024, 3)
  free_mem = virtual_memory().available / GiB
  cmd: str = ""
  o_init = " --initSettings"
  
  if mem is None:
    while mem != EXIT:
      try:
        mem = int(input(strs.Q_MEM))
      except ValueError:
        print(strs.E_INT)
        continue
      if mem >= free_mem:
        print(strs.E_NOMEM)
        continue
      if utils.yes_no(strs.Q_MEM_CONF.format(mem)): continue
      break    
  elif type(mem) != int:
    print(strs.E_INT)
    return None
  elif mem >= free_mem:
    print(strs.E_NOMEM)
    return None
  if mem == EXIT: return None

  cmd = LAUNCH_C.format(mem, JAR_NAME)
  if init is True: cmd = cmd + o_init
  return cmd


def help(p: Path):
  # to do
  print("help")

def kill(p: Path):
  # to do
  print("kill")


def check_eula(p: Path) -> int:
  if not p.exists and utils.safe_mkdir(p):
    print(strs.E_EULA)
  if utils.yes_no("{0}\n{1}".format(EULA_URL, strs.EULA_CHK)):
    try: p.write_text(EULA_F)
    except Exception as err: 
      print(strs.E_WRITE_TEXT.format(p))
      print(err)
      input()
    return 1
  try: p.write_text(EULA_T)
  except:
    print(strs.E_WRITE_TEXT.format(p))
    return 1
  return 0


# Ask the user which server version they want to use,
# and download it if needed.
def mk_srv_version(server_path: Path, jars_path: Path) -> int:
  mgr = JarManager()
  link_path = Path("{0}/{1}".format(str(server_path), "server.jar"))
  userin: str = NONE
  tf = False

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
    tf = utils.is_in_dir(jars_path, jar_path)
    if tf is False:
      print(strs.LOOK_SERVER.format(userin))
      if mgr.build_exists(userin):
        print(strs.DOWNLOAD_JAR.format(userin))
        if mgr.get_jar(jars_path, userin) is None: continue
        break
      else:
        print("Couldn't find {0}".format(userin))
        continue
    elif tf is None:
      return 1
    else: break

  if utils.safe_symlink(jar_path, link_path): 
    input()
    return 1
  return 0


# Create the directory for a new server
def mk_srv_dir(servers_path: Path) -> Path:
  userin: str = NONE
  server_path: Path = None

  while userin != EXIT:
    userin = str(input(strs.NEW_SRV_NAME))
    if userin == EXIT: return None
    if userin == NONE: continue
    try: userin.index("/")
    except: pass
    else:
      print(strs.E_NAME_SLASH)
      continue

    server_path = Path("{0}/{1}".format(str(servers_path), userin))
    if utils.is_in_dir(servers_path, server_path):
      print(strs.E_SRV_EXISTS.format(userin))
      continue
    server_path = Path("{0}/{1}".format(str(servers_path), userin))
    if utils.safe_mkdir(server_path): 
      try: server_path.rmdir()
      except: pass
      continue
    break
  return server_path
  

# Create a new server
def create(p: Path) -> int:
  servers_path = Path(str(p) + SERVER_DIR)
  jars_path = Path(str(p) + JAR_DIR)
  server_path: Path = None

  if not servers_path.exists() and utils.safe_mkdir(servers_path):
    input()
    return 1
  if not jars_path.exists() and utils.safe_mkdir(jars_path):
    input()
    return 1

  server_path = mk_srv_dir(servers_path)
  if server_path is None:
    input()
    return 1

  if mk_srv_version(server_path, jars_path): 
    print(strs.E_MAKE_SERVER.format(server_path))
    input()
    return 1
  if check_eula(Path("{0}{1}".format(server_path, EULA_NAME))): return 1

  cmd = mk_launch_cmd(init = True)
  print(strs.INIT_PROP)
  if cmd is None: return 1
  try: subprocess.run(cmd.split(" "), check = True, cwd = server_path, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL, input = "stop\n", text = True)
  except subprocess.CalledProcessError as err:
    print(err)
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
    print(strs.ENT_EXIT)
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
  

def main() -> int:
  signal.signal(signal.SIGINT, utils.sig_handler)
  p = chk_settings()
  if p is None: return 1
  p = chk_dir(p)
  if p is None: return 1
  chk =  chk_servers(p)
  if chk == 2: return 1
  elif chk == 1:
    print(strs.E_LATEST)
    print(strs.ANY_CONTINUE)
    input()
  if menu(p): return 1
  return 0
  

if __name__ == "__main__":
  main()
