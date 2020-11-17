from pathlib import Path
import json


# def list_options(options: list, pretext: str, postText: str) -> str:
#   response: str = ""

#   while response


def yes_no(question: str = "") -> int:
  # 0 = no, 1 = yes, -1 = exit
  response: str = ""
  ending: str = "y/n: "
  while response != "exit":
    response = str(input("{0} {1}".format(question, ending)))
    if response == "y" or response == "Y": return 1
    elif response == "n" or response == "N": return 0
    elif response == "exit": return -1
    else: print("Invalid response")


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
  

def safe_json_update(p: Path, updates: dict) -> int:
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