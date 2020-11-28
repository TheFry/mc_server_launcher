# Use these functions to download data associated 
# with a specific minecraft version (ex: 1.16.4).
# If you want to easily download a jar file, use the function
# download_jar() at the bottom of this file. It basically
# runs all of the functions in this file in order to obtain 
# either a server or client jar file.
import requests
import json
from pathlib import Path

VERSIONS_URL = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
class JarManager:
  extension = ".jar"
  # Json keys
  k_versions = "versions"
  k_release = "release"
  k_url = "url"
  k_latest = "latest"
  k_server = "server"
  k_client = "client"
  default_path = "."

  # Download a jar file with download_info 
  def __download_jar(self, p: Path, download_info: dict, mode: str) -> int:
    response: requests.models.Response = None
    
    try:
      response = requests.get(download_info[mode][self.k_url])
    except KeyError as err:
      print("download_file() Key Error: {0}".format(err))
      return 1
    except Exception as err:
      print("download_file() Network Error: {0}".format(err))
      return 1


    try:
      p.write_bytes(response.content)
    except Exception as err:
      print("download_file() write error: {0}".format(err))
      response.close()
      return 1
    response.close()
    return 0


  # Gets download info. Includes a link to the jar, hashes, and other info
  def __get_download_info(self, build: dict) -> dict:
    download_info: dict = None
    url: str = ""
    
    url = build[self.k_url]
    try:
      download_info = json.loads(requests.get(url).text)["downloads"]
    except Exception as err:
      print("get_download_info() {0}".format(err))
      return None
    return download_info


  # Use the return value of get_builds() and
  # a string build id (ex: "1.16.4") to download a json file 
  # for that specific build. Defaults to the latest build.
  def __get_build_info(self, builds: dict, id: str = k_latest) -> dict:
    versions: dict = None

    # Set id and versions
    try: 
      if id == "latest": id = builds["latest"]["release"]
      versions = builds["versions"]
      # The next two lines check that the json format hasn't changed
      versions[0]["id"]
      versions[0]["url"]
    except Exception as err:
      print("get_build_info() id = {0} \n{1}".format(id, err))
      return None
    
    # Try to find the given version from the list
    for version in builds["versions"]:
      if version["id"] == id:
        return version

    print("get_build_info()\nCouldn't find {0}".format(id))
    print("Check the name")
    return None


  # Downloads a json file from mojang, which
  # contains a list of builds.
  def __get_builds(self) -> dict:
    builds: dict = None

    # Download json file with list of all versions
    try:
      builds = json.loads(requests.get(VERSIONS_URL).text)
    except KeyError as err:
      print("get_builds() Key Error: {0}".format(err))
      return None
    except Exception as err:
      print("get_builds() Network Error: {0}".format(err))
      return None

    return builds


  def build_exists(self, build_id: str) -> bool:
    builds: dict = self.__get_builds()
    
    if builds is None: return False
    try:
      for build in builds["versions"]:
        if build["id"] == build_id: return True
    except KeyError as err:
      print("build_exists() KeyError: {0}".format(err))
      return False
    return False


  def get_latest_id(self) -> str:
    build_id: str = ""
    builds: dict = None
    
    builds = self.__get_builds()
    if builds is None: return None
    try:
      build_id = builds[self.k_latest][self.k_release]
    except KeyError as err:
      print("get_latest_id(): {0}".format(err))
      return None
    return build_id

    
  # Runs through all of the above functions to download a jar file.
  # Version and type (server/client) can be specified. Use this if you
  # want to just download a jar and don't care about the json data.
  def get_jar(self, d_path: Path = Path(default_path),
              id: str = k_latest, mode: str = k_server) -> str:
    builds: dict = None
    build_info: dict = None
    download_info: dict = None

    if id is self.k_latest: id = self.get_latest_id()
    d_path = Path("{0}/{1}{2}".format(d_path, id, self.extension))
    builds = self.__get_builds()
    if builds is None: 
      print("Could not download jar\n")
      return None
    build_info = self.__get_build_info(builds, id)
    if build_info is None:
      print("Could not download jar\n")
      return None
    download_info = self.__get_download_info(build_info)
    if download_info is None:
      print("Could not download jar\n")
      return None
    if self.__download_jar(d_path, download_info, mode):
      print("Could not download jar\n")
      return None
    return d_path