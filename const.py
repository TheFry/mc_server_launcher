from pathlib import Path
VERSION = "0.1"
TITLE = "Minecraft Server Manager " + VERSION
DEFAULT_PATH = "{0}/.mc_servers/".format(Path.home())
SETTINGS_PATH = "./settings.json"
PROMPT = "> "
NONE = ""
EXIT = "exit"

OPTIONS = ["launch: Start a server",
           "kill: Stop a server",
           "help: More info about this program",
           "exit: Close this manager. Server will continue to run."
          ]
OPTIONS_STYLE = "\n   "

COMMANDS = ["launch", "kill", "help"]
CLEAR_C = "clear"

MEM = "2G"
LAUNCH_C = ["java",
            "-Xms" + MEM,
            "-Xmx" + MEM,
            "-jar", "server.jar"
           ]

JAR_NAME = "server.jar"
S_TYPE = "server"
C_TYPE = "client"

# Settings keys
K_DIR = "dir"
K_JAR = "jar_name"
K_VERSION = "version"
K_MAIN = "main"

INIT_SETTINGS = {K_DIR: DEFAULT_PATH, K_VERSION: VERSION}
JSON_INDENT = 4