import const

TITLE = "Minecraft Server Manager " + const.VERSION
ENT_EXIT = "Enter exit at any time to go back/exit"
EULA_CHK = ("Do you agree to the Minecraft EULA?")
INSTALL = ("Install Directory (default is {0}): ".format(const.DEFAULT_PATH))
SET_GEN = ("Would you like to (re)create it with the default settings?")
SET_EDIT = ("Manually edit settings.json or re-run to create a default.")
SET_NEXIST = ("settings.json not found at {0}".format(const.SETTINGS_PATH))

ENTER_DIR = ("Enter a new install directory (default is {0}):\n")
NO_DIR = ("Looks like {0} doesn't exist.")
LATEST_INSTALLED = (("Latest version {0} already installed"))
DOWNLOAD_JAR = ("Downloading server version {0}")
NEW_SRV_NAME = ("Enter a name for your new sever: ")
NEW_SRV_VER = ("Enter a server version to use (default is latest): ")
INIT_PROP = ("Initializing server.properties")
LOOK_SERVER = ("Looking online for version {0}")

ANY_CONTINUE = ("Press any key to continue")

# Error messages
E_KEY = "Key Error: {0} in {1}"
E_SET_INIT = ("Couldn't create settings.json\nYou can try creating "
              "it manually at " + const.SETTINGS_PATH + 
              "\nSee const.py for format")
E_SET_LOAD = ("Could not load settings.json")
E_BAD_C = ("{0}: Invalid command")
E_DIR_EXISTS = ("Directory already exists: {0}")
E_MKDIR = ("Could not create directory: {0}")
E_JSON_UPDATE = ("Could not update {0}")
E_MAKE_SERVER = ("Could not create server: {0}")
E_NAME_SLASH = ("Server names cannot contain /")
E_PATH_EXISTS = ("Path: {0} already exists")
E_SRV_EXISTS = ("Server {0} already exists")
E_WRITE_TEXT = ("Could not write to {0}")
E_EULA = ("Could not create eula.txt")
E_NOMEM = ("Not enough free memory")
E_INT = ("Not a valid integer")
E_LATEST = ("Could not check for latest version.")

# Questions
Q_MEM = ("How much memory for the server (in GiB): ")
Q_MEM_CONF = ("Is {0} GiB ok? ")
