"""
Simplest possible demo
"""
import pathlib
import sys
import types

import pyflexconfig

config = types.SimpleNamespace(
    # Option: You may add hardcoded options here
    FOURTH_OPTION={"anything": "tou want"}
)

# Compute the absolute path to the default settings module (belt and braces)
default_settings_path = pathlib.Path(__file__).resolve().parent / "defaultsettings.py"

pyflexconfig.bootstrap(config, defaults_path=default_settings_path)

print(config)
