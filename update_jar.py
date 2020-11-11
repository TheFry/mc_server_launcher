# Use these functions to download data associated 
# with a specific minecraft version (ex: 1.16.4).
# If you want to easily download a jar file, use the function
# download_jar() at the bottom of this file. It basically
# runs all of the functions in this file in order to obtain 
# either a server or client jar file.

import requests
import json
import pprint
from constants import PATH, S_TYPE, C_TYPE

VERSIONS_URL = "https://launchermeta.mojang.com/mc/game/version_manifest.json"


# Downloads a json file from mojang, which
# contains a list of builds.
def get_builds():
  builds = None
  # Download json file with list of all versions
  try:
    builds = json.loads(requests.get(VERSIONS_URL).text)
  except Exception as err:
    print("Could not download builds list\n{0}".format(err))
    exit(1)
  return builds


# Use the return value of get_builds() and
# a string build id (ex: "1.16.4") to download a json file 
# for that specific build. Defaults to the latest build.
def get_build_info(builds, id = "latest"):
  try: 
    if id == "latest": id = builds["latest"]["release"]
    versions = builds["versions"]
    # The next two lines are just to test that the json file
    # hasn't changed
    versions[0]["id"]
    versions[0]["url"]
  except Exception as err:
    print("Could not get build info \n{0}".format(err))
  for version in builds["versions"]:
    if version["id"] == id:
      return version

  print("Could not find version {0}. Check the name".format(id))
  return None


# Gets download info. Includes a link to the jar, hashes, and other info
def get_download_info(build):
  download_info = None
  url = build["url"]
  try:
    download_info = json.loads(requests.get(url).text)["downloads"]
  except Exception as err:
    print("Could not get download info {0}".format(err))
  return download_info


# Runs through all of the above functions to download a jar file.
# Version and type (server/client) can be specified. Use this if you
# want to just download a jar and don't care about the json data.
def download_jar(id = "latest", mode = S_TYPE):
  info = get_download_info(get_build_info(get_builds(), id))
  req = None

  try:
    req = requests.get(info[mode]["url"])
  except Exception as err:
    print("Could not download jar file\n{0}".format(err))
  return req