from pathlib import Path
from mcservers.jmgr import JarManager
from const import JAR_DIR, LATEST_SLINK, SERVER_DIR, DEFAULT_PATH,SETTINGS_PATH, K_DIR, SETTINGS_PATH, EXIT, NONE, INIT_SETTINGS
import strs
import utils

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
    latest_id = mgr.get_jar(jars_path)
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