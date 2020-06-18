# Override the one from defaultsettings
import os
FIRST_OPTION = False
CUSTOM_ONE = os.getenv("FOO", "unknown")
