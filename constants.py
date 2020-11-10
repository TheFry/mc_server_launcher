from pathlib import Path

VERSION = "1.0"
TITLE = "Minecraft Server Manager " + VERSION

SERVER_DIR = ".mc_server_launcher/"
PATH = "{0}/{1}".format(str(Path.home()), SERVER_DIR)

OPTIONS = ["launch: Start a server",
           "kill: Stop a server",
           "help: More info about this program",
           "exit: Close this manager. Server will continue to run." ]

COMMANDS = ["launch", "kill", "help"]

OPTIONS_STYLE = "\n   "
PROMPT = "> "


EXIT = "Exiting server manager"
BAD_C = "Command not found"
CLEAR_C = "clear"
MEM = "2G"
LAUNCH_C = ["java",
            "-Xms" + MEM,
            "-Xmx" + MEM,
            "-jar", "server.jar"]
