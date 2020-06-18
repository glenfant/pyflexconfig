import pathlib
import os
import types

import pyflexconfig

config = types.SimpleNamespace(
    HOME=os.getenv("HOME", "unset")
)


def custom_parser(path):
    # Stupid custom parser that just adds an option
    result: dict = pyflexconfig.pure_python_parser(path)
    result["ADDED_BY_PARSER"] = "anything"
    return result


def filters_nothing_more(conf):
    # We do like the standdard filter ;o)
    pyflexconfig.keep_upper_names(conf)
    return


def bootstrap():
    global config
    defaultsettings_path = pathlib.Path(__file__).resolve().parent / "defaultsettings.py"
    pyflexconfig.bootstrap(config, parser=custom_parser, defaults_path=defaultsettings_path,
                           custom_path_envvar="CUSTOM_OPTIONS_FILE", filter_=filters_nothing_more)
