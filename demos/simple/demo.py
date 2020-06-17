"""
Simplest possible demo
"""
import pathlib
import sys
import types

sys.path.insert(0, '../..')

import pyflexconfig

config = types.SimpleNamespace()
config.

default_settings_path = pathlib.Path(__file__).resolve().parent / "defaultsettings.py"

pyflexconfig.bootstrap(config, defaults_path=default_settings_path)

print(config)
