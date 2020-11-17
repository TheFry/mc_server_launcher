import const

TITLE = "Minecraft Server Manager " + const.VERSION
INSTALL = ("Install Directory (default is {0}): ".format(const.DEFAULT_PATH))
SET_GEN = ("Would you like to (re)create it with the default settings?")
SET_EDIT = ("Manually edit settings.json or re-run to create a default.")
SET_NEXIST = ("settings.json not found at {0}".format(const.SETTINGS_PATH))

ENTER_DIR = ("Enter a new install directory (default is {0}):\n")
NO_DIR = ("Looks like {0} doesn't exist.")

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

