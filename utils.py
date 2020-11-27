from pathlib import Path
import json


def yes_no(question: str = "") -> int:
  # 0 = yes, 1 = no, -1 = exit
  response: str = ""
  ending: str = "y/n: "
  while response != "exit":
    response = str(input("{0} {1}".format(question, ending)))
    if response == "y" or response == "Y": return 0
    elif response == "n" or response == "N": return 1
    elif response == "exit": return -1
    else: print("Invalid response")
  return -1


def is_in_dir(p: Path, file: str) -> bool:
  if not p.exists() or not p.is_dir(): return None
  for entry in p.iterdir():
    if str(entry) == str(file): return True
  return False


# Be careful with this
def rmdir_recursive(p: Path) -> int:
  if not p.exists() and not p.is_symlink():
    print("{0} does not exist".format(p))
    return 1
  if p.is_dir():
    for entry in p.iterdir():
      rmdir_recursive(entry)
    try: p.rmdir()
    except Exception as err:
      print("Could not remove {0}: {1}".format(p, err))
  else:
    try: p.unlink(missing_ok = True)
    except Exception as err: 
      print("Could not remove {0}: {1}".format(p, err))
      return 1
    else:
      return 0
  

def safe_symlink(target: Path, lpath: Path, overwrite: bool = False) -> int:
  if lpath.exists() and overwrite is False:
    print("Symlink Error: "
      "{0} already exists and overwrite is False".format(lpath))
    return 1
  
  try: lpath.unlink(True)
  except Exception as err:
    print("Symlink Error: {0}".format(err))
    return 1

  try: lpath.symlink_to(target)
  except Exception as err:
    print("Symlink Error: {0}".format(err))
    return 1
  return 0


def safe_mkdir(p: Path) -> int:
  try:
    p.mkdir()
  except Exception as err:
    print("Directory already exists: {0}".format(err))
    return 1
  except Exception as err:
    print("Could not create directory: {0}".format(err))
    return 2
  return 0
  

def safe_json_update(p: Path, updates: dict) -> dict:
  current: dict = safe_json_loads(p)

  if current is None:
    print("merge_dictionary() error")
    return 1
  try: 
    current |= updates
  except Exception as err:
    print("merge_dictionary(): {0}".format(err))
    return 1

  if safe_json_dumps(p, current):
    print("merge_dictionary() error")
    return 1
  return 0
  
  
def safe_json_dumps(p: Path, d: dict) -> int:
  json_indent = 4
  try:
    p.write_text(json.dumps(d, indent = json_indent))
  except Exception as err:
    print("Could not dump json data to {0}: {1}".format(p, err))
    return 1
  return 0

def safe_json_loads(p: Path) -> dict:
  data: dict = None
  try:
    data = json.loads(p.read_text())
  except json.JSONDecodeError as err:
    print("Could not load {0}: {1}".format(p, err))
    return None
  return data


def sig_handler(signum: int, frame) -> int:
  print()
  exit(signum)