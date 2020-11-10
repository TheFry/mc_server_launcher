import requests
import json
import pprint
from constants import PATH

VERSIONS_URL = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
D_MANUAL = "Error: Download the jar manually to {0} server.jar".format(PATH)

def get_builds():
  builds = None
  # Download json file with list of all versions
  try:
    builds = json.loads(requests.get(VERSIONS_URL).text)
  except Exception as err:
    print("{0}\n{1}".format(D_MANUAL, err))
    exit(1)
  return builds

def get_build_info(builds, id = "latest"):
  try: 
    if id == "latest": id = builds["latest"]["release"]
    versions = builds["versions"]
    # The next two lines are just to test that the json file
    # hasn't changed
    versions[0]["id"]
    versions[0]["url"]
  except Exception as err:
    print("{0}\n{1}".format(D_MANUAL, err))
  for version in builds["versions"]:
    if version["id"] == id:
      return version

  print("Could not find {0}. Check the name".format(id))
  return None

def get_download_info(build):
  download_info = None
  url = build["url"]
  try:
    download_info = json.loads(requests.get(url).text)["downloads"]
  except Exception as err:
    print("Could not get download info {0}".format(err))
  return download_info

def download_server_jar(id = "latest"):
  info = get_download_info(get_build_info(get_builds()))
  req = None

  try:
    req = requests.get(info["server"]["url"])
  except Exception as err:
    print("Could not download jar file\n{0}".format(err))
  return req