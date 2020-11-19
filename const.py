from pathlib import Path
VERSION = "0.1"
DEFAULT_PATH = "{0}/.mc_servers".format(Path.home())
SETTINGS_PATH = "./settings.json"

# root = the user defined install directory
SERVER_DIR = "/servers"
JAR_DIR = "/jars"
LATEST_SLINK = "/latest.jar"

PROMPT = "> "
NONE = ""
EXIT = "exit"
EULA_URL = "https://account.mojang.com/documents/minecraft_eula"

OPTIONS = ["launch: Start a server",
           "kill: Stop a server",
           "create: Make a new server",
           "help: More info about this program",
           "exit: Close this manager. Server will continue to run."
          ]

OPTIONS_STYLE = "\n   "

COMMANDS = ["launch", "kill", "create", "help"]
CLEAR_C = "clear"
LS_1COLUMN_C = ["ls", "-1"]

MEM = "2G"
LAUNCH_C = ["java",
            "-Xms" + MEM,
            "-Xmx" + MEM,
            "-jar", "server.jar"
           ]

JAR_NAME = "server.jar"

# Settings keys
K_DIR = "dir"
K_VERSION = "version"

INIT_SETTINGS = {K_DIR: DEFAULT_PATH, K_VERSION: VERSION}
JSON_INDENT = 4